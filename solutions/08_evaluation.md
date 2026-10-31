# Module 08 solutions — null is not a passing score

Attempt [the exercises](../exercises/08_evaluation.md) first. Use [the runbook](../labs/08_evaluation/README.md) for executable registration/review commands.

## 1. Evaluation objects

The target is the retrieval-plus-answer application. A case fixes question, synthetic identity, split, expected sources/abstention, and semantic rubric. Deterministic checks cover evidence boundaries and citation membership. Human and optional model graders review claim support separately. An experiment is the cases plus configuration and resulting observations—not one impressive answer. Twenty curated cases teach error analysis but cannot support a production reliability guarantee.

## 2. Local report

`--check` runs actual lexical retrieval over development cases. Recall measures overlap with expected source IDs; authorized/current checks inspect returned metadata. Generated answer and semantic scores are null because no model ran. Do not convert that absence to a quality pass, or label an empty valid structure as correct abstention for every case. A retrieval miss requires inspecting token/evidence mismatch, while a forbidden source requires an authorization investigation.

## 3. Registration

`enforce_frozen_config` writes a new development-only config exclusively and compares subsequent settings/data exactly. Held-out requires an existing registration. Changed k/model/strategy/trial/grading settings or corpus hash must fail rather than silently amend the record. This is an instructional procedural guard, not a cryptographic enforcement of honest experimentation: someone can inspect public holdout cases, so document that limitation.

## 4. Paired outcomes

Keep generation model, corpus, question, identity, k, trials, and review protocol fixed while changing retrieval strategy. Present per-case results before aggregates. More evidence recall can still create irrelevant or conflicting context; review generated correctness and grounding. Record failed calls, missing usage, and dated pricing assumptions. After tuning on a held-out failure, use fresh confirmatory evidence for the next superiority claim.

## 5. Grader calibration

Score groundedness, relevance, correctness from 0 to 2 and appropriate abstention separately. Include claim-to-evidence reasoning and reviewer identity. The human-review file is a JSON list keyed by case ID, strategy, trial; the runbook gives the schema. A model grader is a fallible opinion, not ground truth. Read disagreements—especially units, conditions, conflict resolution, and permission boundaries—instead of allowing an average to hide a severe failure.

## 6. Production loop

Inspect transport/tool/deadline errors separately from answer quality; preserve enough permitted metadata to diagnose failures. Hosted traces require permission to upload inputs and outputs. Add real failures to a future regression dataset, protect that version's held-out partition, and record dataset revisions. Do not claim hosted tracing, semantic quality, or cloud evaluation were exercised without credentials and observable results.
