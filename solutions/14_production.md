# Module 14 solutions — visible failure beats fake availability

Attempt [the exercises](../exercises/14_production.md) first. The [runbook](../labs/14_production/README.md) supplies routes/configuration; [verification](../docs/VERIFICATION.md) supplies observed scope.

## 1. Reproducibility and readiness

Use the committed lockfile with the configured index and the required interpreter. `import langchain` must resolve to the external library, not the old course package. Presence booleans are safe operational configuration evidence; secret values are not. Health indicates the process responds; readiness checks required local resources. Neither proves a provider model is reachable or answers correctly. The labs require the source checkout because course data and lesson entry points live there.

## 2. HTTP evidence

The smoke starts a real localhost server and sends actual requests. It tests unauthenticated rejection, body identity rejection, cross-user denial, concurrent manual starts, owned persistence across server restart, repeat approval producing one local action, rejection producing none, actual disconnect, and bounded deadline handling. Inspect both response and state: status 200 alone is not approval or successful delivery.

## 3. Ownership

Bearer tokens map to synthetic users outside request bodies. A valid Alice token cannot operate on Bob's thread; body-provided `user_id` is rejected rather than trusted. Reopening a thread with the same owner returns its stored state instead of overwriting the question/draft. Public health is not an authenticated user-state endpoint. Private tokens must not appear in example outputs, logs, commits, or shared traces.

## 4. Cancellation and idempotency

Terminating work on disconnect/deadline limits further execution; it does not roll back an action already committed. Inspect the persistent thread/action before choosing a retry. Repeating the same terminal decision returns the existing result; changing a final approval into rejection is a conflict, not a harmless retry. A local unique action record proves local idempotency only; an external sender would need its own delivery/transaction contract.

## 5. Live permission boundary

Validate model configuration and consent before persisting a new model-driven thread, even if retrieval would return empty evidence. The regression arose because deterministic empty-evidence abstention bypassed the later model constructor; the fixed workflow checks live intent first. This is a permission boundary, not a special-case question or relaxed HTTP assertion. A real provider outage test requires credentials/consent and intentionally unreachable transport; missing configuration is a different failure.

## 6. Operations

The service is localhost-only with bounded workers/deadlines, POSIX locking, SQLite checkpoints/actions, and sanitized error categories. Cooperating requests serialize graph mutation against the local sink. The request-status registry is transient while workflow state is durable. Graceful shutdown stops workers and releases resources; inspect state before restart/replay. Document backup/restore/schema compatibility and test measured targets before proposing multi-host or public deployment. Do not infer cloud readiness from this lab.
