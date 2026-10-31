# Module 03 solutions — typed does not mean true

Read after [an independent attempt](../exercises/03_structured_output.md). [The complete lab](../labs/03_structured_output/main.py) implements SupportRecord, local parser/source composition and real model/agent branches. Actual proof lives in [verification](../docs/VERIFICATION.md), not in an illustrative answer below.

## Required-nullable and outcome reasoning
`order_id: str | None` without a default is required but permits null. Omitting the field is different from admitting that its value is unavailable. A supported record requires identifier/category/quote; unknown/contradictory/irrelevant cannot select an order or quote. Irrelevant also cannot claim a support category. Cross-field validators enforce those relationships; source validation separately verifies identifier and quote membership.

Complete source with one explicit order can yield supported. Missing order should yield unknown, conflicting distinct orders contradictory and poetry irrelevant. These are rubric expectations, not fabricated model observations. A cautious unknown may be acceptable when semantics are ambiguous; an invented order is never repaired by having a valid schema.

## Booking-domain source guard
After migrating the schema/instructions to BOOK identifiers, this complete guard illustrates the independent change:
```python
import re

def check_booking(record, source: str):
    ids = set(re.findall(r"\bBOOK-[0-9]{4}\b", source))
    if len(ids) > 1 and record.status != "contradictory":
        raise ValueError("ambiguous booking source")
    if record.status == "contradictory" and len(ids) <= 1:
        raise ValueError("unsupported contradiction")
    if record.status == "supported":
        if ids != {record.booking_id}:
            raise ValueError("booking identifier absent or ambiguous")
        quote = record.evidence_quote
        if not quote or quote not in source or record.booking_id not in quote:
            raise ValueError("quote does not support selected booking")
    return record
```
The corresponding schema must still require supported ID/category/quote, enforce `BOOK-` plus four digits and forbid selected IDs/quotes in other outcomes. The guard alone is not a complete schema. A substring such as “please refund” is genuine source text but insufficient evidence for `BOOK-1204` because it lacks the identifier. Selecting the first of two IDs silently solves a different problem.

## Composition and strategy answers
Local LCEL: authored JSON string → PydanticOutputParser → source guard → typed record. Live LCEL: exact input dictionary → normalization → parallel original-source retention and prompt→structured model → raw/parse-error inspection → source guard → consumer result. Runnable composition changes wiring, not validation truth. Lambdas may buffer streams, so token streaming is not guaranteed by the pipe symbol.

Model-level structured output returns parsed data or, with include_raw, a raw/parsed/parsing_error envelope. Agent output places the typed result in `structured_response` alongside messages. ProviderStrategy requests native schema support; ToolStrategy represents the response using function arguments. No business action follows merely from this representation. This lab disables tool-strategy automatic error correction and bounds agent recursion. Unsupported capabilities must remain errors, not fake fallback responses.

## Failure-feedback answer
Missing key/blank input fails before transport. Missing nullable fields or invalid enums fail shape validation. Inconsistent supported/null combinations fail the model validator. Fabricated ID/quote and choosing among conflicts fail the source guard. Wrong category/relevance can survive literal checks and therefore needs human semantic review. A retry cannot recover an identifier absent from source; get more evidence or abstain.

Exit evidence must include all named cases, strategy explanation, a changed domain and a diagnosis. If live access is unavailable, mark those branches pending and demonstrate reachable deterministic boundaries. Review later with a new optionality/evidence constraint before using schemas as a grounding mechanism in Module 07.
