# Module 01 solutions — boundaries and evidence

Use after [your attempt](../exercises/01_llm_baseline.md). The implemented solution is [the direct SDK lab](../labs/01_llm_baseline/main.py); this explanation does not claim a provider run. See [verification](../docs/VERIFICATION.md) for actual evidence.

## Request-path answer
`synthetic text → request_payload → OpenAI client → HTTPS request with authentication → provider generation → Response → output_text → exact-label validation → human rubric review`.

The request body contains instructions, model, input and output limit. Secret client configuration must never be printed. Python owns the payload and any explicitly stored history; model weights are not your mutable application memory. This lab sends no previous-response identifier, so separate calls do not demonstrate conversation persistence.

Deterministic stages: input size/nonblank checks, payload construction from fixed values, exact-label parsing and report formatting. Provider/model stages: accepted model capabilities, network timing, status/output and classification semantics. Reported usage comes from the response, not a guessed tokenizer. Exact future output is not proven by temperature or a successful call.

## Parser and rubric variation
A complete local parser variation, not observed generation:
```python
LABELS = {"billing", "technical", "account", "other"}

def validate_label(text: str) -> str:
    label = text.strip()
    if label not in LABELS:
        raise ValueError("output is not a permitted lowercase label")
    return label
```
A four-label cutover must also change instructions and consumer expectations. If `account` means access/identity, clarify what remains technical; otherwise you have created overlapping categories without a policy. A reasonable ambiguity policy for “My payment page crashes” is technical when the requested resolution is software malfunction, billing when it is a posted charge. Other policies are legitimate if declared and evaluated consistently. There is no universal answer supplied by label membership.

`Billing` is rejected for capitalization; `billing because…` is rejected for representation; `technical` on a double charge can pass representation while failing the rubric. Accepting every nonempty response or substituting `other` on parse error would hide the real boundary.

## Failure diagnoses
| Evidence | Stage/cause | Next action |
|---|---|---|
| missing configuration name | local prerequisite | configure privately; do not select a fake model |
| consent error | spend boundary | approve deliberately or stay in check mode |
| unavailable/unsupported model | provider capability | inspect official model/API support |
| timeout | transport/deadline | inspect request/error class; do not fix a prompt first |
| 429 | quota/rate boundary | inspect account limits and bounded retry policy |
| non-completed status | incomplete/refused/provider outcome | inspect status/full output before parsing |
| text outside labels | representation | inspect prompt/output contract, then explicitly repair |
| valid wrong label | semantic rubric/model issue | compare input and intended rubric, not just JSON |

The lab's 128-output-token limit is not a correctness guarantee and can exhaust reasoning-heavy models' output budget. Character limits are application bounds; token context/pricing require model-specific information. Elapsed time includes network/SDK and allowed retries. Cost needs reported usage plus dated pricing assumptions; null usage is not zero.

## Architecture and delayed transfer
Ordinary Python is enough for one direct classification call. Introduce LangChain when common messages, reusable composition or tool/agent wiring serves a concrete requirement. It does not replace validation, authorization or review. Compare actual envelopes, not imaginary provider equivalence.

A proper gate includes an independently changed rubric/input and a request-path explanation. If credentials are missing, retain deterministic evidence and mark live classification pending. Next-session closed-note recall and a later unfamiliar request can reveal retention; reading this solution cannot certify it.
