# Independent exercise — durable decisions across real process restart

Prerequisites: [Module 10](../lessons/10_durable_approval/01.md). Use dedicated paired databases with `--db` and `--actions-db`, or new unique thread IDs in course state. Read [the runbook](../labs/10_durable_approval/README.md), not the [solution](../solutions/10_durable_approval.md), before your attempt.

1. Predict the durable facts after start, reject, approve and edit. Start three explicit human drafts, allow each Python process to exit, then inspect them in new processes. Show retained text, origin, pending review and zero preapproval actions.
2. Reject one, approve another and edit the third to a materially different statement. Inspect actual owned action rows: zero for rejected, one for approved, one containing exact edited text. Do not count printed response messages as actions.
3. Repeat the same approval and edit decisions after another process restart. Show row counts unchanged. Try a conflicting later decision and a blank edit; state what must stay immutable.
4. As bob, attempt inspection, resumption and `start` of alice's existing thread. All must fail without changing owner or draft. Show that bob's actions list remains empty. Explain why trusted local --user is not authentication and what the HTTP boundary must do later.
5. Attempt to open the existing checkpoint file with a different empty action DB. Predict the sink-binding rejection. Restore the original pair; do not reset away evidence of a configuration error.
6. Explain the crash window between sink commit and next checkpoint. The regression test replays the actual record node: identify how stable action ID plus atomic uniqueness prevents duplicates. Give one external-email counterexample where this local guarantee would not suffice.
7. When provider configuration is available, start a new `--live` thread without --draft, inspect actual RAG source IDs and review the proposal. Record unavailable provider proof explicitly rather than substituting human text.

## Exit and review

Submit actual command transcripts with no credentials, per-thread row counts/text, an ownership explanation, and one independently changed draft. The gate requires process restart, all decisions, retry safety and cross-owner denials. Later, in Module 14, repeat through authenticated HTTP rather than user-controlled identity. Cleanup only your dedicated experiment files after all connections close.
