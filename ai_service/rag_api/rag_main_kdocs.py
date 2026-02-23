# rag_main_kdocs.py
from __future__ import annotations
import os
import json
from typing import List, Dict
from collections import Counter
from openai import OpenAI
import httpx

from config import (
    OPENAI_BASE_URL, OPENAI_API_KEY, CHAT_COMPLETION_MODEL,
    RAG_DOCS_EMBEDDING_MODEL, MILVUS_API_URL,
)

TEXT_FIELD = "text"
TITLE_FIELD = "title"
DOCID_FIELD = "doc_id"
FILE_UUID_FIELD = "file_uuid"
PATH_FIELD = "path"

MILVUS_SEARCH_TIMEOUT = 60.0

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

def _build_full_doc_context_from_paths(doc_infos: dict[str, dict],
                                       budget_tokens: int, kb_name: str = None) -> str:
    """
    Combines selected documents into one large context chunk to get injected
    into the user message.
    """
    blocks, used = [], 0
    for title in doc_infos:
        info = doc_infos[title]
        path = info.get("path")
        uuid = info.get("uuid")
        
        if not path: continue
        
        txt = _read_file(path).strip()
        
        print(f"{title} has {_approx_tokens(txt)} tokens approximately")
        if not txt:
            continue
        tlen = _approx_tokens(txt)
        if used + tlen > budget_tokens:
            break
            
        header = f"[{title}]"
        if uuid and kb_name:
            url = f"/kbs/{kb_name}/docs/{uuid}/view"
            header += f" (Link: {url})"
            
        blocks.append(f"{header}\n{txt}")
        used += tlen
    output = "\n\n---\n\n".join(blocks)
    print(f"Number of tokens of full document context:  {_approx_tokens(output)}")
    return output

def _embed_query(text: str) -> List[float]:
    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
    resp = client.embeddings.create(model=RAG_DOCS_EMBEDDING_MODEL, input=text)
    return resp.data[0].embedding


def _milvus_search(qvec: List[float], top_k: int,
                   output_fields: List[str],
                   kb_name: str = None) -> list:
    """Call the Milvus API /search endpoint and return the hit list."""
    resp = httpx.post(
        f"{MILVUS_API_URL}/search",
        json={
            "kb_name": kb_name,
            "vector": qvec,
            "limit": top_k,
            "output_fields": output_fields,
        },
        timeout=MILVUS_SEARCH_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["results"]


def _select_topk_docs_by_first_hit(hits: list, k: int) -> list[str]:
    """
    Selects the k most relevant documents using the top n most relevant chunks.
    """
    seen, ordered = set(), []
    for h in hits:
        ent = h.get("entity", {}) or {}
        title = ent.get(TITLE_FIELD) or "Untitled"
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
    if top_n_chunks is not None:
        hits = hits[:top_n_chunks]

    if not hits:
        return []

    from collections import Counter

    first_idx: dict[str, int] = {}
    counts: Counter[str] = Counter()

    for idx, h in enumerate(hits):
        ent = h.get("entity", {}) or {}
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

    ordered_titles = sorted(
        doc_scores.keys(),
        key=lambda t: doc_scores[t],
        reverse=True,
    )

    return ordered_titles[:k]


def _map_doc_to_info(hits: list, wanted_titles: list[str]) -> dict[str, dict]:
    """
    Creates a dictionary mapping the k top documents to their paths and UUIDs.
    Returns {title: {"path": path, "uuid": uuid}}
    """
    out = {t: None for t in wanted_titles}
    wanted = set(wanted_titles)
    for h in hits:
        ent = h.get("entity", {}) or {}
        t = ent.get(TITLE_FIELD) or "Untitled"
        if t in wanted and out[t] is None:
            p = ent.get(PATH_FIELD)
            u = ent.get(FILE_UUID_FIELD)
            if p:
                out[t] = {"path": p, "uuid": u}
                if all(out[v] is not None for v in wanted_titles):
                    break
    return {t: info for t, info in out.items() if info}

def _read_file(path: str) -> str:
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
    qvec = _embed_query(question)

    hits = _milvus_search(
        qvec, top_k=top_n_chunks,
        output_fields=[TITLE_FIELD, PATH_FIELD, TEXT_FIELD, FILE_UUID_FIELD],
        kb_name=kb_name,
    )

    file_counts = Counter(
        hit.get("entity", {}).get(TITLE_FIELD, "unknown")
        for hit in hits if "entity" in hit
    )

    print("Top 10 hits:")
    for i, h in enumerate(hits[:10]):
        ent = h.get("entity", {}) or {}
        title = ent.get(TITLE_FIELD, "unknown")
        print(f"{i + 1}: {title}")
    
    print("Chunk counts by file (top {top_n_chunks}):")
    for title, count in file_counts.most_common():
        print(f"{count:2d}  {title}")

    top_docs = _select_topk_docs_weighted(
        hits,
        k=top_k_docs,
        alpha=0.75,
        top_n_chunks=top_n_chunks,
    )
    print("[diag] top_docs:", top_docs)

    doc_infos = _map_doc_to_info(hits, top_docs)
    print("[diag] doc_infos:", doc_infos)
    context = _build_full_doc_context_from_paths(doc_infos, budget_tokens=ctx_budget_tokens, kb_name=kb_name)
    if not context:
        return "Insufficient context to answer from the knowledge base."

    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
    print(f"QA context loaded: {qa_context}")
    
    instructions = (
        "Output Rules:\n"
        "1. Full sentences.\n"
        "2. When citing a document, use standard markdown link format: `[Title](Link)` using the Link provided in the context header.\n"
        "3. DO NOT use brackets like 【Title】. ONLY use `[Title](Link)`.\n"
        "4. Example: 'The Titanic was found in 1985 [Titanic.txt](/kbs/my_kb/docs/uuid/view)'.\n"
        "5. This ensures the citation is clearly visible as linked text.\n"
        "6. Use LaTeX for all mathematical expressions.\n"
        "7. Use `$$` delimiters for display math (separate lines).\n"
        "8. Use `$` delimiters for inline math."
    )
    
    if qa_context:
        user_msg = (
            f"Context (authoritative; cite using Markdown links [Title](Link)):\n{context}\n\n"
            f"QA Context:\n{qa_context}\n\n"
            f"{instructions}\n"
            f"Question:\n{question}\n\n"
        )
    else:
        user_msg = (
            f"Context (authoritative; cite using Markdown links [Title](Link)):\n{context}\n\n"
            f"{instructions}\n"
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
    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

    qvec = _embed_query(question)

    hits = _milvus_search(
        qvec, top_k=top_n_chunks,
        output_fields=[TITLE_FIELD, PATH_FIELD, TEXT_FIELD, FILE_UUID_FIELD],
        kb_name=kb_name,
    )

    top_docs = _select_topk_docs_weighted(
        hits,
        k=top_k_docs,
        alpha=alpha,
        top_n_chunks=top_n_chunks,
    )
    print("[diag] top_docs:", top_docs)

    doc_infos = {}
    wanted = set(top_docs)
    for h in hits:
        ent = h.get("entity", {}) or {}
        t = ent.get(TITLE_FIELD) or "Untitled"
        if t in wanted and t not in doc_infos:
            p = ent.get(PATH_FIELD)
            u = ent.get(FILE_UUID_FIELD)
            if p:
                doc_infos[t] = {"path": p, "uuid": u}
                if len(doc_infos) == len(top_docs):
                    break

    print("[diag] doc_infos:", doc_infos)

    context = _build_full_doc_context_from_paths(
        doc_infos,
        budget_tokens=ctx_budget_tokens,
        kb_name=kb_name
    )

    if not context:
        msg = "Insufficient context to answer from the knowledge base."
        yield f"data: {json.dumps({'choices':[{'delta':{'content': msg}}]})}\n\n"
        return

    instructions = (
        "Output Rules:\n"
        "1. Full sentences.\n"
        "2. When citing a document, use standard markdown link format: `[Title](Link)` using the Link provided in the context header.\n"
        "3. DO NOT use brackets like 【Title】. ONLY use `[Title](Link)`.\n"
        "4. Example: 'The Titanic was found in 1985 [Titanic.txt](/kbs/my_kb/docs/uuid/view)'.\n"
        "5. This ensures the citation is clearly visible as linked text.\n"
        "6. Use LaTeX for all mathematical expressions.\n"
        "7. Use `$$` delimiters for display math (separate lines).\n"
        "8. Use `$` delimiters for inline math."
    )

    user_msg = (
        f"Context (authoritative; cite using Markdown links [Title](Link)):\n{context}\n\n"
        f"{instructions}\n"
        f"Question:\n{question}\n\n"
    )

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
