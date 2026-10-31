# Reasoned solution — durable approval is more than saved text

Use the exact separate-process commands in [the lab README](../labs/10_durable_approval/README.md); [verification](../docs/VERIFICATION.md) records exercised evidence. This solution does not claim authoring runs or model results.

## Correct state transitions

Start binds owner, action ID and original input, then real graph execution pauses in review. `inspect` in another process loads SQLite checkpoints: the explicit human draft and pending review survive. No action exists yet because record is downstream of the interrupt.

Reject persists the human decision, resumes the review node with Command, and routes to END: zero action rows. Approve routes to record: one row. Edit replaces the proposal with nonempty human-approved text before record: the stored action contains that exact text. A blank edit must fail before binding a decision, allowing a later valid edit. These assertions concern actual local records, not displayed success wording.

## Restart, replay and identity

A matching repeated decision returns existing terminal state without another action. The stronger regression test selects the actual pre-record checkpoint and reexecutes record; stable action identity and the SQLite unique insert preserve one identical row. The record transaction checks identity/content rather than overwriting a collision. A failure after the sink commits but before completion checkpoints is safe to replay locally.

This is not external email exactly once. If a mail server accepts a send and the process dies before acknowledgment, another attempt may deliver twice unless that external interface supports idempotency or a delivery design with stated semantics. LangGraph persistence alone cannot create such a guarantee.

Owner metadata is bound on first creation and never accepts an owner supplied by a later restart. Bob cannot inspect, resume or overwrite alice's thread. Alice repeating start receives original state, not a new proposal. Trusted CLI identity is not authentication; Module 14 derives it from verified tokens before calling SupportWorkflow.

## Diagnostic feedback

Pending state disappears → compare database pair/thread ID and process configuration, not model memory. Wrong edited text → inspect review update and committed sink row. Duplicate rows → inspect action identity placement/transaction and checkpoint crash window. Changed sink path → preserve existing pair; the checkpoint binding intentionally rejects the mismatch. Provider failure → report prerequisite/transport failure, do not invent draft text.

Live proof requires actual rag.answer with model consent and source support review. Human input proves durable control only. Independent transfer should change text/owner/thread constraint; supplied solution execution is practice, not mastery evidence.
