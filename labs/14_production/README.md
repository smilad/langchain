# Module 14 lab — Operate a real localhost workflow application

## Scope, environment, and proof
The serving mechanism is a locked Python process using the standard library's HTTP server, restricted to **127.0.0.1**. This is an operations teaching application, not a hardened internet-facing deployment. Python explicitly [does not recommend http.server for production](https://docs.python.org/3.14/library/http.server.html). TLS, remote identity provisioning, distributed quotas, and a production proxy are outside this localhost lab; do not expose this port publicly.

Installed authoring baseline: Python 3.14.0, LangGraph 1.2.14, SQLite checkpointer 3.1.1, langchain-openai 1.7.0, OpenAI SDK 3.29.0. [uv.lock](../../uv.lock) records exact dependencies. [Verification](../../docs/VERIFICATION.md) records actually exercised local paths and unavailable live gates. No latency/SLA or successful model output is invented.

```sh
uv sync --locked
uv run python labs/14_production/main.py --check
```

That lab starts **actual service subprocesses** and uses real HTTP clients. It exercises public health/readiness, bearer authentication, two concurrent identities, body-identity rejection, cross-user denial, human-authored drafts, client disconnect visibility, clean process restart with pending review, approval replay/idempotent local action, rejection, missing live permission, and a short deadline trial. Temporary lab files are removed only after all launched servers stop; existing `.course/service` data is untouched.

`--live` additionally executes source-grounded RAG and an unreachable configured provider endpoint with genuine credentials. It needs a valid JSON-schema-capable endpoint/model and `COURSE_ALLOW_LIVE=1`. The live question matches current returns evidence so an empty-evidence abstention cannot masquerade as generation/outage proof. The available gateway failed JSON-schema output validation; see [observed results](../../docs/VERIFICATION.md). A model-free human draft is not generated text.

## Manual start: private token bindings
Run from repository root. Generate throwaway tokens without printing their values. Do not enable shell tracing (`set -x`), commit these values, or use them as production credentials:

```sh
export COURSE_ALICE_TOKEN="$(uv run python -c 'import secrets; print(secrets.token_urlsafe(24))')"
export COURSE_BOB_TOKEN="$(uv run python -c 'import secrets; print(secrets.token_urlsafe(24))')"
export COURSE_AUTH_TOKENS="$(uv run python -c 'import json,os; print(json.dumps({os.environ["COURSE_ALICE_TOKEN"]:"alice",os.environ["COURSE_BOB_TOKEN"]:"bob"}))')"
uv run python -m langchain_learning.service --port 8765 --deadline 30 --max-workers 4
```

Tokens must have at least sixteen ASCII non-whitespace characters and map to supported `alice`, `bob`, or `finance` identities. Default state is `${COURSE_STATE_DIR:-.course}/service/checkpoints.sqlite` and `actions.sqlite`. `--db PATH --actions PATH` can select an explicit matched pair. The service does not log token bindings. Curl examples below are localhost-only; command arguments can be visible to local processes, so do not reuse this pattern as a production secret-management guarantee.

## Exact API contract
Success is HTTP 200; workflow routes return `{"result": ..., "request_id": "..."}`. `result` for a thread contains `thread_id`, `user_id`, `status`, `state`, `pending_review`, and `actions`. Actions returns an owner-filtered list. Bearer identity is the **only** request identity; `user_id` in bodies is rejected.

| Method/path | Authentication | Body/meaning |
|---|---|---|
| `GET /health` | Public | Liveness; local-only flag |
| `GET /ready` | Public | Local storage available and not stopping; provider not probed |
| `POST /threads/start` | Bearer | `thread_id`, nonempty `question`, optional human `draft`, optional boolean `live` |
| `GET /threads/<id>` | Bearer | Inspect owned persisted state |
| `POST /threads/<id>/decision` | Bearer | `decision`: `approve`, `reject`, or `edit`; edit requires `edited_draft` |
| `GET /actions` | Bearer | List only the owner's actual local actions |
| `GET /requests/<request_id>` | Bearer | Owner-filtered transient request outcome; last 256/current process |

Thread/request IDs match `[A-Za-z0-9_-]{1,80}`. Optional `X-Request-ID` allows observing a disconnected request; duplicate request IDs return 409. Request IDs are observation identifiers, **not** idempotency keys. Workflow/action identity provides local action deduplication. Repeated owned thread start inspects existing input rather than replacing it; conflicting persisted decisions fail.

```sh
curl --fail http://127.0.0.1:8765/health
curl --fail http://127.0.0.1:8765/ready
curl --fail -H "Authorization: Bearer $COURSE_ALICE_TOKEN" -H 'Content-Type: application/json' \
  -d '{"thread_id":"review-a","question":"What is the return policy?","draft":"This response was explicitly authored by a human for the approval exercise."}' \
  http://127.0.0.1:8765/threads/start
curl --fail -H "Authorization: Bearer $COURSE_ALICE_TOKEN" http://127.0.0.1:8765/threads/review-a
```

Stop with Ctrl-C; restart with the same state paths and token bindings. Inspect `review-a` again before resuming:

```sh
curl --fail -H "Authorization: Bearer $COURSE_ALICE_TOKEN" -H 'Content-Type: application/json' \
  -d '{"decision":"edit","edited_draft":"Human-reviewed replacement text."}' \
  http://127.0.0.1:8765/threads/review-a/decision
curl --fail -H "Authorization: Bearer $COURSE_ALICE_TOKEN" http://127.0.0.1:8765/actions
```

To use actual RAG, configure the provider privately and send a **new** thread with `{"thread_id":"live-a","question":"What is the returns deadline for an unused item?","live":true}` and no human draft. No retrieved evidence means explicit abstention without a model call. Do not overwrite an existing human thread and call its retained draft model-generated.

## Bounds, cancellation, and failure diagnosis
The server bounds admitted connections, the TCP backlog, body size (16 KiB), socket reads, and the whole workflow deadline (0.1..60 seconds). Overload returns 503 with Retry-After; there is no per-user distributed rate limiter. Independent spawned workers own SQLite contexts. Workflow-level cross-process locking serializes graph runs safely, so more HTTP workers do not imply more concurrent SQLite effects. The model runtime allows one SDK retry; the service adds none.

- 401: bearer missing/invalid; 403: ownership/permission denied.
- 400: invalid fields/state or missing model settings; 413/415: body/content-type rejected.
- 502: workflow/upstream worker failure, including `ModelOutputError` for malformed or ungrounded generated output; sanitized exception class only. 504: deadline expired.
- 503: overloaded, stopping, or storage not ready; 409: reused observation ID.

The server checks real client disconnects while a worker runs. It terminates/joins the child on cancellation, deadline, or shutdown, and records status plus `effects_may_have_committed`. **No rollback guarantee:** SQLite checkpoints or actions may already have committed. Inspect `/threads/<id>` and `/actions` before retry. A disconnect during response writing is separately visible as `response_disconnected`. Request-outcome records vanish on restart; workflow state does not.

Logs contain event/status/request ID/latency/error class, never bearer headers, prompts, drafts, or raw provider error text. Failures are not swallowed into success. Responses still contain synthetic state and require appropriate handling in a real system. `--live` lab's outage uses `OPENAI_BASE_URL=http://127.0.0.1:1/v1` only in its isolated child service; it does not alter your `.env` or fabricate a key.

## Clean stop, backup, and observable rollback
SIGINT/SIGTERM stops admission, cancels active child work, joins it, closes the socket, and emits `stopped`. Stop **all** processes using the same workflow files before backup/restore. Check that the old port is closed and no worker remains; a forced kill is not clean-shutdown evidence.

Use SQLite's backup API rather than copying an active database/WAL pair. The following example assumes default `.course` state; adjust both paths together when using `COURSE_STATE_DIR` or explicit CLI paths:

```sh
uv run python -c 'import sqlite3; from pathlib import Path; root=Path(".course/service"); backup=root/"backup-before-change"; backup.mkdir(exist_ok=True); names=("checkpoints.sqlite","actions.sqlite");
for name in names:
    with sqlite3.connect(root/name) as source, sqlite3.connect(backup/name) as target:
        source.backup(target)'
```

Record the current revision, lockfile, and backup location locally. For a code rollback, use a separate known-good checkout/worktree and `uv sync --locked`; do not destructively reset unrelated user changes. Start that revision on port 8766 against **copies** of a matched, schema-compatible checkpoint/action backup using `--db` and `--actions`. Probe readiness, inspect a known pending thread with its owner token, and verify owner-filtered action counts before selecting it as the serving process. Then stop the failed version. Never restore only one file or silently erase already committed actions.

No automatic schema migration is claimed. If an incompatible change has occurred, restoring a matched backup is a recovery decision that can discard newer local state; preserve evidence and obtain an explicit data-recovery decision. Rehearse using synthetic lab state first. Rollback does not undo external email/payment; this course's sink records local actions only.

After manual practice, stop the process before removing your **selected synthetic state directory**. Do not delete shared policy/catalog fixtures or another learner's state. Derive latency/cost targets from your measured workload, not from the worker count. Continue with [lessons](../../lessons/14_production/01.md), [exercise](../../exercises/14_production.md), and [solutions](../../solutions/14_production.md).

## Captured `--check` output

Real output of `uv run python labs/14_production/main.py --check` (no credentials, no network; machine paths replaced by `<repo>`). Compare your own run against it.

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
... (461 lines omitted)
      "event": "running",
      "request_id": "171f76b9ac334fe99624231be6ce2433"
    },
    {
      "event": "deadline_exceeded",
      "request_id": "171f76b9ac334fe99624231be6ce2433",
      "effects_may_have_committed": true
    },
    {
      "event": "http_response",
      "method": "POST"
    },
    {
      "event": "stopping",
      "signal": 15
    },
    {
      "event": "stopped"
    }
  ],
  "exit_code": 0
}
{
  "local_state": "Temporary lab state removed after service shutdown; persistent manual service state is untouched."
}
[+486 hidden: rtk recall de7066d83af1]
```
