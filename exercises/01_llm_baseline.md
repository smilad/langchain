# Module 01 — trace and vary a direct model boundary

**Objective:** Explain the request path, separate deterministic contracts from model behavior, and diagnose a bad rubric versus transport failure. Prerequisite: Module 00 gate; [lessons](../lessons/01_llm_baseline/01.md), [runbook](../labs/01_llm_baseline/README.md). Attempt without an AI-written implementation. Live access is optional for reachable deterministic work but required for the live gate.

## Recall and prediction
Before opening the lab, name where application state lives, what a timeout means and what label validation proves. Predict the stage that rejects a string with valid JSON syntax but the wrong classification representation.

## Guided fading
Recreate `validate_label` with the three permitted labels after reading its contract, not its implementation. Test lowercase, whitespace, capitalization, a sentence, a JSON-shaped string and empty output. Do not count these authored fixtures as generated classifications.

Build a request diagram with explicit Python text, instructions, model ID, SDK client, HTTPS boundary, response object, text projection and consumer acceptance. Mark every deterministic versus model/provider-dependent stage. Add the location of secret authentication without printing its value.

## Independent variations
1. Choose a new synthetic input combining a payment and a software fault. Write an overlap policy before any model call, then revise the instructions intentionally to match it. Keep parser representation unchanged.
2. Define a four-category classifier in your own separate implementation. Update instruction rubric, accepted-label contract and consumer together; do not add a shim accepting obsolete labels.
3. Explain when the direct SDK is enough and identify one concrete future requirement that would justify LangChain. Do not claim either architecture is inherently more intelligent.
4. Write a comparison of character limits, token context and output budget. Show why this lab's 4000-character check is not a token-cost calculation.

## Failure investigation
For each case, state expected stage, evidence to inspect, likely cause and next action: missing model/key, absent consent, unavailable model, HTTP 429, timeout, non-completed response, unexpected output format, semantically wrong valid label. Do not make a paid request merely to provoke a transport failure. Configuration failure is safely reachable by using an unconfigured environment; do not print or erase another learner's credential file.

## Optional approved live evidence
Only after independently approving credentials/model/budget, run one unfamiliar synthetic text with `--live`. Record actual request, status/model, output envelope/text, elapsed time and usage when available. Distinguish reported tokens from any explicitly priced cost estimate. State trial count before comparing variability; one call does not establish reliability. Never copy illustrative documentation output as your own run.

## Exit and delayed transfer
Submit behavior, conceptual explanation, diagnosis and one independently changed constraint. If live access is unavailable, label live classification unverified and retain your reachable boundary evidence; do not use a fake model. Next session explain the deterministic boundary closed-note; roughly a week later construct a fresh direct request with documentation lookup. Revisit model state in Module 05 and measurements in Module 08.

[Solutions](../solutions/01_llm_baseline.md) explain diagnoses after an attempt. [Verification](../docs/VERIFICATION.md) separates implemented paths from exercised proof. No learner progress is prefilled.
