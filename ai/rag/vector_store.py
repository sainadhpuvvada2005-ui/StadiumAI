from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np
from openai import OpenAI


@dataclass(frozen=True)
class RetrievedDocument:
    text: str
    score: float


class FaissRAGStore:
    def __init__(self, api_key: str, index_path: Path, documents_path: Path, embedding_model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.index_path = index_path
        self.documents_path = documents_path
        self.embedding_model = embedding_model
        self.documents = documents_path.read_text(encoding="utf-8").split("\n---\n") if documents_path.exists() else []
        self.index = faiss.read_index(str(index_path)) if index_path.exists() else None

    def build(self, documents: list[str]) -> None:
        vectors = np.array([self._embed(doc) for doc in documents], dtype="float32")
        index = faiss.IndexFlatIP(vectors.shape[1])
        faiss.normalize_L2(vectors)
        index.add(vectors)
        faiss.write_index(index, str(self.index_path))
        self.documents_path.write_text("\n---\n".join(documents), encoding="utf-8")
        self.documents = documents
        self.index = index

    def search(self, query: str, limit: int = 5) -> list[RetrievedDocument]:
        if self.index is None or not self.documents:
            return []
        vector = np.array([self._embed(query)], dtype="float32")
        faiss.normalize_L2(vector)
        scores, indices = self.index.search(vector, limit)
        return [RetrievedDocument(text=self.documents[index], score=float(score)) for score, index in zip(scores[0], indices[0]) if index >= 0]

    def _embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(model=self.embedding_model, input=text)
        return response.data[0].embedding
