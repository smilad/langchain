"""Navigate the checkout's lessons and run their documented Python labs."""

import argparse
import runpy
import sys

from .runtime import ROOT, emit, preflight

MODULES = (
    "00_setup", "01_llm_baseline", "02_models_messages", "03_structured_output",
    "04_tools_agents", "05_memory_context", "06_retrieval", "07_rag",
    "08_evaluation", "09_graph_workflows", "10_durable_approval", "11_middleware_security",
    "12_multi_agent", "13_mcp", "14_production", "15_capstone",
)


def main() -> None:
    parser = argparse.ArgumentParser(description="LangChain learning course: local checks and explicitly opted-in live labs")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Show module lesson and lab locations")
    commands.add_parser("check", help="Check interpreter and installed integrations without a model request")
    run = commands.add_parser("run", help="Run a module lab, passing its remaining arguments")
    run.add_argument("module", help="Module number 00-15 or full module directory name")
    run.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command == "check":
        emit(preflight())
    elif args.command == "list":
        for module in MODULES:
            print(f"{module}: lessons/{module}/01.md | labs/{module}/main.py")
    else:
        module = next((name for name in MODULES if args.module in (name, name[:2])), None)
        if module is None:
            parser.error("module must be 00-15 or one of the names shown by list")
        path = ROOT / "labs" / module / "main.py"
        if not path.is_file():
            parser.error(f"Module lab is missing: {path}")
        sys.argv = [str(path), *args.arguments]
        runpy.run_path(str(path), run_name="__main__")
