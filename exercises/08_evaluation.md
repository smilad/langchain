# Module 08 exercises — measure failures without leaking the answer

Use [the lessons](../lessons/08_evaluation/01.md) and [the evaluation runbook](../labs/08_evaluation/README.md). Attempt the analysis before [solutions](../solutions/08_evaluation.md).

## 1. Write the evaluation contract

Explain the difference between a target, a dataset case, a deterministic check, a human rubric, a model grade, and an experiment. Inspect the twenty-case dataset: eight answerable, four unanswerable, four conflicting/outdated, four adversarial/access cases; twelve development and eight held-out. Explain why this is instructional, not a production reliability estimate.

## 2. Inspect real development evidence

Run `uv run python labs/08_evaluation/main.py --check`. Select one retrieval miss and one access-boundary case. Explain `expected_evidence_recall`, `authorized_current_only`, and the deliberately null generated-answer/semantic measurements. Why is a null unexercised check different from a successful score of zero or one?

## 3. Freeze a comparison protocol

Declare strategy, k, trials, comparison strategy, model/embedding identifiers, dataset/corpus hashes, and grading mode before the confirmatory run. Freeze a new configuration on development cases, then use the same settings with `--config` on the held-out split. Attempt one changed setting or freeze on held-out; the guard must reject the inconsistent protocol. Do not edit hashes or overwrite the original registration to bypass this rule.

## 4. Compare one variable

With real provider consent, compare lexical and semantic retrieval while keeping generation configuration/cases/trials fixed. Report per-case outcomes, latency, usage when available, missing usage, and human semantic review. State any estimated-price assumptions. If you inspect holdout failures and tune on them, explain why they cease to be independent evidence for the next claim.

## 5. Calibrate the evaluator

Review an actual generated answer against its passages and case rubric. Score groundedness, relevance, and correctness separately; record claim-to-evidence reasoning and reviewer identity. If using `--judge`, compare its opinion with human review before trusting it. Diagnose grader disagreement rather than averaging away an access leak.

## 6. Move from offline to monitoring

Describe which operational failures and live-run quality signals you would inspect in production, how privacy affects trace uploads, and how an observed failure becomes a future regression case without contaminating the existing holdout. Cloud tracing/grades require their own credentials and spending/data-upload decision.

**Gate:** publish per-case evidence and failure categories, distinguish retrieval/generation/evaluator/environment errors, and state which checks were actually exercised. A missing provider is not learner incompetence, but it leaves stochastic quality unverified. Reassess with a fresh case explanation later.
