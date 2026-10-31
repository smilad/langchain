# Capstone solutions and diagnosis

Attempt [the exercises](../exercises/15_capstone.md) first. These are solution methods and expected invariants, not fabricated run output. Compare them with your actual evidence and [the verification report](../docs/VERIFICATION.md).

## A. Smallest architecture

Token authentication binds identity; retrieval selects authorized current `Document` values with source metadata; the model proposes a typed `GroundedAnswer`; the workflow persists state and interrupts; a reviewer supplies a decision; a SQLite transaction inserts an action with stable identity. A different user must be rejected at the workflow boundary, even if the HTTP handler already authenticated. Unknown evidence permits abstention; conflicting current evidence needs an explicit qualification/abstention, not an invented resolution.

There is no requirement for independent autonomous specialists here. A specialist is retained only if the Module 12 comparison justifies its extra cost/error surface. LangGraph makes the requested approval/recovery behavior explicit without requiring multiple agents.

## B. Persistence and local effect identity

Run the exact separate-process commands in [the capstone runbook](../labs/15_capstone/README.md) with a fresh thread ID. The second process should find a pending review because checkpoints live in SQLite, not Python memory. The edit decision supplies the intended text; resumption records it in the local sink.

Retrying the same completed decision should inspect/reuse the completed state and existing action identity. A conflicting retry is not a new review request and must be rejected. The relevant guarantee is the unique transactional **local** record. Sending an external email after a database insert would require its own delivery/idempotency design and cannot inherit this guarantee automatically.

A wrong thread ID selects another run; a wrong owner is denied; neither is a model-memory failure. Inspect configuration/state before changing prompts.

## C. Rejection and ownership

A rejected review ends without inserting an action. Check the owner-filtered action list, not only the final assistant sentence. Another user's access must fail before the inspected state/draft is returned and before resume can mutate it. The ownership binding survives process restart.

HTTP request bodies cannot select authenticated identity. A bearer token maps to a trusted user; the persisted workflow checks that identity again. If a test passes only because the model obeyed an instruction not to leak, you have not demonstrated an access-control boundary.

## D. Evidence categories

`RETURN` v1 is obsolete: the current-version filter prevents it competing with the current thirty-day policy. The two remote-work allowances are both current and intentionally conflict: provenance helps expose a real contradiction, but cannot decide authority without a rule. A generated answer should acknowledge this rather than choosing whichever passage appears first.

A finance question as Alice tests authorization independently of relevance. The finance identity may retrieve the restricted source; Alice must not see it. Source membership establishes provenance, not claim support. Read the cited passage and inspect the period, eligibility, scope, and effective version of the generated claim.

## E. Honest comparison

Use the development split for diagnosis/tuning, record/freeze configuration, then assess the holdout under a declared protocol. If you tune on inspected holdout failures, that set is no longer independent for the subsequent claim. Report case-level outcomes and uncertainty because eight held-out examples are too few for strong production claims.

A lexical-to-semantic comparison changes only retrieval strategy (and necessarily the actual embedding implementation). Preserve the generation configuration and report that distinction. Report measured latency and provider-reported usage; compute cost only with explicit model pricing assumptions. Without a live provider, generated semantics, stochastic robustness, and model-judge calibration remain unverified.

## F. Transfer and consumer documentation

A new policy needs stable source identity, version/access metadata, ingestion/reindexing, and an independent query. It should not require rewriting approval ownership or local-action uniqueness. Explain this separation before making changes.

A usable tutorial includes the locked environment, no-cost local run, explicit paid/live consent, token-bound HTTP flow, process restart, rejection/edit, evaluation protocol, and known limitations. Client disconnect/deadline does not prove rollback; inspect persisted state before retry. Do not publish an exact stochastic sentence as a guaranteed output or claim peer approval without that review.

The independent variation and later review must be performed by the learner. These solutions can support practice; reading them is not evidence that the learner has mastered the capstone.
