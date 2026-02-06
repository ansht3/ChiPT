# rag_main_kdocs.py
from __future__ import annotations
import os
import json
from typing import List, Dict
from collections import Counter #Used to check where chunking is originating from
from openai import OpenAI

# Select GPU to run on
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

from .milvus_connect import ( 
    _milvus_connect,
    TEXT_FIELD, TITLE_FIELD, DOCID_FIELD,
)

from .vector_database_handling import get_kb_path

from config import OPENAI_BASE_URL, OPENAI_API_KEY, CHAT_COMPLETION_MODEL, RAG_DOCS_EMBEDDING_MODEL


PATH_FIELD          = "path"

SYSTEM_PROMPT = (
    fr"""System prompt: You are a helpful assistant that answers questions based solely on the provided context. Your role is to extract and synthesize information from the given context to provide accurate, relevant answers.
    RAG Template: You are given a user query, some textual context, and rules 
    all inside XML tags. You have to answer the query based on the context
    only, using the format shown in the examples or by including short inline handles like [Title] when citing. Please respect the rules.
    <rules>
    - If asked instructions, always give step-by-step instructions. Do not leave any steps out.
    - If you don't know, just say so.
    - If you are not sure, ask for clarification.
    - Answer in the same language as the user query.
    - If the context appears unreadable or of poor quality, tell the user then answer as best as you can.
    - Do not use any outside knowledge. If the answer is not found in the context, respond with "I don't know the answer."
    - Answer directly and without using xml tags.
    </rules>
    """
)

def _approx_tokens(s: str) -> int:
    return max(1, len(s) // 4)

def _build_full_doc_context_from_paths(doc_paths: dict[str, str],
                                       budget_tokens: int) -> str:
    """
    Combines selected documents into one large context chunk to get injected
    into the user message.
    """
    blocks, used = [], 0
    for title in doc_paths:
        txt = _read_file(doc_paths[title]).strip()
        
        # THE DECISION TREE DOCUMENT WILL BREAK THE CONTEXT GENERATION
        # if title == "decision_tree_handson.md":
        #     continue
        print(f"{title} has {_approx_tokens(txt)} tokens approximately")
        if not txt:
            continue
        tlen = _approx_tokens(txt)
        if used + tlen > budget_tokens:
            break
        blocks.append(f"[{title}]\n{txt}")
        used += tlen
    output = "\n\n---\n\n".join(blocks)
    print(f"Number of tokens of full document context:  {_approx_tokens(output)}")
    return output

def _embed_query(text: str) -> List[float]:
    # Returns an embedding vector for the query
    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
    resp = client.embeddings.create(model=RAG_DOCS_EMBEDDING_MODEL, input=text)
    return resp.data[0].embedding

def _select_topk_docs_by_first_hit(hits: list, k: int) -> list[str]:
    """
    Selects the k most relevant documents using the top n most relevant chunks.
    """
    seen, ordered = set(), []
    for h in hits:
        ent = getattr(h, "entity", {})
        title = (ent or {}).get(TITLE_FIELD) or "Untitled"
        if title not in seen:
            seen.add(title)
            ordered.append(title)
            if len(ordered) == k:
                break
    return ordered

def _select_topk_docs_weighted(
        hits: list,
        k: int,
        alpha: float = 0.75,
        top_n_chunks: int | None = None,
    ) -> list[str]:
    """
    Select top-k documents by a weighted combination of:
      - how early they first appear in the ranked hit list (rank signal)
      - how many chunks they contribute in the top-N hits (count signal)

    Score per doc d:
        R_d = 1 - first_index(d) / N
        C_d = count(d) / max_count
        S_d = alpha * R_d + (1 - alpha) * C_d
    """
    # Optionally cap to first top_n_chunks hits for scoring
    if top_n_chunks is not None:
        hits = hits[:top_n_chunks]

    if not hits:
        return []

    from collections import Counter

    first_idx: dict[str, int] = {}
    counts: Counter[str] = Counter()

    for idx, h in enumerate(hits):
        ent = h.get("entity", {})
        title = ent.get(TITLE_FIELD) or "Untitled"
        counts[title] += 1
        if title not in first_idx:
            first_idx[title] = idx

    if not counts:
        return []

    max_count = max(counts.values())
    N = len(hits)

    doc_scores: dict[str, float] = {}
    for title in counts:
        rank_score = 1.0 - (first_idx[title] / N)
        count_score = counts[title] / max_count
        score = alpha * rank_score + (1.0 - alpha) * count_score
        doc_scores[title] = score

    # Sort by combined score, descending
    ordered_titles = sorted(
        doc_scores.keys(),
        key=lambda t: doc_scores[t],
        reverse=True,
    )

    return ordered_titles[:k]


def _map_doc_to_path(hits: list, wanted_titles: list[str]) -> dict[str, str]:
    """
    Creates a dictionary mapping the k top documents to their paths and
    returns the dict.
    """
    out = {t: None for t in wanted_titles}
    wanted = set(wanted_titles)
    for h in hits:
        ent = getattr(h, "entity", {})
        t   = (ent or {}).get(TITLE_FIELD) or "Untitled"
        if t in wanted and out[t] is None:
            p = (ent or {}).get(PATH_FIELD)
            if p:
                out[t] = p
                if all(out[v] is not None for v in wanted_titles):
                    break
    return {t: p for t, p in out.items() if p}

def _read_file(path: str) -> str:
    # Safe read function in case file is an incorrect format or is corrupted
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def rag_answer(question: str,
               top_k_docs: int = 3,
               ctx_budget_tokens: int = 40000,
               top_n_chunks: int = 50,
               qa_context: str = "",
               kb_name: str = None) -> str:
    # 1) embed query via OpenAI
    qvec = _embed_query(question)

    # 2) ANN: get many chunk candidates
    db_path = get_kb_path(kb_name) if kb_name else None
    conn = _milvus_connect(db_path=db_path); conn.load()
    hits = conn.search(qvec, top_k=top_n_chunks, output_fields=[TITLE_FIELD, PATH_FIELD, TEXT_FIELD])
    # Count how many chunks per file title in the top results
    file_counts = Counter(hit["entity"].get(TITLE_FIELD, "unknown") for hit in hits if "entity" in hit)

    print("Top 10 hits:")
    for i, h in enumerate(hits[:10]):
        ent = h.get("entity", {}) or {}
        title = ent.get(TITLE_FIELD, "unknown")
        # print(ent.get(TEXT_FIELD, "unknown"))
        # print('----------------------------\n\n\n\n\n')
        print(f"{i + 1}: {title}")
    
    print("Chunk counts by file (top {top_n_chunks}):")
    for title, count in file_counts.most_common():
        print(f"{count:2d}  {title}")

    # Chose K documents by first appearance
    # top_docs = _select_topk_docs_by_first_hit(hits, k=top_k_docs)

    # chunks_text = [hit.get("entity", {}).get(TEXT_FIELD, "") for hit in hits]

    #3) choose K documents by weighted rank and count policy
    top_docs = _select_topk_docs_weighted(
        hits,
        k=top_k_docs,
        alpha=0.75,              # tweak if desired
        top_n_chunks=top_n_chunks,
    )
    print("[diag] top_docs:", top_docs)

    # 4) map each doc to its absolute path, then load full files
    doc_paths = _map_doc_to_path(hits, top_docs)
    print("[diag] doc_paths:", doc_paths)  # should be {title: "/abs/path.md", ...}
    context = _build_full_doc_context_from_paths(doc_paths, budget_tokens=ctx_budget_tokens)
    if not context:
        return "Insufficient context to answer from the knowledge base."

    # 5) chat
    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
    print(f"QA context loaded: {qa_context}")
    if qa_context:
        user_msg = (
            f"Context (authoritative; cite using [Title]):\n{context}\n\n"
            f"QA Context:\n{qa_context}\n\n"
            "Output: Full sentences with inline handles after supported statements."
            f"Question:\n{question}\n\n"
        )
    else:
        user_msg = (
            f"Context (authoritative; cite using [Title]):\n{context}\n\n"
            "Output: Full sentences with inline handles after supported statements."
            f"Question:\n{question}\n\n"
        )

    resp = client.chat.completions.create(
        model=CHAT_COMPLETION_MODEL,
        temperature=0.7,
        max_tokens=3000,
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":"user","content":user_msg}]
    )

    return resp.choices[0].message.content.strip()

def rag_answer_stream(
    question: str,
    top_k_docs: int = 3,
    ctx_budget_tokens: int = 40000,
    top_n_chunks: int = 50,
    alpha: float = 0.75,
    kb_name: str = None
):
    """
    Streaming variant of rag_answer(): identical retrieval + doc-selection + prompt,
    but yields SSE lines OpenWebUI can stream.
    """

    def _ent(h):
        # Works whether hits are dicts or objects with .entity
        if isinstance(h, dict):
            return h.get("entity", {}) or {}
        return getattr(h, "entity", {}) or {}

    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

    # 1) embed query
    qvec = _embed_query(question)

    # 2) ANN search over chunks
    db_path = get_kb_path(kb_name) if kb_name else None
    conn = _milvus_connect(db_path=db_path); conn.load()
    hits = conn.search(
        qvec,
        top_k=top_n_chunks,
        output_fields=[TITLE_FIELD, PATH_FIELD, TEXT_FIELD],
    )

    # 3) choose K documents by weighted rank+count policy (same as rag_answer)
    top_docs = _select_topk_docs_weighted(
        hits,
        k=top_k_docs,
        alpha=alpha,
        top_n_chunks=top_n_chunks,
    )
    print("[diag] top_docs:", top_docs)

    # 4) robust doc->path mapping (keeps behavior consistent even if hit type changes)
    doc_paths = {}
    wanted = set(top_docs)
    for h in hits:
        ent = _ent(h)
        t = ent.get(TITLE_FIELD) or "Untitled"
        if t in wanted and t not in doc_paths:
            p = ent.get(PATH_FIELD)
            if p:
                doc_paths[t] = p
                if len(doc_paths) == len(top_docs):
                    break

    print("[diag] doc_paths:", doc_paths)

    context = _build_full_doc_context_from_paths(
        doc_paths,
        budget_tokens=ctx_budget_tokens,
    )

    if not context:
        msg = "Insufficient context to answer from the knowledge base."
        yield f"data: {json.dumps({'choices':[{'delta':{'content': msg}}]})}\n\n"
        return

    # 5) chat (same prompt as rag_answer)
    user_msg = (
        f"Context (authoritative; cite using [Title]):\n{context}\n\n"
        "Output: Full sentences with inline handles after supported statements."
        f"Question:\n{question}\n\n"
    )

    # optional initial role chunk (harmless; helps some clients)
    yield f"data: {json.dumps({'choices':[{'delta':{'role':'assistant'}}]})}\n\n"

    resp = client.chat.completions.create(
        model=CHAT_COMPLETION_MODEL,
        temperature=0.7,
        max_tokens=3000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        stream=True,
    )

    for event in resp:
        delta = event.choices[0].delta
        if delta and getattr(delta, "content", None):
            yield f"data: {json.dumps({'choices':[{'delta':{'content': delta.content}}]})}\n\n"

def rag_answer_stream(question: str):
    """
    Streaming model response
    """
    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

    # build messages etc (same as rag_answer)
    qvec = _embed_query(question)
    conn = _milvus_connect(); conn.load()
    hits = conn.search(qvec, top_k=50, output_fields=[TITLE_FIELD, PATH_FIELD, TEXT_FIELD])
    top_docs = _select_topk_docs_by_first_hit(hits, 5)
    doc_paths = _map_doc_to_path(hits, top_docs)
    context = _build_full_doc_context_from_paths(doc_paths, budget_tokens=40000)

    user_msg = (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
    )

    resp = client.chat.completions.create(
        model=CHAT_COMPLETION_MODEL,
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":"user","content":user_msg}],
        stream=True,
        temperature=0.7,
        max_tokens=3000,
    )

    for event in resp:
        delta = event.choices[0].delta
        if delta and delta.content:
            # IMPORTANT: SSE format required by OpenWebUI
            yield f"data: {json.dumps({'choices':[{'delta':{'content':delta.content}}]})}\n\n"

if __name__ == "__main__":
    import sys
    while True:
        query = input("Enter your question: ").strip()
        if query.lower() == 'q':
            break
        if not query:
            query = "No question was answered, so respond with NA"
        print("Q:", query)
        print(rag_answer(query))
