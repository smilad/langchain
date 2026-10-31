# Module 13 exercises — cross the real protocol boundary

Read [the lessons](../lessons/13_mcp/01.md) and [the runbook](../labs/13_mcp/README.md). Do the reasoning before [solutions](../solutions/13_mcp.md).

## 1. Separate protocol roles

Draw agent → LangChain-adapted tool → MCP client/transport → FastMCP server → catalog operation. Explain tool discovery, execution, and structured results. Distinguish the wider MCP protocol's tools/resources/prompts from the capabilities implemented by this beta LangChain wrapper.

## 2. Invoke the actual local server

Run `uv run python labs/13_mcp/main.py --check`. Inspect the discovered `catalog_lookup` and `catalog_quote` tools, real notebook lookup, missing-item result, two-unit integer-cent quote, and zero-quantity tool error. Identify `ToolMessage` content, status, and structured artifact. An invalid argument is not a successful quote with a warning sentence.

## 3. Vary the request

Use a read-only tool invocation for another actual catalog item and predict stock/quantity behavior before running. Keep the function/adapter/server boundary; do not replace it with a local copied answer. Explain why a missing catalog item and an unavailable MCP server are different error classes.

## 4. Exercise failure and disconnect

Run `--check --scenario unavailable`, then `--check --scenario disconnect`. The first connects to an actual unavailable endpoint and stops; the second closes a real client context and verifies the direct client cannot call afterward. Explain why adapted tools' reentrant behavior must not be conflated with an already connected direct client. No alternate server is selected silently.

## 5. Review trust and lifecycle

State which tools are exposed, what they can read/write, where identity/authentication would be bound for a remote deployment, and who owns transport shutdown. A discovered schema/docstring is not authorization. A path target deliberately launches reviewed local code; an arbitrary model-generated filesystem path must not become executable configuration.

## 6. Optional agent integration

Only with provider consent run `--live`. Inspect actual tool messages and final source-supported catalog claims. Protocol checks can pass while a model chooses poor arguments or invents prose. Keep those quality findings separate.

**Gate:** demonstrate actual client/server calls, invalid input, unavailable transport, disconnect, and cleanup. Report the expected beta warning rather than suppressing it. Later explain the same boundaries for a new read-only tool without granting broader capabilities.
