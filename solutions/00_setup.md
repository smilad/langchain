# Module 00 solutions — reasoning before repairs

Use after a genuine [diagnostic attempt](../exercises/00_setup.md), not as evidence of independent mastery. The complete executable diagnostic is [main.py](../labs/00_setup/main.py). Runtime proof is recorded separately in [verification](../docs/VERIFICATION.md).

## Recall corrections
A checkout directory name is not necessarily an import name. Python's selected environment/import paths determine where `langchain` resolves. Metadata permits dependency ranges; the lock records exact versions/hashes; installed files are what your interpreter actually executes. An annotation is documentation/static-tool input, not automatic runtime validation. `async def` does not make a blocking function cooperative.

## A changed typed JSON boundary
This illustrative complete variation can be copied into your own scratch file after an attempt; it is not reported as executed course evidence:
```python
import json
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

class Ticket(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    ticket_id: str = Field(min_length=1, max_length=40)
    priority: int = Field(ge=1, le=3)

    @field_validator("ticket_id")
    @classmethod
    def nonblank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("ticket_id must not be blank")
        return value

def read_ticket(raw: str) -> Ticket:
    return Ticket.model_validate(json.loads(raw))

for raw in ['{"ticket_id":"T-01","priority":2}',
            '{"priority":2}', '{"ticket_id":"T-02","priority":4}']:
    try:
        print(read_ticket(raw).model_dump())
    except json.JSONDecodeError as error:
        print("invalid JSON", error.lineno, error.colno)
    except ValidationError as error:
        print([{"location": e["loc"], "type": e["type"]} for e in error.errors()])
```
The decoder must run before model validation because the schema expects a Python value. Missing ID and priority 4 fail different field rules; valid syntax alone proves neither. Strict mode deliberately rejects string priority. Returning a default Ticket in `except` would erase the failure and mislead consumers.

Environment reporting should be `bool(os.environ.get(name))`, never the value. A harmless synthetic variable suffices to prove the boundary. The lab's preflight reports presence and import origin; it does not authenticate with a provider.

## Diagnosis feedback
- **Goal:** reproduce the environment. **Observation:** IDE import fails but `uv run` succeeds. **Hypothesis:** interpreter mismatch. **Next action:** compare `sys.executable`/preflight paths and select the project interpreter before reinstalling anything.
- **Goal:** accept positive quantity. **Observation:** validation points to `quantity`. **Cause:** declared lower bound. **Next action:** follow `main → read_request`; repair input or revise the legitimate contract, not dependency installation.
- **Goal:** cooperative concurrency. **Observation:** tasks run one after another without an await. **Cause:** no yielding point. **Next action:** inspect the actual blocking operation; choose an async client or explicit offload where appropriate.

HTTP timeout means no timely response, not proof that the server made no change. HTTP 429 means rate/quota pressure; a completed wrong label means application/model semantics. These demand different repairs.

## Gate and remediation
Demonstrate changed schemas, invalid cases, safe environment reporting and interpreter ownership. Solution-assisted execution is practice, not independent evidence. A new Python learner may need much more than 3–5 hours: use functions/dictionaries → JSON/exceptions → environments → schema → HTTP → async as a remediation sequence, with a fresh reassessment after each gap. Delayed review should ask a new domain/constraint, not repeat the same source. No credential is needed until Module 01's explicitly approved live gate.
