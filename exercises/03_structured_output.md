# Module 03 — reject typed fiction and preserve unknowns

**Objective:** Deliver validated extraction or an explicit error/abstention and justify structured-output strategy/composition. Prerequisites: Module 02 and Pydantic validation; [lessons](../lessons/03_structured_output/01.md), [runbook](../labs/03_structured_output/README.md). Start with your own schema diagram before reading [solutions](../solutions/03_structured_output.md).

## Retrieval warm-up
Does valid JSON prove a fact? How does required nullable differ from a missing field? Which LCEL stage must retain the original source? Answer closed-note, then use documentation for code.

## Guided fading
Recreate a minimal version of SupportRecord with required nullable fields. Supply the missing cross-field rule: supported requires ID/category/quote; other statuses must not select an order. Parse authored JSON with PydanticOutputParser, then add a separate source guard. Never call authored JSON an API response.

Draw every edge of the live pipeline, labeling values as input dictionary, prompt value/messages, raw/parsed/error envelope, original source and validated record. Explain why the guard cannot run correctly if source text has been discarded.

## Independent domain change
Use synthetic booking requests with `BOOK-` followed by four digits, not the worked ORDER domain. Define complete, missing, contradictory and irrelevant cases. Migrate identifier pattern, instruction policy, schema consistency and source checks together. Every field remains required; missing facts are null, not guessed defaults. Introduce an evidence quote that is present in the source but does not contain the selected identifier, and reject it.

Add a deliberately contradictory input containing two distinct booking IDs. State the policy before running: do not pick the first, last or most convenient ID. If your domain permits multiple IDs, redesign the output as a list with its own evidence contract instead of quietly weakening this single-record schema.

## Failure investigation
Predict the failed boundary for missing input key, blank text, omitted required null, unsupported JSON Schema capability, invalid enum, unsupported cross-field combination, fabricated ID, fabricated quote and semantically wrong category. Demonstrate reachable deterministic cases with real validation/composition; do not create a fake model for unavailable live branches. Explain why automatic retries cannot recover an absent booking identifier.

## Optional approved live strategy comparison
Run one synthetic case with the model engine and inspect raw/parsed/parsing_error. If your model supports it, compare `json_schema` and `function_calling` explicitly. Then inspect an agent result's `structured_response` using a declared provider or tool strategy. Tool-strategy schema arguments are not business effects. Record actual messages, errors, trial count and missing capability branches; do not infer provider strategy solely from your requested option.

## Gate and delayed reassessment
Submit validated records or explicit unknown/contradiction/irrelevance/errors for fresh inputs, a strategy explanation, a source-boundary failure diagnosis and an independent domain variation. Human review still assesses relevance/category/eligibility; exact quote membership alone is not complete factual verification. Next session rebuild a two-stage local parser/source chain from memory. Next week reassess on a different nullable field, then revisit evidence checks in Modules 07–08.

[Verification](../docs/VERIFICATION.md) distinguishes implementation from actual execution; no claimed learner mastery is stored by these exercises.
