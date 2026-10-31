"""Policy ingestion and retrieval; lexical is a real local baseline, not embeddings."""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import re

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict

from langchain_learning.runtime import DATA, load_environment

USERS = {"alice": {"public"}, "bob": {"public"}, "finance": {"public", "finance"}}
STOPWORDS = set("a an the is are was were do does how what when where can i my me to of for and or in on with please tell about policy policies".split())


def authorize(user_id: str) -> set[str]:
    """Identity must come from the authenticated caller, not generated tool arguments."""
    if user_id not in USERS:
        raise PermissionError("Unknown policy user")
    return USERS[user_id]


def terms(text: str) -> Counter[str]:
    return Counter(t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS)


def chunk_text(text: str, *, size: int = 700, overlap: int = 80) -> list[str]:
    """Small transparent character splitter; prefer a sentence break near the limit."""
    if size < 100 or not 0 <= overlap < size // 2:
        raise ValueError("Invalid chunk size/overlap")
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = text.rfind(". ", start + size // 2, end)
            if boundary != -1:
                end = boundary + 1
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = end - overlap
    return chunks


class PolicyIndex:
    """Reload sources before each search; atomically replace, never append stale chunks.

    Semantic stores are scoped to authorized current documents *before* embedding or
    ranking. The course corpus is synthetic; do not upload real confidential policies.
    """

    def __init__(self, strategy: str = "lexical", *, directory: Path | None = None,
                 chunk_size: int = 700, overlap: int = 80):
        if strategy not in {"lexical", "semantic", "hybrid"}:
            raise ValueError("Strategy must be lexical, semantic or hybrid")
        self.strategy = strategy
        self.directory = directory or DATA / "policies"
        self.chunk_size, self.overlap = chunk_size, overlap
        self.documents: list[Document] = []
        self.fingerprint = ""
        self._stores: dict[str, object] = {}
        self.refresh()

    def refresh(self) -> bool:
        files = sorted(self.directory.glob("*.json"))
        if not files:
            raise ValueError("No policy source files")
        payloads = [(p.name, p.read_bytes()) for p in files]
        fingerprint = sha256(b"".join(n.encode() + b"\0" + b for n, b in payloads)).hexdigest()
        if fingerprint == self.fingerprint:
            return False
        documents, active, versions = [], set(), set()
        for name, payload in payloads:
            record = json.loads(payload)
            required = {"source_id", "version", "audience", "current", "title", "text", "provenance", "trust"}
            if not required <= record.keys():
                raise ValueError(f"Missing policy metadata in {name}")
            if (not isinstance(record["source_id"], str) or not record["source_id"]
                    or type(record["version"]) is not int or record["version"] < 1
                    or type(record["current"]) is not bool
                    or record["audience"] not in {"public", "finance"}
                    or record["trust"] not in {"policy", "untrusted"}
                    or not isinstance(record["text"], str) or not record["text"].strip()):
                raise ValueError(f"Invalid policy record in {name}")
            key = (record["source_id"], record["version"])
            if key in versions or record["current"] and record["source_id"] in active:
                raise ValueError("Duplicate policy version/current source")
            versions.add(key)
            if record["current"]:
                active.add(record["source_id"])
            metadata = {k: v for k, v in record.items() if k != "text"}
            metadata["path"] = name
            metadata["content_sha256"] = sha256(record["text"].encode()).hexdigest()
            for ordinal, chunk in enumerate(chunk_text(record["text"], size=self.chunk_size, overlap=self.overlap)):
                chunk_id = f"{record['source_id']}:v{record['version']}:{ordinal}"
                documents.append(Document(id=chunk_id, page_content=chunk,
                                          metadata={**metadata, "chunk_id": chunk_id, "chunk": ordinal}))
        self.documents, self.fingerprint = documents, fingerprint
        self._stores.clear()
        return True

    def authorized_documents(self, user_id: str) -> list[Document]:
        audiences = authorize(user_id)
        self.refresh()
        return [d for d in self.documents if d.metadata["current"] and d.metadata["audience"] in audiences]

    @staticmethod
    def _lexical(query: str, documents: list[Document], k: int) -> list[Document]:
        """Cosine TF-IDF over authorized documents only; no synonym understanding."""
        query_terms = terms(query)
        counts = [terms(d.metadata["title"] + " " + d.page_content) for d in documents]
        df = Counter(t for c in counts for t in c)
        idf = {t: math.log((1 + len(counts)) / (1 + n)) + 1 for t, n in df.items()}
        q = {t: n * idf[t] for t, n in query_terms.items() if t in idf}
        qnorm = math.sqrt(sum(v * v for v in q.values()))
        if not qnorm:
            return []
        ranked = []
        for doc, count in zip(documents, counts):
            vector = {t: n * idf[t] for t, n in count.items()}
            norm = math.sqrt(sum(v * v for v in vector.values()))
            score = sum(v * vector.get(t, 0) for t, v in q.items()) / (qnorm * norm) if norm else 0
            if score > 0:
                ranked.append((score, doc))
        ranked.sort(key=lambda pair: (-pair[0], pair[1].id))
        return [doc.model_copy(deep=True) for _, doc in ranked[:k]]

    def _semantic(self, query: str, user_id: str, documents: list[Document], k: int) -> list[Document]:
        from langchain_core.vectorstores import InMemoryVectorStore
        from langchain_openai import OpenAIEmbeddings
        load_environment()
        if os.getenv("COURSE_ALLOW_LIVE") != "1" or not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Semantic search requires live consent and OPENAI_API_KEY")
        embedding_model = os.getenv("COURSE_EMBEDDING_MODEL")
        if not embedding_model:
            raise ValueError("Set COURSE_EMBEDDING_MODEL to an available OpenAI embedding model")
        cache_key = user_id + ":" + embedding_model
        if cache_key not in self._stores:
            store = InMemoryVectorStore(OpenAIEmbeddings(model=embedding_model, request_timeout=30,
                                                        max_retries=1))
            store.add_documents(documents)
            self._stores[cache_key] = store
        retriever = self._stores[cache_key].as_retriever(search_kwargs={"k": k})
        return [d.model_copy(deep=True) for d in retriever.invoke(query)]

    def search(self, query: str, user_id: str, *, k: int = 3) -> list[Document]:
        documents = self.authorized_documents(user_id)  # before ranking, embedding, or provider call
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Question must be nonempty")
        if type(k) is not int or not 1 <= k <= 10:
            raise ValueError("k must be between 1 and 10")
        if self.strategy == "lexical":
            return self._lexical(query, documents, k)
        semantic = self._semantic(query, user_id, documents, k)
        if self.strategy == "semantic":
            return semantic
        lexical = self._lexical(query, documents, k)
        scores, by_id = Counter(), {}
        for ranking in (lexical, semantic):
            for rank, doc in enumerate(ranking, 1):
                scores[doc.id] += 1 / (60 + rank)
                by_id[doc.id] = doc
        return [by_id[key] for key in sorted(scores, key=lambda key: (-scores[key], key))[:k]]

    def as_retriever(self, user_id: str, *, k: int = 3) -> PolicyRetriever:
        authorize(user_id)
        return PolicyRetriever(index=self, user_id=user_id, k=k)


class PolicyRetriever(BaseRetriever):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    index: PolicyIndex
    user_id: str
    k: int = 3

    def _get_relevant_documents(self, query: str, *, run_manager) -> list[Document]:
        return self.index.search(query, self.user_id, k=self.k)
