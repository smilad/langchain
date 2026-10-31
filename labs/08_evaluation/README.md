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

Real output of `uv run python labs/08_evaluation/main.py --check` (no credentials, no network; machine paths replaced by `<repo>`). Compare your own run against it.

```json
{
  "preflight": {
    "python": "3.14.0",
    "interpreter": "<repo>/.venv/bin/python",
    "packages": {
      "langchain": "1.4.4",
      "langchain-core": "1.6.9",
      "langchain-openai": "1.7.0",
      "langgraph": "1.2.14",
      "langgraph-checkpoint-sqlite": "3.1.1",
      "fastmcp": "4.1.0",
      "pydantic": "2.14.1"
    },
    "langchain_origin": "<repo>/.venv/lib/python3.14/site-packages/langchain/__init__.py",
    "configured": {
      "api_key": false,
      "model": false,
      "live_consent": false,
      "custom_endpoint": false,
      "hosted_tracing": false
    },
    "live_request_sent": false
  }
}
{
... (807 lines omitted)
        "abstention_matches_label": null,
        "semantic_support": "not a deterministic check"
      },
      "trace": {
        "retrieval_seconds": 0.0017297079903073609,
        "model_calls": 0,
        "usage": [],
        "corpus_sha256": "42dfb685e549233d2795a949c5296ec8f148498f616608b981e541d3ce972066"
      },
      "elapsed_seconds": 0.0017349160043522716
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
[+832 hidden: rtk recall 53d86df7a7d4]
```
