"""Common setup for the course's real local and explicitly opted-in remote labs."""

import argparse
import json
import os
import platform
import sys
from collections.abc import Callable
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def load_environment() -> None:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env", override=False)


def state_dir() -> Path:
    load_environment()
    path = Path(os.getenv("COURSE_STATE_DIR", str(ROOT / ".course"))).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def model_settings() -> dict:
    """Require explicit consent; this return value contains a secret: never emit it."""
    load_environment()
    missing = [name for name in ("OPENAI_API_KEY", "COURSE_MODEL") if not os.getenv(name)]
    if missing:
        raise ValueError("Live model configuration missing: " + ", ".join(missing))
    if os.getenv("COURSE_ALLOW_LIVE") != "1":
        raise PermissionError("Remote calls require COURSE_ALLOW_LIVE=1 and your provider budget approval")
    return {
        "model": os.environ["COURSE_MODEL"],
        "api_key": os.environ["OPENAI_API_KEY"],
        "timeout": 30.0,
        "max_retries": 1,
    }


def get_model():
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(**model_settings(), temperature=0)


def preflight() -> dict:
    """Report availability, not credential values; this never calls a model."""
    load_environment()
    packages = (
        "langchain", "langchain-core", "langchain-openai", "langgraph",
        "langgraph-checkpoint-sqlite", "fastmcp", "pydantic",
    )
    versions = {}
    for package in packages:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    try:
        import langchain
        origin = str(Path(langchain.__file__).resolve())
    except ImportError:
        origin = None
    return {
        "python": platform.python_version(),
        "interpreter": sys.executable,
        "packages": versions,
        "langchain_origin": origin,
        "configured": {
            "api_key": bool(os.getenv("OPENAI_API_KEY")),
            "model": bool(os.getenv("COURSE_MODEL")),
            "live_consent": os.getenv("COURSE_ALLOW_LIVE") == "1",
            "custom_endpoint": bool(os.getenv("OPENAI_BASE_URL")),
            "hosted_tracing": os.getenv("LANGSMITH_TRACING", "false").lower() == "true",
        },
        "live_request_sent": False,
    }


def lab_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Run real local checks; no paid model request")
    mode.add_argument("--live", action="store_true", help="Run model-dependent paths with explicit configured consent")
    return parser


def _json_value(value):
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (set, tuple)):
        return list(value)
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def emit(value) -> None:
    print(json.dumps(value, default=_json_value, ensure_ascii=False, indent=2))


def _safe_error(error: Exception) -> str:
    text = str(error)
    for key, value in os.environ.items():
        if value and key.endswith("_API_KEY"):
            text = text.replace(value, "[redacted]")
    return f"{type(error).__name__}: {text}"


def run_lab(fn: Callable[[], None]) -> None:
    from openai import APIError

    try:
        fn()
    except (ValueError, PermissionError, FileNotFoundError, APIError) as error:
        print(_safe_error(error), file=sys.stderr)
        raise SystemExit(2) from error
