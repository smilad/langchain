"""Launch actual FastMCP stdio server and invoke adapted tools with/without a model."""
import asyncio
from pathlib import Path

from fastmcp import Client
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_core.messages import ToolMessage

from langchain_learning.advanced import limits
from langchain_learning.runtime import ROOT, emit, get_model, lab_parser, preflight, run_lab

SERVER = ROOT / "src" / "langchain_learning" / "mcp_server.py"


async def invoke_tool(tools: list, name: str, arguments: dict, call_id: str) -> ToolMessage:
    tool = next(item for item in tools if item.name == name)
    message = await tool.ainvoke({"name": name, "args": arguments, "id": call_id, "type": "tool_call"})
    if not isinstance(message, ToolMessage):
        raise TypeError("Expected actual MCP ToolMessage")
    return message


async def connected(args) -> None:
    async with asyncio.timeout(60):
        async with MCPAdapter(SERVER) as adapter:
            tools = await adapter.list_tools()
            names = sorted(tool.name for tool in tools)
            if names != ["catalog_lookup", "catalog_quote"]:
                raise ValueError("Unexpected server capability catalog")
            found = await invoke_tool(tools, "catalog_lookup", {"item_id": "notebook"}, "found")
            missing = await invoke_tool(tools, "catalog_lookup", {"item_id": "absent"}, "missing")
            quote = await invoke_tool(tools, "catalog_quote", {"item_id": "notebook", "quantity": 2}, "quote")
            invalid = await invoke_tool(tools, "catalog_quote", {"item_id": "notebook", "quantity": 0}, "invalid")
            if found.status != "success" or quote.status != "success" or invalid.status != "error":
                raise AssertionError("MCP success/error contract differs from expected")
            # Inspect real structured artifacts, not invented output or copied doc examples.
            def structured(message):
                if message.artifact is None:
                    raise ValueError("Catalog server did not return structured content")
                return message.artifact["structured_content"]
            if structured(found)["item_id"] != "notebook" or structured(missing)["found"] is not False:
                raise AssertionError("Wrong real catalog lookup result")
            if structured(quote)["total_cents"] != 2598:
                raise AssertionError("Wrong integer quote")
            emit({"discovered_tools": names, "lookup": found, "missing": missing,
                  "quote": quote, "invalid_quantity": invalid})
            if args.live:
                agent = create_agent(get_model(), tools, middleware=limits(4, 3),
                                     system_prompt="Use actual catalog tools. Never invent stock, item or price. "
                                                   "All tools are read-only; report unavailable items explicitly.")
                result = await agent.ainvoke({"messages": [{"role": "user", "content":
                    "Look up notebook, quote two units, and tell me if absent is in the catalog."}]},
                    {"recursion_limit": 12})
                messages = result["messages"]
                if not any(isinstance(message, ToolMessage) for message in messages):
                    raise ValueError("Agent did not invoke an actual MCP tool")
                emit({"agent_messages": messages})
        emit({"lifecycle": "Adapter context exited; stdio connection released.",
              "live_gate": "Real agent invocation executed" if args.live else "Agent generation not exercised."})


async def unavailable() -> None:
    # Real failed TCP connection, not a fake server response. Port 1 should have no course server.
    try:
        async with asyncio.timeout(5):
            async with MCPAdapter("http://127.0.0.1:1/mcp") as adapter:
                await adapter.list_tools()
    except Exception as exc:
        emit({"scenario": "unavailable", "error_type": type(exc).__name__,
              "decision": "Stop; no automatic alternate tool/server."})
        return
    raise RuntimeError("Port 1 unexpectedly served MCP; choose an unused endpoint")


async def disconnect() -> None:
    # Closing a real client's context releases stdio transport. Calls outside that context
    # must fail for Client directly; adapted tools are deliberately reentrant (can reconnect).
    client = Client(SERVER)
    async with asyncio.timeout(30):
        async with client:
            result = await client.call_tool("catalog_lookup", {"item_id": "notebook"})
            emit({"before_disconnect": result.data})
        if client.is_connected():
            raise AssertionError("Client remained connected after context exit")
        try:
            await client.call_tool("catalog_lookup", {"item_id": "notebook"})
        except Exception as exc:
            emit({"scenario": "disconnect", "connected": client.is_connected(),
                  "post_disconnect_error_type": type(exc).__name__, "clean_context_exit": True})
        else:
            raise AssertionError("Direct Client unexpectedly accepted a disconnected call")


def main() -> None:
    parser = lab_parser(__doc__)
    parser.add_argument("--scenario", choices=["normal", "unavailable", "disconnect"], default="normal")
    args = parser.parse_args()
    emit({"preflight": preflight(), "api_note": "langchain.mcp is beta in LangChain>=1.4; lockfile is baseline."})
    if args.scenario == "unavailable":
        asyncio.run(unavailable())
    elif args.scenario == "disconnect":
        asyncio.run(disconnect())
    else:
        asyncio.run(connected(args))


if __name__ == "__main__":
    run_lab(main)
