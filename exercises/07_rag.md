# Module 07 exercises — support is more than citation presence

Read [the lessons](../lessons/07_rag/01.md) and inspect [the lab](../labs/07_rag/README.md). Use official documentation lookup; attempt the questions before [solutions](../solutions/07_rag.md).

## 1. Map the two-step baseline

Draw question → authorized retrieval → evidence payload → typed model output → citation-membership check. State the input/output shape and responsibility at each boundary. Which stage can run without a model? Which check can establish only structural validity, not factual support?

## 2. Investigate the local cases

Run `uv run python labs/07_rag/main.py --check`. Compare evidence for a current return deadline, unrelated question, remote-work contradiction, outdated fourteen-day claim, malicious source, and finance request. Separate current-version filtering, permission filtering, insufficient relevance, and conflicting current evidence. Predict the desired answer behavior before considering any generated prose.

## 3. Refute citation-only scoring

The lab deliberately supplies a human-authored nine-hundred-day claim with the real `RETURN` ID. Explain why membership validation passes while support fails. Design a claim-to-passage rubric that checks the period, start event, eligibility, and units. Do not treat this authored counterexample as observed model output.

## 4. Generate and review, when configured

With explicit consent, run `--live --question 'What is the returns deadline?'`, then a warranty question and an unanswerable question. Inspect raw selected evidence and typed answers. Review substantive claims, citations, and appropriate abstention separately. An exact output sentence is not a reproducible acceptance criterion.

## 5. Change one retrieval decision

On development examples, choose query rewrite or reranking (`--experiment rewrite` or `--experiment rerank`). Keep model/corpus/other settings fixed, record extra calls, and compare selected evidence. Explain why the generation trace alone does not include rewrite/rerank usage. Use an explicitly authorized tracing service only if content upload is acceptable.

## 6. Decide whether agentic retrieval is justified

Run the real paired experiment `--live --compare-agentic` only with provider access. Explain what dynamic retrieval decisions add and what extra error/latency/cost they create. Retaining the two-step baseline is a valid result. Do not infer general superiority from one paired run.

**Gate:** supported citations, deliberate abstention, conflicts, outdated sources, and malicious/unavailable evidence must be investigated. Diagnose a retrieval miss separately from an unsupported generated claim. Without a provider, preserve the local boundary evidence and explicitly leave generated support/injection behavior unverified. Review a changed question in Module 08.
