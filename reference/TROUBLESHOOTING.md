# Troubleshooting the course

Start with the failing boundary and observed values, not random prompt changes. Use [the API map](API_MAP.md) to locate a component and [the verification report](../docs/VERIFICATION.md) to separate exercised paths from unverified live behavior.

## Observed environment issues during implementation

### Package download host does not resolve

The initial PyPI-backed `uv lock` timed out fetching wheel metadata from `files.pythonhosted.org`; an IPv4 header diagnostic also timed out during DNS resolution. This was a connectivity problem, not evidence of an incompatible LangChain dependency graph.

The Tsinghua TUNA mirror was reachable. Resolution and installation succeeded there; `pyproject.toml` declares that default index and `uv.lock` records its artifact URLs and hashes. Normal course commands therefore use `uv sync --locked` without silently changing indexes on every run.

If your network can use PyPI and you prefer it, deliberately re-resolve with your chosen index configuration, review the resulting versions/hash sources, then re-exercise the course. Do not hand-edit lockfile URLs or disable certificate verification. Choosing a new index can change the environment; it is not a pass/fail workaround for application tests.

### Provider configuration is absent

No OpenAI, Anthropic, Google, or LangSmith credential was configured in the implementation session; no model ID was selected and no local Ollama executable was installed. Model-free local paths remain meaningful: schemas, catalog tools, retrieval permissions, actual graphs, persistence, local action records, HTTP, and MCP can be investigated without claiming generated-model evidence.

For a live run, configure `.env` from `.env.example`, choose an accessible model and budget, and set `COURSE_ALLOW_LIVE=1` only after consent. Semantic retrieval additionally needs `COURSE_EMBEDDING_MODEL`. `--live` must fail explicitly if required configuration is missing; never add a fake answer or silent fallback to make it appear successful.

### Gateway generation works but JSON-schema output fails

The actual OpenAI-Codex gateway returned natural text or an invalid enum on JSON-schema requests; tool/function-calling paths succeeded. A credential and successful text response do not establish every capability. Keep validation strict and select a compatible endpoint/model privately; do not repair output into fake success. SDK parsing may raise before an `include_raw` envelope exists. The HTTP service reports generated-output failures as `502 / ModelOutputError`, not malformed caller input. Embeddings separately need a real accessible embedding model.

### Advisor review is waived

The user explicitly skipped advisor review and disabled its session-only setting. No sign-off is claimed and no replacement review is required.

## Boundary-oriented diagnosis for learner experiments

The following are investigative procedures, not claims that every listed failure occurred during implementation.

| Symptom | Inspect first | Corrective action |
|---|---|---|
| `import langchain` finds course code | `langchain.__file__`, interpreter, project distribution name | The course is `langchain_learning`; synchronize the locked environment and select the same IDE interpreter. |
| Live request exits before contacting a provider | Key/model/consent booleans from preflight | Supply missing configuration privately; do not print keys or bypass consent. |
| Authentication/404/capability error from provider | Endpoint/model access and provider error class | Verify the account/model and documented feature support. Schema prompting does not create missing native capabilities. |
| Structured output parses but is false | Source/input evidence and semantic rubric | Separate shape validation from factual support; abstain or correct the evidence/prompt based on a diagnosed cause. |
| Agent does not use a tool | Tool description/schema, requested calls, actual result messages | Inspect the real conversation/trace; a tool-call request is not execution proof. |
| Quote total is wrong or quantity fails | Catalog stock and integer-cent arithmetic | Fix the input or deterministic calculation; avoid arbitrary expression evaluation. |
| Retrieval misses a paraphrase | Actual retrieved passages, lexical versus semantic strategy | Measure the miss; configure real semantic embeddings for that comparison rather than renaming lexical vectors “semantic.” |
| Old document appears | Source ID/current/version metadata and index rebuild | Rebuild from the changed corpus; do not leave old duplicate chunks active. |
| Citation exists but does not support claim | Claim-to-passage mapping | Review semantic support, not only source-ID membership. |
| Resume cannot find pending state | Same state directory, thread ID, stored owner, checkpoint status | Select the original owned thread; in-memory checkpoints cannot recover across processes. |
| Another user can inspect/resume | Authentication binding and persisted thread ownership | Deny at execution/data boundaries, independently of model instructions. |
| Repeated decision conflicts | Existing persisted terminal decision/action | Matching retry is idempotent; a different terminal decision is not a new request. Use a fresh thread for a new proposal. |
| Client disconnects/deadline expires | Server request outcome and persisted thread/action | Cancellation may occur after commit. Inspect before retry; do not assume rollback or external exactly-once delivery. |
| MCP call fails | Script path, process stderr, adapter lifecycle and transport | Fix the actual connection/tool schema; a connected server is not automatically trusted. |
| Evaluation looks too good | Dataset split, frozen configuration, per-case checks and human support review | Remove leakage and weak citation-only scoring; disclose small-sample/stochastic limits. |

## Safe resets

Use a fresh `COURSE_STATE_DIR` for disposable experiments. Stop the server/workflow before removing any local database directory. Keep synthetic fixture sources separate from generated state. Do not delete a persistence directory to hide a failed replay/ownership investigation; capture evidence and diagnose the cause first.

**Sources:** [uv indexes](https://docs.astral.sh/uv/concepts/indexes/), [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts), [evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts).
