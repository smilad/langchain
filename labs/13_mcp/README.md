# Module 13 lab — Actual FastMCP stdio integration

## Setup and commands
Use the locked environment, not a tutorial's older adapter imports:

```sh
uv sync --locked
uv run python labs/13_mcp/main.py --check
uv run python labs/13_mcp/main.py --check --scenario unavailable
uv run python labs/13_mcp/main.py --check --scenario disconnect
```

Installed baseline: Python 3.14.0, `langchain[mcp]` 1.4.4 and FastMCP 4.1.0. [MCPAdapter documentation](https://docs.langchain.com/oss/python/langchain/mcp) calls `langchain.mcp` beta; its warning is intentional, not suppressed. Exact versions/hashes are in [uv.lock](../../uv.lock), actual execution evidence in [verification](../../docs/VERIFICATION.md).

The real server entrypoint is:

```sh
uv run python -m langchain_learning.mcp_server
```

That command waits for MCP protocol input. It is not an HTTP endpoint and does not print a catalog as ordinary CLI prose. Usually let the adapter launch the repository-owned script automatically. All server stdout belongs to stdio protocol; use stderr for diagnostics. The server requires no model or credentials.

## Normal model-free path
`MCPAdapter(Path(...))` starts an actual local subprocess and discovers exactly `catalog_lookup` and `catalog_quote`. The lab invokes the adapted LangChain tools with real tool-call IDs, inspects ToolMessages and structured artifacts, and checks:

- `notebook` resolves from actual `data/catalog.json`;
- `absent` is an explicit missing-item result, not an invented record;
- two notebooks quote 2598 USD cents from the fixture;
- zero quantity produces a server-reported error status.

No in-memory server, fake tool, or generated model answer substitutes for this path. Read-only annotations declare intent; only the actual registered functions enforce capability. Quantity/domain validation also protects direct Python callers.

## Actual agent path
With privately configured key/model and explicit consent:

```sh
uv run python labs/13_mcp/main.py --live
```

The live agent uses discovered MCP tools, is bounded to four model/three tool calls plus a recursion limit, and must produce at least one actual MCP ToolMessage. Inspect requested arguments, result artifacts, and final prose; a connected tool is not automatically trusted. Prices/stock remain catalog facts, not model guesses. Provider usage/cost and failures are genuine live prerequisites; no remote unreviewed tools or production credentials are needed.

## Lifecycle and failure cases
`unavailable` attempts a real localhost connection at port 1 with a five-second timeout and reports the exception category. If that port unexpectedly hosts MCP, choose an unused endpoint before drawing conclusions. `disconnect` starts the actual stdio server with a direct FastMCP Client, calls lookup, exits its context, verifies disconnection, and demonstrates a failing direct call afterward. This differs from adapted tools: they can intentionally reconnect after discovery exits.

Normal mode releases its adapter context after all calls; disconnect mode releases a direct client context. Both exercise real transport cleanup. Neither asserts arbitrary remote-server process shutdown. Tools expose synthetic data only; no persistent state/reset is required. If an interpreter/import fails, run `uv sync --locked` and inspect the real server stderr rather than hiding it behind a model fallback.

See [lessons](../../lessons/13_mcp/01.md), [exercise](../../exercises/13_mcp.md), and [solutions](../../solutions/13_mcp.md).

## Captured `--check` output

Real output of `uv run python labs/13_mcp/main.py --check` (no credentials, no network; machine paths replaced by `<repo>`). Compare your own run against it.

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
  "api_note": "langchain.mcp is beta in LangChain>=1.4; lockfile is baseline."
}
... (78 lines omitted)
    },
    "status": "success"
  },
  "invalid_quantity": {
    "content": [
      {
        "type": "text",
        "text": "Error calling tool 'catalog_quote'",
        "id": "lc_0a413475-3782-48bf-a558-1b72423912d0"
      }
    ],
    "additional_kwargs": {},
    "response_metadata": {},
    "type": "tool",
    "name": "catalog_quote",
    "id": null,
    "tool_call_id": "invalid",
    "artifact": null,
    "status": "error"
  }
}
{
  "lifecycle": "Adapter context exited; stdio connection released.",
  "live_gate": "Agent generation not exercised."
}
[+103 hidden: rtk recall bd7c5d57ea70]
  from langchain.mcp import MCPAdapter


╭──────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│                                                                              │
│                         ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█                        │
│                         █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀                        │
│                                                                              │
│                                                                              │
│                                                                              │
│                                FastMCP 4.1.0                                 │
│                            https://gofastmcp.com                             │
│                                                                              │
│               🖥  Server:      Course synthetic catalog, 4.1.0                │
│               🚀 Deploy free: https://horizon.prefect.io                     │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────╮
│                          🎉 Update available: 4.1.4                          │
│                      Run: pip install --upgrade fastmcp                      │
╰──────────────────────────────────────────────────────────────────────────────╯


... (46 lines omitted)
                    ╭─────────── Traceback (most recent call last) ────────────╮
                    │ <repo>/.venv/li │
                    │ b/python3.14/site-packages/fastmcp/server/server.py:1467 │
                    │  in call_tool                                            │
                    │                                                          │
                    │ <repo>/.venv/li │
                    │ b/python3.14/site-packages/fastmcp/tools/base.py:440 in  │
                    │ _run                                                     │
                    │                                                          │
                    │                 ... 9 frames hidden ...                  │
                    │                                                          │
                    │ <repo>/.venv/li │
                    │ b/python3.14/site-packages/fastmcp/tools/function_tool.p │
                    │ y:96 in wrapper                                          │
... (truncated)
```
