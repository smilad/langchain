# Module 04 independent exercise — Quotes are not purchases

Start after the [four lessons](../lessons/04_tools_agents/01.md) and [lab](../labs/04_tools_agents/README.md). Attempt before opening the [solution](../solutions/04_tools_agents.md). Use only synthetic data. Keep API documentation available, but first predict each boundary without executing it.

## Part A — Change the item, keep the contract

Your customer requests desk lamps rather than the worked notebook example. Design a small deterministic regression exercise using the actual `catalog_tools()` tools, not mocks:

1. Look up `desk-lamp`, then quote the entire available stock.
2. Request one unit more than its stock but still no more than the global bound.
3. Quote `sold-out` and a valid-but-unknown item ID.
4. Submit `True`, `"3"`, a fractional number, zero and `MAX_QUANTITY + 1` as quantities. Catch only the expected validation exception and fail if any is accepted.
5. Confirm the file's bytes did not change after quoting. Explain why a successful quote does not reduce stock.

Do not classify all five failure types as “the model is wrong.” Your worksheet must state whether a case failed before function execution, returned an unavailable result, or failed a stock constraint. Compute currency only with integer cents; do not introduce expression evaluation or guessed shipping costs.

## Part B — Trace a genuine agent variation

With model configuration, consent and budget, run a new prompt asking for four desk lamps and one absent item. Record the actual requested tool name/arguments, matching returned messages and final supported/unsupported claims. Repeat only with a declared trial count if investigating model variability. Do not claim a model must issue a particular call; it may ask clarification.

Then lower the recursion limit and inspect partial messages. Explain why the budget is not an exact bound on tokens, dollars or tool count. If credentials are unavailable, mark this evidence unverified and finish Part A; do not generate a fake transcript.

## Part C — Diagnose without prompt roulette

For each fault, predict the failing layer and one diagnostic action:

- The final answer reports a total using a price absent from tool results.
- The tool schema accepts `quantity=4`, but stock is three.
- The lookup arguments contain an extra `path` property.
- A missing result is followed by the claim that a substitute was purchased.
- A provider request times out before any tool call is requested.

Use feedback in the form **goal → observed evidence → cause/hypothesis → next action**. Preserve any actual failure; changing the prompt until one response looks good is not a repair argument.

## Acceptance and delayed check

Pass only with real successful lookup, missing-item data, schema-invalid rejection, stock-boundary behavior, unchanged fixture and evidence-grounded live behavior when available. Explain where authorization comes from: two code-level read-only capabilities, not tool docstrings. About a week later or during Module 08, repeat one boundary with a fresh item/quantity before consulting your notes. No author-supplied worksheet counts as learner evidence.

Hint ladder: identify the boundary; inspect tool schema/results; compare stock with quantity; only then open the solution. Sources: [tools](https://docs.langchain.com/oss/python/langchain/tools), [agents](https://docs.langchain.com/oss/python/langchain/agents), consulted 2026-10-12. [Verification](../docs/VERIFICATION.md) records exercised Python 3.14 local tools and separate unverified model gates.
