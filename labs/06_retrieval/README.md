# Module 06 — provenance-preserving retrieval

## Setup and commands
From the repository root, run `uv sync --locked`. Installed baseline is Python 3.14.0, LangChain 1.4.4, langchain-core 1.6.9 and langchain-openai 1.7.0; consult the lockfile and [central verification](../../docs/VERIFICATION.md) for actual exercised results rather than inferring them from installation.

```sh
uv run python labs/06_retrieval/main.py --check
uv run python labs/06_retrieval/main.py --check --query 'SHIP-42' --user bob
uv run python -m unittest discover -s labs/06_retrieval -p 'test_invariants.py'
# Requires a real OpenAI key, COURSE_ALLOW_LIVE=1 and COURSE_EMBEDDING_MODEL:
uv run python labs/06_retrieval/main.py --live --strategy semantic
uv run python labs/06_retrieval/main.py --live --strategy hybrid
```

`--check` (also the no-flag default) performs actual lexical TF-IDF retrieval, checks audience/current invariants, rejects an unknown identity, and edits a real source in a temporary copy. It does not call a model or claim semantic retrieval. `--live --strategy lexical` still performs lexical retrieval; the output explicitly states whether remote embedding ran. Choose semantic/hybrid to exercise OpenAIEmbeddings plus InMemoryVectorStore and its actual retriever interface.

No embedding model is hardcoded. Choose an available OpenAI embedding model in `COURSE_EMBEDDING_MODEL`. Semantic/hybrid search sends eligible synthetic policy text and queries remotely and may incur charges. Generation's `COURSE_MODEL` is not needed for this retrieval-only lab. Never copy private documents into this course corpus without a separate data/upload decision. There is no automatic hosted tracing setup.

## Inspect these cases before generating anything
- Returns: current RETURN v2 is 30 calendar days after delivery with receipt/unused conditions; old v1 remains inspectable but ineligible.
- Exact identifier: SHIP-42 is lexical-friendly; inspect SHIPPING.
- Paraphrase: “money back for dinner while travelling” tests vocabulary mismatch against MEAL. Nonempty retrieval is not itself success.
- No-match: “quasar lunar habitat” returns no lexical evidence; semantic top-k may still return irrelevant passages.
- Public finance query: FINANCE must not enter alice/bob candidates, even when its terms match exactly. The untrusted public MALICIOUS note may match; it does not confer permission.
- Source edit: the copied RETURN v2 becomes 37 days; the temporary index must expose changed text without a stale 30-day duplicate. Committed sources remain untouched.

Each returned Document carries source_id, version, audience, current, trust, provenance, content hash and chunk ID. Locate it in `data/policies`, explain each field's purpose, and distinguish a revision from a passage. Experiment with `PolicyIndex(chunk_size=200, overlap=40)` in a disposable corpus to observe boundaries rather than assuming tiny sources demonstrate splitting.

## Failure diagnosis, state and limits
Unknown users fail at code-level authorization. Duplicate active source IDs fail ingestion. Missing consent/key/embedding model is a prerequisite error, not a fake semantic success. Sources are re-read before search; changed snapshots replace the document list and invalidate identity-scoped vector stores. Semantic caches are process-local and rebuilding repeats embedding requests; no disk vector database is claimed. Temporary source copies are automatically removed. The lab writes no persistent index; an externally saved report is yours to remove by its exact chosen path.

Regression tests cover actual authorization, current-only source selection, source edit/deletion replacement, duplicate-active-source rejection and trusted citation membership. They do not mock a provider or prove semantic relevance. [Exercise](../../exercises/06_retrieval.md) and [solution](../../solutions/06_retrieval.md) explain the independent variation. Real live embedding evidence remains subject to credentials and the central verification report.

Primary references: [semantic search](https://docs.langchain.com/oss/python/langchain/knowledge-base), [InMemoryVectorStore](https://reference.langchain.com/python/langchain-core/vectorstores/in_memory/InMemoryVectorStore). Checked 2026-10-12.
