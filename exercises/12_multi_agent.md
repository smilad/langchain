# Module 12 exercises — justify the specialist

Read [the lessons](../lessons/12_multi_agent/01.md), [the comparison runbook](../labs/12_multi_agent/README.md), and [the source APIs](../src/langchain_learning/advanced.py). Attempt before [solutions](../solutions/12_multi_agent.md).

## 1. Choose an architecture deliberately

For the support draft, compare a single tool-using agent, router, handoff, and one delegated specialist. Identify context ownership, where identity is bound, and termination at every boundary. Explain why a skill loaded into one agent is not automatically another autonomous agent.

## 2. Inspect the local handoff boundary

Run `uv run python labs/12_multi_agent/main.py --check`. For each case, inspect request-scoped evidence IDs and the rejected outside-source fixture. This is authored schema/evidence validation, not a model-quality score. Explain which claims still require semantic review even after `validate_handoff` passes.

## 3. Declare a real comparison

With an accessible model, consent, and budget, run `--live --trials 2`. Count the total runs before starting (four cases × two patterns × two trials). Explain why alternating pattern order reduces one ordering bias without establishing a strong statistical result. Keep corpus, identity, evidence scope, and question fixed between patterns.

## 4. Interpret cost and failure evidence

Read model/tool call counts, nested boundary counts, reported usage, missing usage, elapsed time, and explicit failure categories. Logical call limits are not an exact monetary ceiling: retries and token lengths matter. A faster unsupported answer is not automatically a better architecture.

## 5. Investigate a specialist contract failure

Run the explicit `--live --fail-specialist` experiment only with real provider access. It corrupts the handoff after an actual specialist result; explain why this is fault injection, not evidence that the model naturally produced that defect. The boundary must stop that trial without pretending to deliver a successful replacement answer.

## 6. Make a retention decision

Apply the support/abstention/security rubric to actual outputs and justify retaining or rejecting the specialist. If no provider is available, publish only the local contract evidence and a planned comparison protocol. Do not invent latency/token/quality results.

**Gate:** explain an appropriate pattern, demonstrate a bounded invalid handoff, and justify complexity from measured results or explicitly leave that comparison unverified. Revisit with one changed corpus constraint in the capstone.
