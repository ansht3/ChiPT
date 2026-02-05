
# milvus_utils.py
# Shared Milvus connection logic (adapted from ai_service/rag_api/milvus_connect.py)

import os
import time
import logging
from typing import List, Union, Dict
from dataclasses import dataclass

from pymilvus import (
    connections,
    Collection,
    MilvusClient,
    DataType,
    utility
)

logger = logging.getLogger(__name__)

# Constants (mirrored from config/main)
VEC_FIELD = "embedding"
TEXT_FIELD = "answer" # In cache service we retrieve answer, question is separate
TITLE_FIELD = "question"
DOCID_FIELD = "id"

@dataclass
class MilvusConnection:
    """Unified wrapper for both local and remote Milvus connections"""
    client: Union[MilvusClient, Collection]
    is_local: bool
    collection_name: str
    
    def __post_init__(self):
        """Ensure index exists after initialization"""
        if self.is_local:
            pass # Index creation handled on insert/init usually for Lite, or already compliant
    
    def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 30,
        output_fields: List[str] = None
    ) -> List:
        """Unified search interface"""
        if output_fields is None:
            output_fields = ["question", "answer"]
            
        if self.is_local:
            # MilvusClient API
            search_params = {
                "metric_type": "IP", # Inner Product for Cache (Cosine Sim on normalized)
                "params": {}
            }
            results = self.client.search(
                collection_name=self.collection_name,
                data=[query_embedding],
                limit=top_k,
                output_fields=output_fields,
                search_params=search_params
            )
            return results[0] if results else []
        else:
            # Collection API
            search_params = {
                "metric_type": "IP", 
                "params": {"nprobe": 10}
            }
            results = self.client.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=output_fields
            )
            return results[0] if results else []

    def insert(self, data: List[list]):
        """Unified insert interface"""
        if not data:
            return

        if self.is_local:
            # MilvusClient expects list of dicts for insert, but cache_service provides list of lists (columnar)
            # We need to convert columnar [questions, answers, embeddings] to row-based
            questions = data[0]
            answers = data[1]
            embeddings = data[2]
            
            rows = []
            for q, a, emb in zip(questions, answers, embeddings):
                rows.append({
                    "question": q,
                    "answer": a,
                    "embedding": emb
                })
                
            res = self.client.insert(
                collection_name=self.collection_name,
                data=rows
            )
            return res
        else:
            # Collection API expects list of lists (columnar)
            res = self.client.insert(
                data=data
            )
            self.client.flush()
            return res
            
    def flush(self, collection_name=None):
        if self.is_local:
            # MilvusClient doesn't strictly need flush generally but good practice if available? 
            # Actually MilvusClient doesn't expose flush() same way.
            pass
        else:
            self.client.flush()

    @property
    def num_entities(self):
        if self.is_local:
            # MilvusClient doesn't have num_entities property, need query or stats
            try:
                res = self.client.query(
                    collection_name=self.collection_name,
                    filter="id >= 0",
                    output_fields=["count(*)"]
                )
                # This might be slow for large DBs, but fine for cache
                # Actually count(*) support varies. Let's try simple stats if get_collection_stats exists
                stats = self.client.get_collection_stats(self.collection_name)
                return stats.get('row_count', 0)
            except:
                return 0
        else:
            return self.client.num_entities
