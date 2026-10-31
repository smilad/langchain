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

## Captured `--check` output

Output of `uv run python labs/09_graph_workflows/main.py --check` (no credentials, no network), re-formatted as indented JSON; local paths are replaced by `<repo>`. The environment `preflight` block is omitted here; Module 00 shows it in full. The middle of the output is omitted for length. Ids, timings and temporary paths will differ on your machine; the shape and the pass/fail results should match.

```text
{
  "routes": [
    {
      "question": "What is the return policy?",
      "updates": [
        {
          "classify": {
            "route": "supported",
            "events": [
              "classify:supported"
            ]
          }
        },
        {
          "constraints": {
            "events": [
              "constraint:read_only"
            ]
          }
        },
        {
          "retrieve": {
            "evidence": [],
            "events": [
              "retrieve"
            ]
          }
        },
        {
          "draft": {
            "draft": "Human routing exercise: review the retrieved policy before replying.",
            "draft_origin": "human",
            "status": "drafted",
            "events": [
              "draft"
            ]
          }
        }
      ],
      "state": {
        "question": "What is the return policy?",
        "user_id": "alice",
        "route": "supported",
        "evidence": [],
        "events": [
          "classify:supported",
          "constraint:read_only",
          "retrieve",
          "draft"
        ],
        "draft": "Human routing exercise: review the retrieved policy before replying.",
        "draft_origin": "human",
        "status": "drafted"
      }
    },
    {
      "question": "Please escalate this request",
      "updates": [
        {
          "classify": {
            "route": "review",
            "events": [
              "classify:review"
            ]
          }
        },
        {
          "review": {
            "status": "human_review_required",
            "events": [
... (middle omitted for length) ...
        ],
        "status": "human_review_required"
      }
    },
    {
      "question": "Describe Saturn",
      "updates": [
        {
          "classify": {
            "route": "unsupported",
            "events": [
              "classify:unsupported"
            ]
          }
        },
        {
          "unsupported": {
            "status": "unsupported",
            "events": [
              "unsupported"
            ]
          }
        }
      ],
      "state": {
        "question": "Describe Saturn",
        "user_id": "alice",
        "route": "unsupported",
        "events": [
          "classify:unsupported",
          "unsupported"
        ],
        "status": "unsupported"
      }
    }
  ],
  "reducer_failure": "Actual parallel writes without reducer rejected",
  "termination_failure": "Actual nonterminating graph reached recursion limit",
  "live_gate": "Unverified: real model classification and grounded drafting require --live"
}
```
