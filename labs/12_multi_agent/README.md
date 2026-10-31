# Module 12 lab — One specialist must earn its place

## Setup and entrypoint
From repository root:

```sh
uv sync --locked
uv run python labs/12_multi_agent/main.py --check
```

Installed authoring baseline: Python 3.14.0, LangChain 1.4.4, langchain-openai 1.7.0. [uv.lock](../../uv.lock) records the full set; [verification](../../docs/VERIFICATION.md) records exercised paths and unavailable live gates. The default is model-free check mode, not a fake agent run.

The check retrieves actual filtered policy documents for four cases and rejects a deliberately out-of-scope structured handoff. It does not estimate model quality, token usage, or architecture latency.

## Real model experiment
Configure `OPENAI_API_KEY`, `COURSE_MODEL`, and `COURSE_ALLOW_LIVE=1` privately. The selected model must support tool calling and structured output. Do not print configuration objects, commit `.env`, or upload traces without permission.

```sh
uv run python labs/12_multi_agent/main.py --live --trials 2
uv run python labs/12_multi_agent/main.py --live --trials 1 --fail-specialist
```

Trials are declared and bounded to 1..5. Each trial runs four cases under both arms, with alternating arm order. Questions cover returns, shipping, unavailable information, and a restricted-finance request from Bob. Both arms receive the same request-scoped evidence. The single agent drafts using one retrieval tool; the coordinator can call one actual policy-specialist agent via one tool. Neither arm can approve or execute an action.

Limits: single drafter at most four logical model calls/two retrieval calls; specialist arm at most three coordinator plus four drafter model calls and one delegation plus two retrieval calls. Recursion is capped per agent. With two trials, there are sixteen runs and at most eighty-eight logical model calls across arms; provider retries may add physical requests. A full run can cost money even when it fails. Missing usage means unknown, never zero.
The middleware limits **named business tools**, not structured-response formatting calls. A global one-call coordinator limit would incorrectly block the response after a successful delegation. Actual after-fix eight-run evidence and the real-result fault stop are recorded in [verification](../../docs/VERIFICATION.md).

`--fail-specialist` corrupts citations **after a real specialist result**, making the handoff validator stop propagation. This is an explicitly injected boundary fault, not a claim that the provider naturally emitted it. Expected fault stops are printed; normal-mode failures make the lab exit nonzero.

## Evidence and decision rubric
Retain actual rows locally: case/trial/arm, evidence IDs, result/error, elapsed seconds, attempted calls, actual boundary calls, and reported usage. For each substantive claim, inspect supporting passages. Review contradictions, abstention, restricted disclosure, and document-instruction resistance separately from source-ID membership.

Publish failures, variability, and usage limitations alongside median/range latency. Do not award quality for fluent unsupported prose. Keep the specialist only if its observed benefit outweighs cost, latency, and another failure boundary; deliberately rejecting it passes the architecture-decision gate.

## Diagnosis and state
Missing consent/configuration is not a failed learner concept. Tool/model-budget errors require trace inspection; unauthorized source IDs require fixing the handoff boundary, not increasing context blindly. This lab creates no persistent workflow actions or model transcripts. It reuses the source corpus; do not delete shared policy data to “reset” an experiment. Live evidence must be supplied by an actual configured run.

Continue with [lessons](../../lessons/12_multi_agent/01.md), [exercise](../../exercises/12_multi_agent.md), and [reasoned solutions](../../solutions/12_multi_agent.md).

## Captured `--check` output

Real, unedited stdout of `uv run python labs/12_multi_agent/main.py --check` (no credentials, no network; local paths replaced by `<repo>`). Compare your own run against it.

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
  "contract_cases": [
    {
      "question": "What is the return policy?",
      "user_id": "alice",
      "evidence_ids": [],
      "invalid_handoff_rejected": true
    },
    {
      "question": "How long does shipping take?",
      "user_id": "bob",
      "evidence_ids": [
        "SHIPPING"
      ],
      "invalid_handoff_rejected": true
    },
    {
      "question": "What is the policy for teleporting a parcel?",
      "user_id": "alice",
      "evidence_ids": [],
      "invalid_handoff_rejected": true
    },
    {
      "question": "What is the confidential finance reimbursement limit?",
      "user_id": "bob",
      "evidence_ids": [
        "MALICIOUS",
        "MEAL"
      ],
      "invalid_handoff_rejected": true
    }
  ],
  "live_gate": "Unverified: real single/specialist generation, quality, timing and usage."
}
```
