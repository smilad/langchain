# Module 01 lab — one direct SDK classification

The complete lab implements the direct **OpenAI Responses API**, not a LangChain model or fake classifier. It prints synthetic input/request, actual response items/text/status/model, elapsed client time and provider-reported usage. [Lessons](../../lessons/01_llm_baseline/01.md) explain the boundary; [exercise](../../exercises/01_llm_baseline.md) and [solution](../../solutions/01_llm_baseline.md) are separate.

## Safe default
```sh
uv run python labs/01_llm_baseline/main.py --check
```
This invokes no model. It exercises actual request construction, 4000-character/nonblank input limits and exact-label parser acceptance/rejection. Authored strings are explicitly parser fixtures; they do not classify user text or demonstrate model behavior. `--text` applies only to the live request; check mode runs the fixed boundary suite.

## Real request, only after deliberate approval
Use the private `.env` setup described in the root README. Configure `OPENAI_API_KEY`, a Responses-capable `COURSE_MODEL`, and `COURSE_ALLOW_LIVE=1` only after approving remote transmission/billing. Never copy secrets into published commands or evidence.
```sh
uv run python labs/01_llm_baseline/main.py --live --text "The sign-in page crashes."
```
One initial request is made; configured SDK policy permits one transport retry. Output budget is 128 tokens, which can be insufficient for reasoning-heavy models; an incomplete response is reported and rejected, not silently retried until success. The direct baseline omits temperature because accepted controls vary by model. Choose a suitable small classification model through official capability/pricing documentation.

## Cases and interpretation
- Double charge: rubric suggests billing; actual output must still be reviewed.
- Crashing sign-in page: rubric suggests technical.
- Poetry request: rubric suggests other.
- Blank/oversized text: rejected before transport.
- `Billing`, explanation prose, empty response or JSON-shaped label: rejected by the exact-label parser.
- Missing configuration/consent, timeout, API error or rate limit: explicit nonzero error; never a default label.
- Completed but wrong label: semantic/model/rubric failure, not transport success as correctness.

Elapsed time includes the SDK/network and allowed retry. Usage may be null. No dollar estimate is invented; calculate cost only with dated pricing and the reported usage categories. Full output may include reasoning or refusal items, so `output[0]` is not assumed to contain text. Only synthetic inputs belong in this printable report.

## Evidence, compatibility, state
Installed authoring snapshot: Python 3.14.0/OpenAI SDK 3.29.0; exact dependencies are in `uv.lock`. [Verification](../../docs/VERIFICATION.md) records actual gateway-mediated Responses classification (`billing`, 79 reported tokens) and direct-public-endpoint limits. No state is persisted and no reset is needed. Check mode does not contact a remote endpoint; live requires privately configured Responses-capable access and consent. Review data-retention and optional hosted-tracing configuration before using real data.

Primary references checked 2026-10-12: [SDK](https://github.com/openai/openai-python), [text generation](https://platform.openai.com/docs/guides/text), [Responses](https://platform.openai.com/docs/api-reference/responses).
