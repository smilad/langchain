# Module 09 — explicit graph workflows

Read [lesson 01](../../lessons/09_graph_workflows/01.md); environment setup: `uv sync --locked` from the repository root. Python >=3.14, exact dependency versions in [uv.lock](../../uv.lock). Official [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), checked 2026-10-12.

## Runnable commands

```sh
uv run python labs/09_graph_workflows/main.py --check
uv run python labs/09_graph_workflows/main.py --live --question 'What is the return policy?'
uv run python labs/09_graph_workflows/main.py --live --question 'Please escalate this request'
uv run python labs/09_graph_workflows/main.py --live --question 'Describe Saturn'
```

Check is the default. It executes actual LangGraph routes for return/support, escalation/review and unrelated/unsupported inputs, shows partial updates, checks both parallel reducer contributions, intentionally executes a missing-reducer graph and a nonterminating graph, and requires their actual exceptions. Retrieval uses the actual local policy corpus and identity filters. The deterministic draft is labeled human exercise text, never a generated answer.

Live uses runtime configuration `OPENAI_API_KEY`, `COURSE_MODEL`, `COURSE_ALLOW_LIVE=1` and calls a real structured classifier. A supported route then invokes real grounded RAG. Model routes may differ from fixture rules; record classification outcomes rather than silently forcing desired routes. Live RAG retrieves again internally; evidence displayed in the graph is an inspectable retrieval stage, not a claim of exact reused context.

## Gate and limits

Trace every node's reads/writes; run all routes; explain the fan-in barrier and reducer; identify the two actual graph faults; complete [the independent variation](../../exercises/09_graph_workflows.md). Validate source support separately from schema shape. Parallel event order is not a semantic priority guarantee. The graph has bounded recursion and no side-effecting tool.

**Evidence status:** [verification](../../docs/VERIFICATION.md) records actual local commands and outcomes separately from unavailable live proof. Installed baseline: Python 3.14.0, LangGraph 1.2.14, LangChain 1.4.4, langchain-openai 1.7.0, Pydantic 2.14.1. Live proof requires provider configuration, not a fake fallback. No learner progress is implied. This lab uses no persistent local state. [Solutions](../../solutions/09_graph_workflows.md).
