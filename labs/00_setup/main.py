"""No-network Python and environment diagnostic; run with uv run python ... --check."""
from __future__ import annotations

import asyncio
import json
import os
import traceback
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from langchain_learning.runtime import ROOT, emit, lab_parser, preflight, run_lab


class Request(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    request_id: str = Field(min_length=1)
    quantity: int = Field(ge=1, le=20)

    @model_validator(mode="after")
    def nonblank_id(self) -> Self:
        if not self.request_id.strip():
            raise ValueError("request_id must not be blank")
        return self


def read_request(raw: str) -> Request:
    """Decode untrusted JSON, then validate its application contract."""
    return Request.model_validate(json.loads(raw))


def config_presence() -> dict[str, bool]:
    return {name: bool(os.environ.get(name)) for name in ("OPENAI_API_KEY", "COURSE_MODEL")}


async def cooperative_work(name: str, events: list[str]) -> str:
    events.append(f"{name}:start")
    await asyncio.sleep(0)  # A genuine scheduling point, not a simulated API response.
    events.append(f"{name}:end")
    return name


async def async_demo() -> dict:
    events: list[str] = []
    results = await asyncio.gather(cooperative_work("A", events), cooperative_work("B", events))
    assert sorted(results) == ["A", "B"]
    assert events.index("B:start") < events.index("A:end")
    return {"results_in_input_order": results, "scheduling_events": events}


def main() -> None:
    args = lab_parser(__doc__).parse_args()
    report = preflight()
    emit({"preflight": report, "configuration_present": config_presence()})
    import langchain

    origin = langchain.__file__
    if origin is None:
        raise ValueError("langchain has no inspectable import origin")
    from pathlib import Path

    if Path(origin).resolve().is_relative_to(ROOT / "src"):
        raise ValueError("langchain resolves to local source instead of the external library")
    valid = read_request('{"request_id":"REQ-01","quantity":2}')
    emit({"validated_request": valid, "json_round_trip": json.loads(valid.model_dump_json())})
    invalid = [
        ("invalid_json", '{"quantity":'),
        ("missing_field", '{"quantity":2}'),
        ("wrong_type", '{"request_id":"REQ-02","quantity":"2"}'),
        ("out_of_range", '{"request_id":"REQ-03","quantity":0}'),
        ("blank_id", '{"request_id":" ","quantity":1}'),
    ]
    for case, raw in invalid:
        try:
            read_request(raw)
        except json.JSONDecodeError as error:
            emit({"case": case, "error": type(error).__name__, "line": error.lineno, "column": error.colno})
        except ValidationError as error:
            emit({"case": case, "errors": [{"location": e["loc"], "type": e["type"]} for e in error.errors()]})
        else:
            raise AssertionError(f"invalid case accepted: {case}")
    try:
        read_request('{"request_id":"REQ-trace","quantity":-1}')
    except ValidationError as error:
        frames = traceback.extract_tb(error.__traceback__)
        emit({"traceback_frames": [{"function": frame.name, "line": frame.lineno} for frame in frames],
              "diagnosis": "Read the final validation location, then follow main -> read_request."})
    emit({"async": asyncio.run(async_demo()), "live_gate": "No model call belongs to setup; provider verification is in Module 01.",
          "mode": "live requested; setup still sends no request" if args.live else "check"})


if __name__ == "__main__":
    run_lab(main)
