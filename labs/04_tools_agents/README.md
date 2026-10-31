# Module 04 lab — Project A: read-only catalog assistant

## Objective and setup

Meet the [Module 04 gate](../../ROADMAP.md#04--tools-and-a-first-agent--68-hours): inspect successful lookup, unavailable item, invalid input and bounded agent execution. Start with [lesson 01](../../lessons/04_tools_agents/01.md), complete Modules 00–03 and run from the repository root:

```text
uv sync --locked
uv run python labs/04_tools_agents/main.py --check
```

The default without flags also runs `--check`. It performs actual local data/tool/schema operations, not a fake model. This local path passed; exact versions are in `uv.lock` and preflight. Consult the centralized [verification record](../../docs/VERIFICATION.md) for exercised versions/outcomes and separate unverified live model gates.

## Local cases and contracts

| Case | Actual operation / expected contract |
|---|---|
| Notebook present | `lookup_item("notebook")`, quote 2; total equals integer price × quantity |
| Valid missing identifier | `invisible-widget` returns `found=false`; quote returns `item_unavailable` |
| Stock boundaries | 3 desk lamps quote; 4 fail with `insufficient_stock`; sold-out fails |
| Maximum quantity | 20 pen sets quote; 21 is schema-invalid |
| Invalid quantity | 0, -1, 21, boolean, fractional number and string are rejected |
| Invalid lookup shape | Path-like ID and additional `path` field are rejected |
| Read-only | Catalog bytes remain unchanged after operations |

The synthetic fixture is [`data/catalog.json`](../../data/catalog.json). USD prices are integer cents; no binary-float money calculation or arbitrary `eval` exists. Quantities are strict integers 1–20. Missing-item and stock outcomes are data, not transport exceptions. Quotes neither reserve inventory nor include tax/shipping or checkout.

## Real model cases

Copy the root `.env.example` to a local `.env` using your normal secret-management workflow. Set `OPENAI_API_KEY`, choose `COURSE_MODEL` with tool-call support and set `COURSE_ALLOW_LIVE=1` only after accepting remote transfer/charges. Never commit the key or emit model settings.

```text
uv run python labs/04_tools_agents/main.py --live --case normal
uv run python labs/04_tools_agents/main.py --live --case missing
uv run python labs/04_tools_agents/main.py --live --case invalid
uv run python labs/04_tools_agents/main.py --live --case bounded
```

Each command invokes a real `create_agent` and streams intermediate node updates. Trace `AIMessage.tool_calls`, requested arguments, matching `ToolMessage` results and the final claims. The normal/missing/invalid cases use recursion limit eight. The bounded case uses one and reports the outcome actually observed: exhausted or terminated. The limit bounds graph steps, not exact calls, cost or wall time. An exhausted normal case remains an error; the deliberately tiny-budget case prints the partial trace without fabricating a final answer.

The invalid live prompt may trigger a clarification rather than an invalid tool call. The deterministic check is the reproducible proof of schema rejection; do not force an LLM to make a particular mistake.

## Review, evidence and limitations

Create your own per-case worksheet only after running: input → requested call → executed function → result → final claim → failure category. No authored learner record or model transcript is supplied. Live gate remains unverified when credentials/model/consent are absent. Provider transport failures are errors, never an automatic fake fallback.

No durable lab state is written, so restarting resets agent state. To change the catalog, edit only your synthetic fixture and rerun checks; restore intended records before sharing results. The loader reloads records each operation. Study the [independent exercise](../../exercises/04_tools_agents.md) before the [solution](../../solutions/04_tools_agents.md). Source: [official tools](https://docs.langchain.com/oss/python/langchain/tools), [agents](https://docs.langchain.com/oss/python/langchain/agents), consulted 2026-10-12.

## Captured `--check` output

Real, unedited stdout of `uv run python labs/04_tools_agents/main.py --check` (no credentials, no network; local paths replaced by `<repo>`). Excerpt: first 150 lines only. Compare your own run against it.

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
  "tool_schemas": {
    "lookup_item": {
      "additionalProperties": false,
      "description": "Exact catalog identifier; no free-form expressions or filesystem paths.",
      "properties": {
        "item_id": {
          "maxLength": 40,
          "minLength": 1,
          "pattern": "^[a-z0-9][a-z0-9-]*$",
          "title": "Item Id",
          "type": "string"
        }
      },
      "required": [
        "item_id"
      ],
      "title": "LookupInput",
      "type": "object"
    },
    "quote_total": {
      "additionalProperties": false,
      "properties": {
        "item_id": {
          "maxLength": 40,
          "minLength": 1,
          "pattern": "^[a-z0-9][a-z0-9-]*$",
          "title": "Item Id",
          "type": "string"
        },
        "quantity": {
          "maximum": 20,
          "minimum": 1,
          "title": "Quantity",
          "type": "integer"
        }
      },
      "required": [
        "item_id",
        "quantity"
      ],
      "title": "QuoteInput",
      "type": "object"
    }
  }
}
{
  "normal": {
    "found": true,
    "item_id": "notebook",
    "name": "Recycled paper notebook",
    "price_cents": 1299,
    "currency": "USD",
    "stock": 12
  },
  "quote": {
    "found": true,
    "quoted": true,
    "item_id": "notebook",
    "quantity": 2,
    "unit_price_cents": 1299,
    "total_cents": 2598,
    "currency": "USD",
    "stock": 12
  },
  "missing": {
    "found": false,
    "item_id": "invisible-widget"
  },
  "missing_quote": {
    "found": false,
    "item_id": "invisible-widget",
    "quoted": false,
    "quantity": 1,
    "reason": "item_unavailable"
  },
  "stock_boundary": {
    "found": true,
    "quoted": true,
    "item_id": "desk-lamp",
    "quantity": 3,
    "unit_price_cents": 3499,
    "total_cents": 10497,
    "currency": "USD",
    "stock": 3
  },
  "over_stock": {
    "found": true,
    "quoted": false,
    "item_id": "desk-lamp",
    "quantity": 4,
    "stock": 3,
    "reason": "insufficient_stock"
  },
  "sold_out": {
    "found": true,
    "quoted": false,
    "item_id": "sold-out",
    "quantity": 1,
    "stock": 0,
    "reason": "insufficient_stock"
  },
  "max_quantity": {
    "found": true,
    "quoted": true,
    "item_id": "pen-set",
    "quantity": 20,
    "unit_price_cents": 599,
    "total_cents": 11980,
    "currency": "USD",
    "stock": 40
  },
  "invalid_arguments": [
    {
      "quantity": 0,
      "error_types": [
        "greater_than_equal"
      ]
    },
    {
      "quantity": -1,
      "error_types": [
        "greater_than_equal"
      ]
    },
    {
      "quantity": 21,
      "error_types": [
```
