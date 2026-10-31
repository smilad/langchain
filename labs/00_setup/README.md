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
