# Module 05 lab — Thread state, explicit preference and visible context

## Setup and local path

Prerequisites: Module 04 and [memory lesson 01](../../lessons/05_memory_context/01.md). From the repository root:

```text
uv sync --locked
uv run python labs/05_memory_context/main.py --check
```

Default behavior is `--check`. It uses a real `StateGraph`, `MessagesState`, `InMemorySaver`, `InMemoryStore`, and `trim_messages`; no fake chat model or canned generated answer exists. The graph accumulates actual human messages and selects a preference from the real store. This local path passed; `uv.lock`, preflight, and the centralized [verification record](../../docs/VERIFICATION.md) identify exercised versions, outcomes, and unverified live gates.

## What the deterministic path demonstrates

- Alice's same-thread messages accumulate; Bob's separate thread contains only Bob input.
- A new Alice thread has no Alice-shopping history but selects Alice's explicitly consented short-style preference.
- Bob's preference selection remains empty; his attempt to access an owned Alice thread is rejected before graph access.
- A graph reconstructed against the same saver retains checkpoints; a new in-memory saver does not. This is not process-restart durability.
- Consent-free preference writes fail. Store deletion works, but a previous checkpoint retains the preference snapshot selected at that time.
- A long unrelated human message causes approximate-budget trimming to retain only the latest complete request. Full, trimmed and **human-authored** summary contexts are printed and labelled.
- A real local catalog quote demonstrates that memory state and deterministic current facts remain separate.

The `Sessions` ownership dictionary is a single-process teaching guard, not authentication, concurrent service isolation or a durable ownership registry. Synthetic caller IDs are selected by application code. Never expose the underlying graph directly to arbitrary callers.

## Real memory and summarization path

Configure `OPENAI_API_KEY`, a tool-capable `COURSE_MODEL` and explicit `COURSE_ALLOW_LIVE=1` as described in Module 00. This run makes multiple model calls, including one summarization call and three context-comparison agents; agree to their cost before starting.

```text
uv run python labs/05_memory_context/main.py --live
```

The real `create_agent` receives a checkpointer, store and `SessionContext`. Dynamic prompt middleware reads only the exact user's response-style namespace and emits the actual supplied system context. Four conversations/turns establish Alice's temporary 3000-cent shopping budget, follow up in the same thread, inspect Bob's absent budget and inspect a new Alice thread. Every run streams intermediate model/tool messages.

Then the program supplies the same follow-up to three fresh real catalog agents: full history, approximate-budget trimmed history and a real model-generated summary plus question. Fresh agents prevent hidden checkpoint memory from contaminating the comparison. Input messages and summary input/output are printed for review. Generated summary accuracy, remembered budget, tool-supported totals and final abstentions require semantic human review; message counts alone do not establish them.

## Retention, reset and caveats

All state is held in process memory. Ending the process releases these local objects; no `.course` database is created by this lab. Do not confuse that with deletion of provider/optional hosted-trace records. Trimming selects a request copy, not stored-history erasure. Long-term describes cross-thread store scope here, not restart durability. Preference deletion does not erase old checkpoint snapshots.

The token counter is approximate and does not guarantee fit for every provider. Complete tool-call/result pairing must survive selection. Summaries can omit facts, introduce mistakes or carry untrusted instructions; they cannot grant permission. Use synthetic data only and do not upload traces without considering consent/retention.

Complete the [exercise](../../exercises/05_memory_context.md) before opening the [solution](../../solutions/05_memory_context.md). No live run or learner mastery is claimed when model credentials/consent are unavailable. Sources consulted 2026-10-12: [short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory), [long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory), [custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom).

## Captured `--check` output

Real, unedited stdout of `uv run python labs/05_memory_context/main.py --check` (no credentials, no network; local paths replaced by `<repo>`). Excerpt: first 150 lines only. Compare your own run against it.

```text
{
  "python": "3.14.0",
  "interpreter": "<repo>/.venv/bin/python",
  "packages": {
    "langchain": "1.4.4",
    "langchain-core": "1.6.9",
    "langchain-openai": "1.7.0",
    "langgraph": "1.2.14",
    "langgraph-checkpoint-sqlite": "3.1.1",
    "fastmcp": "4.1.0",
    "pydantic": "2.14.1"
  },
  "langchain_origin": "<repo>/.venv/lib/python3.14/site-packages/langchain/__init__.py",
  "configured": {
    "api_key": false,
    "model": false,
    "live_consent": false,
    "custom_endpoint": false,
    "hosted_tracing": false
  },
  "live_request_sent": false
}
{
  "alice_thread": {
    "messages": [
      {
        "content": "I prefer short replies.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "1454fc1a-40be-4ed0-8bf1-50d13b34dbda"
      },
      {
        "content": "Look up notebook.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "f2877c5a-5556-4a53-bccd-d0827521e25d"
      }
    ],
    "user_id": "alice",
    "selected_preference": {
      "style": "short"
    }
  },
  "bob_thread": {
    "messages": [
      {
        "content": "Look up desk-lamp.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "896ba4cd-2b16-4485-bad3-a1305bd5c346"
      }
    ],
    "user_id": "bob",
    "selected_preference": {}
  },
  "alice_other_thread": {
    "messages": [
      {
        "content": "A new conversation.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "a00b02f1-c924-48cf-be7a-4b4b28266255"
      }
    ],
    "user_id": "alice",
    "selected_preference": {
      "style": "short"
    }
  },
  "ownership": "Cross-user thread reuse rejected before graph access",
  "checkpoint_count": 6,
  "context_comparison": {
    "full": [
      {
        "content": "Synthetic preference: short replies. My old request concerned a notebook.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "early"
      },
      {
        "content": "Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. Unrelated historical discussion. ",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "irrelevant"
      },
      {
        "content": "Quote 2 notebooks; use fresh catalog facts.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "latest"
      }
    ],
    "trimmed": [
      {
        "content": "Quote 2 notebooks; use fresh catalog facts.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "latest"
      }
    ],
    "human_summarized": [
      {
        "content": "Human-authored summary, not model output: user requested short replies and considered notebook.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": null
      },
      {
        "content": "Quote 2 notebooks; use fresh catalog facts.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "latest"
      }
    ],
    "discarded_by_trim": [
      "early",
      "irrelevant"
    ]
  },
  "real_tool_result": {
    "found": true,
    "quoted": true,
    "item_id": "notebook",
    "quantity": 2,
    "unit_price_cents": 1299,
    "total_cents": 2598,
    "currency": "USD",
    "stock": 12
  }
}
```
