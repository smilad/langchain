"""Actual read-only catalog MCP server; stdout belongs to the stdio protocol."""
from fastmcp import FastMCP
from langchain_learning.catalog import lookup_item, quote_total

server = FastMCP(
    "Course synthetic catalog",
    instructions="Read-only synthetic catalog. Prices are integer cents; missing items are explicit.",
    strict_input_validation=True,
    mask_error_details=True,
)


@server.tool(annotations={"readOnlyHint": True, "destructiveHint": False})
def catalog_lookup(item_id: str) -> dict:
    """Look up one synthetic catalog item by exact identifier."""
    return lookup_item(item_id)


@server.tool(annotations={"readOnlyHint": True, "destructiveHint": False})
def catalog_quote(item_id: str, quantity: int) -> dict:
    """Quote a bounded positive quantity using actual stock and integer cents."""
    return quote_total(item_id, quantity)


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
