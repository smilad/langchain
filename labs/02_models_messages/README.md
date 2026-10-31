# Module 02 lab — common messages, real execution modes

Rebuild the three-label classifier using `ChatOpenAI` through the shared runtime. The lab exposes raw content, normalized blocks, text, tool calls, usage and metadata separately. It delivers an exact permitted label or prints the rejected envelope and raises an error; label membership still does not prove semantic correctness. Read [lessons](../../lessons/02_models_messages/01.md), then [exercise](../../exercises/02_models_messages.md); [solutions](../../solutions/02_models_messages.md) explain failure stages.

## Local check
```sh
uv run python labs/02_models_messages/main.py --check
```
The check actually renders a prompt, verifies missing-variable failure and literal braces, projects text from authored blocks, constructs a tool-result envelope and combines authored message chunks including a usage-only chunk. It also validates the accumulated label and rejects explanation prose. Those are **data fixtures, not a mock model or invented API result**. Nonblank/4000-character limits are exercised. No remote client is created.

## Live paths and spend
Configure the private environment and explicit budget consent as in Module 01. The selected model must accept temperature zero and support the selected execution mode. These commands are implemented but unverified until actual execution:
```sh
uv run python labs/02_models_messages/main.py --live --mode invoke
uv run python labs/02_models_messages/main.py --live --mode stream --interactive
uv run python labs/02_models_messages/main.py --live --mode async --text "The app crashes."
uv run python labs/02_models_messages/main.py --live --mode batch
```
`invoke`, `stream` and `async` each make one initial request. `batch` makes two, capped at two concurrent calls. `--mode all` makes **five**, not one; any allowed SDK retry is additional. The interactive mode reads exactly one line, not a perpetual paid loop. `--interactive` without `--live --mode stream` is rejected. Model output limits use provider/runtime defaults here; there is no claimed universal cost ceiling.

## Inspection and failure cases
Streaming text goes to stderr as chunks arrive; structured complete-response inspection goes to stdout after aggregation. Preserve all chunks including empty metadata chunks. A midstream error must remain a failed run, not accepted partial classification. No tool executes in this lab: an authored ToolMessage teaches the envelope only.

Batch responses retain input order, not completion order. Only whole-batch duration is measured; per-response duration is null. Client-side batch is not a provider Batch API or cost discount. Async awaits native model I/O; it does not make CPU-heavy Python nonblocking. Report missing usage as unavailable, especially with custom compatible endpoints. Common interfaces do not imply identical multimodal or provider-specific fields.

## Evidence and state
Installed authoring snapshot: Python 3.14.0, LangChain 1.4.4, langchain-core 1.6.9/langchain-openai 1.7.0. [Verification](../../docs/VERIFICATION.md) records actual gateway-mediated invoke, stream aggregation, async, and batch. The gateway buffers streams; real-time delivery and interactive input remain unverified. Exact versions live in `uv.lock` and actual preflight. No state is written, so there is nothing to reset. Configure compatible private access/consent; disable/review hosted tracing before sending private content.

Sources checked 2026-10-12: [models](https://docs.langchain.com/oss/python/langchain/models), [messages](https://docs.langchain.com/oss/python/langchain/messages), [ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai).
