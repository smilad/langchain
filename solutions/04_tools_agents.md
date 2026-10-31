# Module 04 solution — Locate the boundary before repairing it

Read only after attempting the [exercise](../exercises/04_tools_agents.md). This explains reference behavior, not independent learner evidence. Actual Python 3.14 local tool checks passed; [verification](../docs/VERIFICATION.md) records exact versions and unverified live agent behavior. No invented model transcript is supplied.

## Part A: real stock and strict-input boundaries

The catalog gives `desk-lamp` stock three at 3499 USD cents. Quoting three computes 10497 cents. Quoting four is shape-valid (integer between one and twenty) but returns `quoted=false`, `reason="insufficient_stock"`. `sold-out` is found but has no sellable units. An unknown valid identifier returns `found=false`; it should not become a fabricated replacement.

This small regression exercise uses the real tool layer:

```python
from pydantic import ValidationError
from langchain_learning.catalog import MAX_QUANTITY, catalog_tools
from langchain_learning.runtime import DATA

lookup, quote = catalog_tools()
before = (DATA / "catalog.json").read_bytes()
item = lookup.invoke({"item_id": "desk-lamp"})
assert item["found"]
exact = quote.invoke({"item_id": "desk-lamp", "quantity": item["stock"]})
assert exact["quoted"]
assert exact["total_cents"] == item["stock"] * item["price_cents"]
over = quote.invoke({"item_id": "desk-lamp", "quantity": item["stock"] + 1})
assert not over["quoted"] and over["reason"] == "insufficient_stock"
assert not quote.invoke({"item_id": "sold-out", "quantity": 1})["quoted"]
assert not lookup.invoke({"item_id": "absent-item"})["found"]
for quantity in (True, "3", 2.5, 0, MAX_QUANTITY + 1):
    try:
        quote.invoke({"item_id": "desk-lamp", "quantity": quantity})
    except ValidationError:
        continue
    raise AssertionError("Invalid quantity accepted")
assert (DATA / "catalog.json").read_bytes() == before
```

`strict=True` is important: Python considers `bool` an `int` subclass, and non-strict validators can coerce strings/floats. Direct domain calls validate through the same Pydantic models, so exposing them through MCP does not remove the boundary. Missing items and stock shortages are explicit results; invalid argument shape is an exception before successful execution.

## Part B: bounded agent evidence

The committed lab already provides the four baseline live commands in its [runbook](../labs/04_tools_agents/README.md). For your changed prompt, keep a recursion limit and stream actual updates. Verify the requested call arguments, matched tool result and final claim. Do not accept “three items purchased” as a quote: the capability never performs purchasing.

There is no supplied model transcript because model outputs vary and no live run is claimed here. A tiny budget may exhaust before a tool result exists; the proper artifact is a partial trace plus budget failure, not canned final prose. The step limit does not count exact tools when the model requests multiple calls in one step.

## Part C: diagnosis reasoning

- Unsupported final price: generation/evidence mismatch. Compare final numerical claims with tool cents before changing prompts.
- Four units versus stock three: business constraint, not schema bug. Return shortage explicitly; do not increase stock to satisfy a request.
- Extra `path`: schema-invalid input; `extra="forbid"` rejects it. No caller-supplied path is opened.
- Missing item then purchase claim: unsupported generation plus impossible action. The tool surface has no purchase action; preserve the failure.
- Timeout before tools: transport/configuration issue. Inspect safe provider error and timeout settings, never print credentials.

The feedback contract is: *the answer must be tool-supported → the trace lacks that price/action → generation added unsupported claims → map claims to returned fields and rerun only after a targeted change*. A successful output by itself is not evidence that the boundary is correct.

Sources consulted 2026-10-12: [tools](https://docs.langchain.com/oss/python/langchain/tools), [agents](https://docs.langchain.com/oss/python/langchain/agents). Review with fresh inputs in Module 08 rather than memorizing the fixture's arithmetic.
