# Module 14 exercises — operate the local application

Read [the lessons](../lessons/14_production/01.md) and [the HTTP runbook](../labs/14_production/README.md). Attempt before [solutions](../solutions/14_production.md). This is a localhost operations lab, not an internet-ready security certification.

## 1. Reproduce the environment

Start from a checkout with the locked Python environment, not IDE globals. Explain the configured package index and its hashes, configuration presence versus secret values, health versus readiness, and why the local corpus/state are not model weights.

## 2. Run actual HTTP behavior

Run `uv run python labs/14_production/main.py --check`. Inspect health, token authentication, concurrent Alice/Bob starts, user-ID body rejection, cross-user denial, disconnect outcome, process restart, repeat approval, rejection, and deadline response. Identify the corresponding persisted graph/action observations rather than relying on a happy-path HTTP status alone.

## 3. Serve and vary a request

Configure private synthetic bearer tokens mapped to Alice/Bob, launch `python -m langchain_learning.service`, and use the documented routes. Create a fresh human-draft thread, inspect it, edit/approve/reject explicitly, then restart and inspect. Try invalid credentials and another user's thread. Identity must come from the token, not a client body field.

## 4. Investigate cancellation and replay

Disconnect a client after submitting work, inspect its transient request outcome, then inspect the persistent thread/action before retrying. Explain why cancellation/deadline may happen after commit. A matching terminal decision is an idempotent retry; a conflicting decision must be rejected. Do not promise external exactly-once email delivery from a local unique database record.

## 5. Diagnose provider failure

An unconfigured or unconsented live request must fail before registering a new model-driven thread, even when retrieval would find no evidence. With real provider access, use the live runbook's unreachable-endpoint experiment to observe transport failure and sanitized error classification. Do not insert fake model success to make a health endpoint look ready.

## 6. Write an operational handoff

Document startup/shutdown, bounded concurrency/deadlines, database locations, privacy, observed latency, and a rollback procedure preserving compatible state. Explain the local POSIX lock and serialized database scope; do not extrapolate it to multi-host deployment. Define workload/cost targets from measured behavior, not arbitrary universal SLAs.

**Gate:** another learner can start the application outside the IDE and reproduce owned persistent review and visible failures. Provider quality/outage gates remain unverified without accessible credentials and spending consent. Reassess with an unfamiliar request/owner combination in the capstone.
