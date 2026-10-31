# Module 00 lab — setup and Python readiness

This entrypoint exercises real local Python/Pydantic/async behavior and checks the external LangChain import origin. It sends **no model request**, even if `--live` is selected. Read [the four lessons](../../lessons/00_setup/01.md) and attempt [the diagnostic](../../exercises/00_setup.md) before opening [solutions](../../solutions/00_setup.md).

## Prerequisites and commands
From the repository root, with `uv` and a Python ≥3.14 installation available:
```sh
uv sync --locked
uv run python labs/00_setup/main.py --check
```
The distribution/import names are `langchain-learning` / `langchain_learning`; `langchain` belongs to the external dependency. The repository folder can retain its existing name. Use the reported interpreter for your IDE. Metadata/lock/environment/CLI are maintained at the course root, not by this lab.

## Cases and expected boundaries
| Case | Expected behavior, not observed output |
|---|---|
| preflight | interpreter, installed versions, import origin, configuration booleans only |
| valid JSON | typed Request and JSON serialization round trip |
| malformed JSON | decoder error with line/column |
| missing ID/string quantity/zero quantity/blank ID | explicit validation location/type |
| negative quantity | actual traceback frame extraction for diagnosis |
| cooperative coroutines | both tasks execute; B starts before A ends; gathered results retain input order |

The lab asserts each invalid boundary rather than merely printing examples. Missing model/key configuration is reported as false, not printed or treated as model success. Importing `langchain` from repository `src` is rejected. If a dependency import fails, first inspect the running interpreter, then synchronize the locked environment. Package installation is not a provider capability check.

## Evidence and limits
Installed authoring snapshot: Python 3.14.0, LangChain 1.4.4, Pydantic 2.14.1. Exact versions come from `uv.lock` and your actual preflight; consult [verification](../../docs/VERIFICATION.md) for exercised local checks and integration limits. No authored example is an observed model result. No credential is needed for this lab. A green check would not verify authentication, billing, network access or selected model support; Module 01 performs that separate gate.

This lab is stateless and creates no database or learning record. There is nothing to reset. Keep `.env` private; do not delete another module's `.course` state while diagnosing setup.

## Diagnostic pacing
3–5 hours is a suggested setup allocation for someone with relevant Python readiness, not a beginner deadline. If functions, environments or exceptions are new, work through the diagnostic's remediation sequence over additional sessions and reassess on fresh inputs. Delayed review belongs to the learner after actual evidence, not a prefilled progress checklist.

Sources: [uv](https://docs.astral.sh/uv/guides/projects/), [Pydantic](https://docs.pydantic.dev/latest/concepts/models/), [asyncio](https://docs.python.org/3/library/asyncio-task.html), checked 2026-10-12.

## Captured `--check` output

Real, unedited stdout of `uv run python labs/00_setup/main.py --check` (no credentials, no network; local paths replaced by `<repo>`). Compare your own run against it.

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
  },
  "configuration_present": {
    "OPENAI_API_KEY": false,
    "COURSE_MODEL": false
  }
}
{
  "validated_request": {
    "request_id": "REQ-01",
    "quantity": 2
  },
  "json_round_trip": {
    "request_id": "REQ-01",
    "quantity": 2
  }
}
{
  "case": "invalid_json",
  "error": "JSONDecodeError",
  "line": 1,
  "column": 13
}
{
  "case": "missing_field",
  "errors": [
    {
      "location": [
        "request_id"
      ],
      "type": "missing"
    }
  ]
}
{
  "case": "wrong_type",
  "errors": [
    {
      "location": [
        "quantity"
      ],
      "type": "int_type"
    }
  ]
}
{
  "case": "out_of_range",
  "errors": [
    {
      "location": [
        "quantity"
      ],
      "type": "greater_than_equal"
    }
  ]
}
{
  "case": "blank_id",
  "errors": [
    {
      "location": [],
      "type": "value_error"
    }
  ]
}
{
  "traceback_frames": [
    {
      "function": "main",
      "line": 83
    },
    {
      "function": "read_request",
      "line": 29
    },
    {
      "function": "model_validate",
      "line": 790
    }
  ],
  "diagnosis": "Read the final validation location, then follow main -> read_request."
}
{
  "async": {
    "results_in_input_order": [
      "A",
      "B"
    ],
    "scheduling_events": [
      "A:start",
      "B:start",
      "A:end",
      "B:end"
    ]
  },
  "live_gate": "No model call belongs to setup; provider verification is in Module 01.",
  "mode": "check"
}
```
