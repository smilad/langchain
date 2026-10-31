# Reasoned solution — explicit graph workflows

Start with your own predictions from [the exercise](../exercises/09_graph_workflows.md). Commands below are implemented, not claimed observed during authorship; integration evidence belongs in [verification](../docs/VERIFICATION.md).

## Route and update reasoning

`uv run python labs/09_graph_workflows/main.py --check` runs actual supported/review/unsupported paths. Classify writes a route plus one event. Supported fans out to retrieve and constraints; retrieve owns evidence, both contribute events, and the barrier waits for both before drafting. Review and unsupported go directly to END. The human draft is an explicit workflow fixture, not model quality evidence.

The reducer belongs on events because more than one parallel writer contributes to it. Returning the full existing list would add old events again; returning `[]` would not clear additive state. Evidence needs no merging reducer because only retrieve writes it. The deliberate broken graph should reject concurrent event writes with InvalidUpdateError. A self-loop with no stopping condition should reach the recursion bound; increasing the bound merely delays the defect.

## Changed branch

A provenance check that validates a static required source schema can run independently. Its event can be merged and the fan-in updated to include all required branch names. A check that inspects retrieved evidence depends on retrieve, so it must follow retrieval. It is wrong to run both in parallel and assume shared state contains retrieval's future update. Choosing the correct dependency is the central transfer test.

For overlapping route words, document deterministic precedence. Live classification instead validates a closed Route label and can still choose the wrong meaning. Its supported path invokes actual rag.answer; generated source claims need separate grounding review. No deterministic fixture substitutes for this live gate.

## Diagnostic feedback

Goal → missing evidence before draft → missing dependency or wrong update → inspect updates and join. Goal → one contribution per branch → duplicated events → node returned accumulated history → return only its own update. Goal → finite workflow → recursion exception → unconditional back edge → define termination. Use actual state and trace evidence before prompt edits.

An independent variation must change the constraint, not simply rerun the provided return question. Retention review: reconstruct the graph in Module 10 and explain why checkpoint replay adds a different failure mode from reducer merging.
