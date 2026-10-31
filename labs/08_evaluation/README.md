# Lab 08 — freeze, run, inspect, then grade saved observations

Prerequisites: [Modules 06–07](../../lessons/07_rag/01.md), the [lesson sequence](../../lessons/08_evaluation/01.md), and the locked checkout environment. [Exercises](../../exercises/08_evaluation.md) / [solutions](../../solutions/08_evaluation.md). Actual verification is [separate from learner mastery](../../docs/VERIFICATION.md).

## Target and dataset

`langchain_learning.evaluation` runs actual authorized retrieval, optionally real generation, deterministic boundary checks, and optional fallible model grading. The committed `data/evaluations/rag.jsonl` has exactly twenty synthetic cases: eight answerable, four unanswerable, four conflicting/outdated, four adversarial/access; twelve development and eight held-out. Byte hash and category/split checks reject unnoticed dataset edits. Expected evidence IDs are retrieval targets; they are not sufficient answer-quality scores.

## Local development evidence, no API request

```bash
uv run python labs/08_evaluation/main.py --check
```

Inspect per-case question, user, evidence metadata/text, expected-evidence recall, authorization/current flags, elapsed time, and failure categories. Generated answers and unexercised generation checks remain null. No fake model answers or semantic grades are substituted.

To exercise registration locally without claiming generated quality:

```bash
uv run python labs/08_evaluation/main.py --check --freeze-config .course/local-rag-config.json --output .course/local-rag-dev.json
uv run python labs/08_evaluation/main.py --check --split held_out --config .course/local-rag-config.json --output .course/local-rag-heldout.json
```

These paths must be new: output and registration use exclusive creation. Reuse an existing registration with `--config`, never overwrite it to erase a changed setting. Local registration has `live: false`; it cannot authorize a later live experiment.

## Real generation protocol

Set actual `OPENAI_API_KEY`, `COURSE_MODEL`, and explicit `COURSE_ALLOW_LIVE=1` privately. Semantic/hybrid search also requires `COURSE_EMBEDDING_MODEL`. Confirm model capability, pricing, and data policy before paid requests. Defaults are lexical k=3 and one declared trial; configure different settings deliberately.

```bash
uv run python labs/08_evaluation/main.py --live --trials 2 --freeze-config .course/live-rag-config.json --output .course/live-rag-dev.json
uv run python labs/08_evaluation/main.py --live --trials 2 --split held_out --config .course/live-rag-config.json --output .course/live-rag-heldout.json
```

Tune only on development cases, then freeze before the held-out command. Keep settings identical: the CLI compares them with the registration; it does not silently load different arguments from that file. Twenty small synthetic cases and two trials are instructional, not statistically strong evidence of production reliability.

For a one-variable retrieval comparison add `--compare-strategy semantic` to **both** commands and choose fresh registration/output paths. For an optional real model grader add `--judge` to both before freezing. A grader call costs money, can be wrong, and cannot replace calibration against human review. Failed generation or grader execution is emitted per case and produces a nonzero command exit; semantic-quality failures remain explicit report categories.

## Human review applies to saved answers, not a new run

Read one saved report's exact answer, selected passages, identity, case rubric, and trial. Prepare a private JSON list. Each entry contains:

- `case_id`: the saved row's case identifier (for example `a01`).
- `strategy`: the saved row's strategy, not the desired next strategy.
- `trial`: its integer trial number.
- `reviewer`: a nonempty reviewer identity.
- `grade`: `groundedness`, `relevance`, `correctness` integers 0–2; `abstention_appropriate` boolean; `claim_evidence` list of actual claim-to-passage reasoning; `rationale` string.

Apply those observations offline:

```bash
uv run python labs/08_evaluation/main.py --check --review-report .course/live-rag-heldout.json --human-review .course/human-reviews.json --output .course/live-rag-reviewed.json
```

This command annotates the saved report without retrieval, generation, or judge calls. Partial review is allowed; report how many rows remain unreviewed. Unknown case/strategy/trial keys, duplicate case keys, and grading a row with no generated answer fail visibly. `--human-review` without `--review-report` is rejected: rerunning a stochastic target would associate the old grade with a different observation. An inappropriate abstention is a human semantic failure even if the three numeric grades are high.

## Diagnose before changing anything

A lexical miss is not automatically generation failure. Citation membership is not entailment. Outdated or forbidden evidence is a boundary defect, not something to average away. Distinguish target errors, retrieval relevance, unsupported claims, abstention decisions, grader errors, and missing environment configuration. Record usage only when actually reported; absent usage is not zero spend. Hosted traces require separate credentials and permission to upload content.

**Acceptance:** produce a registered per-case experiment, inspect errors and evidence, and justify the comparison without tuning on confirmatory results. With no provider, finish local retrieval/registration boundaries and mark generated semantic quality, model grades, embedding relevance, and hosted evaluation unverified.

## Captured `--check` output

Output of `uv run python labs/08_evaluation/main.py --check` (no credentials, no network), re-formatted as indented JSON; local paths are replaced by `<repo>`. The environment `preflight` block is omitted here; Module 00 shows it in full. The middle of the output is omitted for length. Ids, timings and temporary paths will differ on your machine; the shape and the pass/fail results should match.

```text
{
  "dataset_sha256": "c52d16db367b05d7cf5bc5c35c6dc21f665bd03c93a013101996704308764467",
  "split": "dev",
  "trials_declared": 1,
  "mode": "deterministic retrieval only; no generated answers",
  "comparison": null,
  "cost": "No currency estimate: usage when reported is per-row; pricing/rates not assumed",
  "limitations": [
    "20 synthetic cases are not a production benchmark",
    "held-out is review only; no tuning loop",
    "semantic support requires human review; model grades are not an oracle",
    "trials reflect provider variability, not statistically strong confidence intervals"
  ],
  "summary": {
    "lexical": {
      "rows": 12,
      "mean_seconds": 0.002054562583604517,
      "population_stdev_seconds": 0.002188508099401922,
      "failures": {},
      "human_reviewed": 0
    }
  },
  "cases": [
    {
      "case_id": "a01",
      "category": "answerable",
      "split": "dev",
      "question": "How many calendar days do I have to return unused items with a receipt?",
      "user_id": "alice",
      "trial": 1,
      "strategy": "lexical",
      "human_rubric": "Must state 30 calendar days after delivery, unused items and receipt; do not repeat old 14-day rule.",
      "human_review": null,
      "model_grade": null,
      "generated_answer": null,
      "failure_categories": [],
      "evidence": [
        {
          "text": "Returns are accepted within 30 calendar days of delivery with a receipt. Items must be unused. Final-sale items cannot be returned.",
          "metadata": {
            "source_id": "RETURN",
            "version": 2,
            "current": true,
            "audience": "public",
            "title": "Returns",
            "trust": "policy",
            "provenance": "Synthetic course author; approved policy",
            "effective_date": "2026-10-01",
            "path": "return-v2.json",
            "content_sha256": "a31916496793af837c1cf1e63299cc8c0cf68259fd5e6d22632d504c86088a3f",
            "chunk_id": "RETURN:v2:0",
            "chunk": 0
          }
        },
        {
          "text": "Submit expense receipts within 45 calendar days of purchase through the expense portal. Receipts must show the date, amount and vendor.",
          "metadata": {
            "source_id": "EXPENSE",
            "version": 1,
            "current": true,
            "audience": "public",
            "title": "Expense submission",
            "trust": "policy",
            "provenance": "Synthetic course author; approved policy",
            "effective_date": "2026-10-01",
            "path": "expense-v1.json",
            "content_sha256": "3a7e11574043528e1eb63ca808280663ea8cc8ae9135fcdd4f6384f940a9cc8c",
            "chunk_id": "EXPENSE:v1:0",
            "chunk": 0
          }
... (middle omitted for length) ...
            "trust": "policy",
            "provenance": "Synthetic course author; approved policy",
            "effective_date": "2026-10-01",
            "path": "cancel-v1.json",
            "content_sha256": "daec76881405878be15eb9cae761554459d014dcd0904902a9d2cc840e77413f",
            "chunk_id": "CANCEL:v1:0",
            "chunk": 0
          }
        }
      ],
      "deterministic": {
        "authorized_current_only": true,
        "expected_evidence_recall": 1.0,
        "expected_evidence_missing": [],
        "citation_membership": null,
        "abstention_matches_label": null,
        "semantic_support": "not a deterministic check"
      },
      "trace": {
        "retrieval_seconds": 0.0014246670180000365,
        "model_calls": 0,
        "usage": [],
        "corpus_sha256": "42dfb685e549233d2795a949c5296ec8f148498f616608b981e541d3ce972066"
      },
      "elapsed_seconds": 0.0014281670446507633
    }
  ],
  "configuration": {
    "strategy": "lexical",
    "k": 3,
    "trials": 1,
    "compare_strategy": null,
    "live": false,
    "judge": false,
    "model": null,
    "embedding_model": null,
    "dataset_sha256": "c52d16db367b05d7cf5bc5c35c6dc21f665bd03c93a013101996704308764467",
    "corpus_sha256": "42dfb685e549233d2795a949c5296ec8f148498f616608b981e541d3ce972066"
  }
}
```
