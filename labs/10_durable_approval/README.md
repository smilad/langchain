# Module 10 — durable human approval

Setup: `uv sync --locked`; read [lesson 01](../../lessons/10_durable_approval/01.md). Python >=3.14, [lockfile versions](../../uv.lock). [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) and [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), checked 2026-10-12. Uses actual SqliteSaver and an atomic local SQLite action sink. macOS/Linux POSIX file locks serialize cooperating local processes.

## Deterministic checks

```sh
uv run python labs/10_durable_approval/main.py --check
uv run python -m unittest discover -s tests -p test_workflow.py
```

Check creates temporary databases, starts approve/reject/edit threads, proves no preapproval actions, closes/reopens, resumes each decision, checks edited content, matching retry and cross-owner denials. Regression tests additionally launch a real separate process and replay the actual record node from checkpoint history. Tests are for parent verification, not claimed already run.

## Actual process-restart gate

Each command below starts a new Python process. Let start exit before inspecting/resuming. Defaults use `.course/support.sqlite` and `.course/actions.sqlite` (or COURSE_STATE_DIR). Use fresh thread IDs if already completed; never delete unrelated learner state to get a desired result.

```sh
uv run python labs/10_durable_approval/main.py --operation start --thread restart-demo --draft 'Human draft: review the return policy before replying'
uv run python labs/10_durable_approval/main.py --operation inspect --thread restart-demo
uv run python labs/10_durable_approval/main.py --operation decide --thread restart-demo --decision approve
uv run python labs/10_durable_approval/main.py --operation decide --thread restart-demo --decision approve
uv run python labs/10_durable_approval/main.py --operation actions
uv run python labs/10_durable_approval/main.py --operation start --thread reject-demo --draft 'Human draft to reject'
uv run python labs/10_durable_approval/main.py --operation decide --thread reject-demo --decision reject
uv run python labs/10_durable_approval/main.py --operation inspect --thread reject-demo
uv run python labs/10_durable_approval/main.py --operation start --thread edit-demo --draft 'Original human draft'
uv run python labs/10_durable_approval/main.py --operation decide --thread edit-demo --decision edit --edited-draft 'Corrected human-approved text'
uv run python labs/10_durable_approval/main.py --operation inspect --thread edit-demo
```

Expected contracts: pending survives restart, rejection has zero thread actions, approval has one, repeated approval stays one, edit stores exact corrected text. Prove denials (each should exit nonzero):

```sh
uv run python labs/10_durable_approval/main.py --operation inspect --user bob --thread restart-demo
uv run python labs/10_durable_approval/main.py --operation decide --user bob --thread restart-demo --decision approve
uv run python labs/10_durable_approval/main.py --operation start --user bob --thread restart-demo --draft 'Ownership takeover attempt'
```

A trusted local `--user` is not authentication. The service later binds identity to authenticated tokens. Existing-owner start only inspects; it never overwrites original input. A persisted human decision cannot be changed by later resume. Both databases must remain paired; the checkpoint database rejects a different sink path. `--db` and `--actions-db` allow dedicated absolute paths for an isolated experiment.

## Real model drafting

Configure OPENAI_API_KEY, COURSE_MODEL and COURSE_ALLOW_LIVE=1 privately:

```sh
uv run python labs/10_durable_approval/main.py --live --thread live-draft-demo --question 'What is the return policy?'
uv run python labs/10_durable_approval/main.py --operation inspect --thread live-draft-demo
uv run python labs/10_durable_approval/main.py --operation decide --thread live-draft-demo --decision approve
```

No `--draft` here: actual `rag.answer` produces a source-grounded proposal. Explicit drafts always remain human-origin even when combined with --live; they are not model-call proof. Provider failure does not fabricate a proposal; ownership remains bound.

## Scope, cleanup and evidence

Exactly-once means a single atomic owned **local record** under replay, not general email/network exactly-once delivery. Stable identity plus unique transaction handles a sink-commit/checkpoint crash window. File locking serializes local operations and limits throughput; this is not a distributed deployment. Synthetic drafts remain in private SQLite files.

For reset, stop every using process, remove only dedicated experiment files (checkpoint DB, its `-wal`/`-shm`/`.lock`, action DB and its `-wal`/`-shm`), and use new paired files. Do not reset shared `.course` blindly. **Evidence status:** [verification](../../docs/VERIFICATION.md) records actual local commands/outcomes separately from unavailable live proof. Installed baseline: Python 3.14.0, LangGraph 1.2.14, langgraph-checkpoint-sqlite 3.1.1. [Exercise](../../exercises/10_durable_approval.md), [solutions](../../solutions/10_durable_approval.md).

## Captured `--check` output

Real output of `uv run python labs/10_durable_approval/main.py --check` (no credentials, no network; machine paths replaced by `<repo>`). Compare your own run against it.

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
... (52 lines omitted)
      "thread_id": "edit",
      "question": "Return policy?",
      "draft": "Human-reviewed corrected text",
      "draft_origin": "human",
      "source_ids": [],
      "live": false,
      "action_id": "68fe9530213747f4a0d92b81facaeb5f",
      "decision": "edit",
      "status": "recorded"
    },
    "pending_review": [],
    "actions": [
      {
        "action_id": "68fe9530213747f4a0d92b81facaeb5f",
        "thread_id": "edit",
        "user_id": "alice",
        "draft": "Human-reviewed corrected text",
        "created_at": "2026-10-31 09:31:45"
      }
    ]
  },
  "cross_owner": "inspection/resumption/restart denied",
  "limits": "Close/reopen verified by this command; separate CLI invocations are the process-restart gate. Exactly-once concerns only atomic local SQLite records.",
  "live_gate": "Model drafting unverified without --live and provider consent"
}
[+77 hidden: rtk recall 291c432d2022]
```
