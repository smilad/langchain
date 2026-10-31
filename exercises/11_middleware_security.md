# Independent exercise — attack the execution boundary

Prerequisites: [Module 11](../lessons/11_middleware_security/01.md). All secrets and records must stay synthetic. Attempt before reading [the solution](../solutions/11_middleware_security.md).

1. Run `uv run python labs/11_middleware_security/main.py --check`. Separate the unsafe non-model counterexample, real corpus retrieval, actual authorization denials and zero sink effects in your report. Which checks do not exercise middleware through a model?
2. Construct a fresh untrusted document claiming a different authority and asking alice to inspect bob's thread or approve alice's proposal. Change wording, not actual caller context. Predict the permission outcome before invoking the boundary. Explain why prompt phrasing cannot grant absent capabilities.
3. Call `authorize_call` directly with authenticated SecurityContext for alice: owned thread allowed, bob thread denied, extra user_id denied, approval tool denied. This deliberately bypasses the agent. Show that middleware removal would not remove domain/workflow ownership enforcement.
4. Design one additional read-only status capability on paper. Specify schema, runtime identity, ownership check and minimal return fields. Identify which fields must never reach a provider. Explain why final-answer redaction cannot repair an upstream disclosure.
5. With provider consent, declare a trial count before using `--live`. Record actual requested tools/arguments, handler execution/denial messages and final claims. If the model never attempted an unauthorized call, report unattempted attack—not observed middleware denial. Evaluate semantic answer contamination separately from zero unauthorized effects.
6. Produce a versioned proof statement: Python and locked package versions, model ID if used, prompt revision, corpus source IDs, trial count and residual risks. Do not publish keys, authentication tokens or full configuration dictionaries.

## Gate and review

Demonstrate untrusted content cannot change identity/capabilities, owner checks occur before data disclosure, extra model arguments cannot override context, and no actions commit. Explain least privilege, minimization and limits. A clean single model response is not injection immunity. Revisit with MCP tool descriptions in Module 13 and held-out adversarial cases in Module 15. Use the teaching guide's hint ladder; no invented learner record.
