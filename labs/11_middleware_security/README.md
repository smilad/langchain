# Module 11 — security boundaries and real middleware

Setup: `uv sync --locked`; [lessons](../../lessons/11_middleware_security/01.md); Python >=3.14 and [exact versions](../../uv.lock). [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom) and [tools](https://docs.langchain.com/oss/python/langchain/tools), checked 2026-10-12.

```sh
uv run python labs/11_middleware_security/main.py --check
uv run python labs/11_middleware_security/main.py --live
```

Check uses real temporary durable workflows for alice/bob, retrieves MALICIOUS from the corpus, confirms finance exclusion for alice, checks authorized status projection, denies cross-owner inspection, extra owner arguments, secret reading and approval capabilities, and inspects actual zero action counts. It also runs a deliberately unsafe non-model fixture: document text grants permission and releases ONLY a committed synthetic marker. This counterexample is not a model leakage observation and never reads credentials.

Live additionally invokes actual `create_agent` with AuthorizationMiddleware, ModelCallLimitMiddleware and ToolCallLimitMiddleware. Provider config/consent and tool calling are required. Inspect all model/tool messages: an unattempted attack, an attempted-and-denied tool call and a model refusal are different evidence. No fake model or fallback exists. The secure tool has no identity argument and receives immutable trusted runtime context; the domain function and workflow repeat ownership checks independently of middleware.

## Gate report

For each case record requested capability, trusted actor, exact synthetic source/input, actual tool execution outcome, action count, versioned model/prompt configuration and declared trial count. Prove denied operations cannot produce effects. Evaluate semantic contamination separately: valid source IDs or no unauthorized actions do not prove grounded wording. Minimize/redact before provider calls; final-display redaction cannot undo upstream disclosure. Never upload private traces without permission.

`--check` proves deterministic boundaries but does not traverse live model middleware. `--live` proves whatever actual messages show, not immunity against every injection. The synthetic secret is not available to secure model context or tool capabilities; this is least privilege rather than successful detection of every secret-request phrasing. Local identity arguments are trusted demonstrations, not login credentials.

**Evidence status:** [verification](../../docs/VERIFICATION.md) records actual local commands/outcomes separately from unavailable live proof. Installed baseline: Python 3.14.0, LangChain 1.4.4, langchain-core 1.6.9, LangGraph 1.2.14, langchain-openai 1.7.0, Pydantic 2.14.1. Temporary state is removed after connections close. [Independent exercise](../../exercises/11_middleware_security.md), [reasoned solution](../../solutions/11_middleware_security.md).
