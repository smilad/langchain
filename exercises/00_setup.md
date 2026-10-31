# Module 00 — prerequisite diagnostic and independent work

**Objective:** Decide which prerequisites you can actually demonstrate before a paid call. Start with [lessons](../lessons/00_setup/01.md) and the [lab runbook](../labs/00_setup/README.md), but attempt the diagnostic without an AI-written solution. Documentation lookup is allowed. Keep your evidence private/local until you decide to share; this repository contains no fictional learning record.

## First attempt: six diagnostic tasks
1. Write a typed function that accepts a JSON string describing `ticket_id` and `priority`, requires both fields, and reports malformed syntax and invalid records distinctly. Try a valid record, missing ID and an out-of-range priority. Explain what annotations guarantee.
2. Reproduce the locked environment from the root. Show the running interpreter and external `langchain` import origin. Select that interpreter in your IDE. Explain project metadata versus lockfile versus installed files.
3. Read an environment variable and report only whether it exists. Explain why putting a value into a printed dictionary or traceback can expose a secret. Use a harmless synthetic variable for the exercise.
4. Draw an HTTP request/response and classify timeout, 429 and a completed response containing an incorrect label. State what a timeout does *not* prove about server-side execution.
5. Define a Pydantic schema for your ticket. Interpret a field location/type for missing data and reject whitespace-only IDs. Explain nullable versus defaulted fields without guessing.
6. Write two coroutines with an explicit yielding point, gather their results, and distinguish execution order from result order. Identify why a blocking SDK call inside `async def` still blocks. Locate the application frame in one genuine validation traceback.

Do not score by confidence. Supply actual code/output, a teach-back, a failure diagnosis and a fresh input variation. Paid credentials are not necessary for any task.

## Guided fading
Read the lab's `read_request` and then close it. Recreate the JSON→schema boundary for the ticket domain, supplying the missing schema validation step yourself. Require integer priority 1–3; decide explicitly whether `"2"` should be accepted. Explain the policy before running it.

## Independent variation and failure investigation
Change the domain again to a stock reservation with a positive bounded quantity. Include an unknown key and a blank identifier. Predict the rejecting stage before execution. Diagnose a deliberately mismatched IDE interpreter without reinstalling all dependencies. Submit the hypothesis and the interpreter-path evidence that confirms or refutes it.

## Remediation, not a deadline
If tasks 1–3 are unfamiliar, pause paid/model work. Use the [Python tutorial](https://docs.python.org/3/tutorial/) to study functions/dictionaries, JSON/exceptions and virtual environments in separate sessions; implement a tiny file-reading utility between sessions. Then reassess with a new record schema, not the supplied solution. This can require substantial additional study beyond the suggested 3–5-hour setup module. For HTTP, Pydantic or async gaps, remediate that specific boundary before its dependent lab. Ask a coach for one hint at a time: stage → relevant trace/documentation → concept → smaller analogy → worked solution.

## Gate and delayed review
Gate: reproducible environment, external import origin, secret-safe missing-configuration reporting, and demonstrated Python boundaries. Next session repeat a changed JSON input from memory. Roughly a week later explain interpreter/lock/async without notes, using API docs only for coding. Adjust review timing after actual errors; do not record mastery merely because the check ran.

[Solutions](../solutions/00_setup.md) provide corrections after an attempt. Source/version limits follow the linked lessons; runtime proof is tracked in [verification](../docs/VERIFICATION.md).
