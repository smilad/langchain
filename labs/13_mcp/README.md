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
