"""Project A: deterministic tool contracts, then an explicitly paid agent run."""

from langgraph.errors import GraphRecursionError
from pydantic import ValidationError

from langchain_learning.catalog import MAX_QUANTITY, build_catalog_agent, catalog_tools
from langchain_learning.runtime import DATA, emit, lab_parser, preflight, run_lab


LIVE_CASES = {
    "normal": "Look up notebook and quote exactly 2 units. Report the total in cents.",
    "missing": "Look up invisible-widget. Do not substitute another product.",
    "invalid": "Quote notebook with quantity -2. Explain why that request cannot be fulfilled.",
    "bounded": "Use lookup_item to look up notebook, then quote exactly 2 units.",
}


def check() -> None:
    before = (DATA / "catalog.json").read_bytes()
    lookup, quote = catalog_tools()
    emit({"tool_schemas": {t.name: t.args_schema.model_json_schema() for t in (lookup, quote)}})
    normal = lookup.invoke({"item_id": "notebook"})
    total = quote.invoke({"item_id": "notebook", "quantity": 2})
    missing = lookup.invoke({"item_id": "invisible-widget"})
    missing_quote = quote.invoke({"item_id": "invisible-widget", "quantity": 1})
    stock_boundary = quote.invoke({"item_id": "desk-lamp", "quantity": 3})
    over_stock = quote.invoke({"item_id": "desk-lamp", "quantity": 4})
    sold_out = quote.invoke({"item_id": "sold-out", "quantity": 1})
    max_quote = quote.invoke({"item_id": "pen-set", "quantity": MAX_QUANTITY})
    assert normal["found"] and total["total_cents"] == normal["price_cents"] * 2
    assert missing == {"found": False, "item_id": "invisible-widget"}
    assert not missing_quote["quoted"] and missing_quote["reason"] == "item_unavailable"
    assert stock_boundary["quoted"] and max_quote["quoted"]
    assert not over_stock["quoted"] and not sold_out["quoted"]
    invalid_cases = [0, -1, MAX_QUANTITY + 1, True, 1.5, "2"]
    rejected = []
    for quantity in invalid_cases:
        try:
            quote.invoke({"item_id": "notebook", "quantity": quantity})
        except ValidationError as error:
            rejected.append({"quantity": quantity, "error_types": [e["type"] for e in error.errors()]})
        else:
            raise AssertionError("Invalid quantity reached the quote body")
    for arguments in ({"item_id": "../catalog.json"}, {"item_id": "notebook", "path": "other.json"}):
        try:
            lookup.invoke(arguments)
        except ValidationError:
            pass
        else:
            raise AssertionError("Invalid lookup schema accepted")
    assert (DATA / "catalog.json").read_bytes() == before, "Read-only tools changed the catalog"
    emit({"normal": normal, "quote": total, "missing": missing, "missing_quote": missing_quote,
          "stock_boundary": stock_boundary, "over_stock": over_stock, "sold_out": sold_out,
          "max_quantity": max_quote, "invalid_arguments": rejected,
          "live_gate": "Not exercised: real model tool choice, final factual answer, agent step bound"})


def live(case: str) -> None:
    agent = build_catalog_agent()
    limit = 1 if case == "bounded" else 8
    emit({"case": case, "recursion_limit": limit, "input": LIVE_CASES[case]})
    try:
        for update in agent.stream(
            {"messages": [{"role": "user", "content": LIVE_CASES[case]}]},
            config={"recursion_limit": limit},
            stream_mode="updates",
        ):
            emit({"intermediate_update": update})
    except GraphRecursionError:
        emit({"status": "step_budget_exhausted", "note": "No fabricated final answer; inspect partial trace."})
        if case != "bounded":
            raise
    else:
        emit({"status": "terminated_within_budget", "note": "Review tool arguments/results and final support manually."})


def main() -> None:
    parser = lab_parser("Read-only catalog tools and bounded real agent")
    parser.add_argument("--case", choices=LIVE_CASES, default="normal")
    args = parser.parse_args()
    emit(preflight())
    live(args.case) if args.live else check()


if __name__ == "__main__":
    run_lab(main)
