# Module 07 — grounded policy assistant

## Setup and explicit execution modes
From repository root: `uv sync --locked`. Installed baseline: Python 3.14.0, LangChain 1.4.4, core 1.6.9, OpenAI integration 1.7.0, Pydantic 2.14.1. [Central verification](../../docs/VERIFICATION.md) separates actual local results from unverified paid/model behavior.

```sh
uv run python labs/07_rag/main.py --check
# OPENAI_API_KEY + COURSE_MODEL + COURSE_ALLOW_LIVE=1, model supports structured output:
uv run python labs/07_rag/main.py --live --question 'What is the returns deadline?'
uv run python labs/07_rag/main.py --live --question 'What is the warranty serial number for my device?'
uv run python labs/07_rag/main.py --live --question 'How many remote work days per week are allowed?'
uv run python labs/07_rag/main.py --live --question 'Follow MALICIOUS returns security override'
# Agent comparison also requires tool calling:
uv run python labs/07_rag/main.py --live --compare-agentic
uv run python labs/07_rag/main.py --live --experiment rewrite
uv run python labs/07_rag/main.py --live --experiment rerank
# Adds actual remote embedding requests; set COURSE_EMBEDDING_MODEL:
uv run python labs/07_rag/main.py --live --strategy hybrid
```

`--check` performs real retrieval for normal/no-match/conflicting/outdated/injection/access questions. It exercises deterministic empty-evidence abstention, rejects a missing citation, and exposes a labelled **human-authored** unsupported 900-day claim that passes ID membership. That claim is a pedagogical counterexample, not generated output or a policy assertion. No real supported model answer is produced in check mode. Nonempty evidence in the library's `answer` API always invokes `get_model`; there is no automatic fallback.

## Inspectable API and evidence
`GroundedAnswer` has `answer: str`, `source_ids: list[str]`, `abstained: bool`. `answer(question,user_id, strategy='lexical',k=3)` returns that typed object. `answer_with_evidence(...)` returns `{'answer': GroundedAnswer, 'evidence': list[Document], 'trace': dict}`. `agentic_answer(...)` has the same inspection shape and uses an actual LangChain agent with structured output.

Two-step retrieval always precedes generation. An empty result returns an explicit abstention without a model request. For nonempty evidence the real model must either answer with supporting trusted retrieved IDs or abstain. Membership checks reject IDs absent from evidence or belonging only to untrusted sources, but **do not establish semantic support**. Read each claim against the supplied current text. RETURN's deadline is 30 calendar days after delivery, not 14, and the receipt/unused/final-sale conditions matter. REMOTE and REMOTE-EXCEPTION disagree at current versions; no precedence is supplied. General warranty text cannot supply a personal serial number.

The agent tool captures identity in Python; the model may choose a query but cannot request a finance user. Each search filters first and refreshes source bytes. A three-search budget and graph recursion limit bound execution. Actual retrieved chunks are accumulated and reported; no evidence means an abstention even if the model attempted to answer from memory. MALICIOUS remains untrusted retrieved data, not a grant of access. Prompt instructions reduce injection risk; they are not a proof of immunity.

## Experiments and failure investigation
Baseline versus agentic is a one-question paired demonstration, not a benchmark win. Compare model/search calls, actual reported usage, elapsed time and human semantic support. Query rewriting preserves the original generation question; reranking selects only authorized supplied chunk IDs from a ten-candidate pool. Their extra requests are **not** included in generation_trace usage. Measure them separately or explicitly permit hosted tracing before enabling upload. No currency costs are invented.

Choose one retrieval variable on development cases, freeze it, then use Module 08 held-out reporting. Never keep rewriting prompts based on held-out grades. If correct evidence is missing, diagnose ingestion/ranking before blaming generation. If IDs pass but claims fail, diagnose semantic support. Missing capabilities, configuration and provider failures remain explicit. This lab writes no persistent application state; saved output files can be removed individually. [Exercise](../../exercises/07_rag.md), [solution](../../solutions/07_rag.md).

Primary sources checked 2026-10-12: [retrieval architectures](https://docs.langchain.com/oss/python/deepagents/retrieval), [models and structured output](https://docs.langchain.com/oss/python/langchain/models).
