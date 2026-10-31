# Module 02 solutions — representation versus execution

Consult after the [exercise](../exercises/02_models_messages.md). [The runnable lab](../labs/02_models_messages/main.py) implements actual local message operations and separate live execution methods; no fake model substitutes for credentials. [Verification](../docs/VERIFICATION.md) records what actually ran.

## Package and role corrections
`langchain_learning` is this course. `langchain-core` supplies prompt/message/Runnable interfaces. `langchain-openai` supplies ChatOpenAI; its SDK handles provider transport. `langchain` exposes the higher-level agent harness. Identical method names do not imply identical capabilities.

A template's `invoke` is local rendering. A model's `invoke` is remote generation. System instructions define the attempt; HumanMessage holds user data. AIMessage can contain generated output or explicitly authored history/fixtures, so provenance must be stated. ToolMessage links an execution result to a call ID; it does not cause that execution. Message roles do not grant permissions.

## Prompt variation
This complete local variation illustrates the missing-context exercise:
```python
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify using this application rubric: {context}"),
    ("human", "{text}"),
])
value = prompt.invoke({
    "context": "billing=invoices; technical=software faults; other=everything else",
    "text": "Literal braces {quantity}; my app crashes.",
})
messages = value.to_messages()
```
`context` here must be trusted application configuration; untrusted text remains in the human slot. Rendering braces in a supplied value does not recursively parse them. That is a formatting property, not immunity to adversarial instructions. Supplying `request` instead of `text` is a deterministic missing-variable error before transport.

## Chunk reconstruction answer
```python
from langchain_core.messages import AIMessageChunk
chunks = [AIMessageChunk(content="tech"), AIMessageChunk(content="nical"),
          AIMessageChunk(content="", usage_metadata={
              "input_tokens": 3, "output_tokens": 2, "total_tokens": 5})]
full = None
for chunk in chunks:
    full = chunk if full is None else full + chunk
```
These are authored exercise values, not provider token counts. Adding full chunks preserves information that `''.join(chunk.text for chunk in chunks)` loses. Display `text`, inspect `content`/`content_blocks`/tool calls/usage separately. Empty text is not an instruction to discard the envelope.

## Execution diagnoses
- A halfway stream failure may have already displayed partial text, but no complete-response success should be recorded. Keep the error visible and do not silently classify the fragment.
- `ainvoke` awaits I/O; `async def` around blocking Python does not make it nonblocking.
- `batch` runs multiple client calls with bounded concurrency and returns input-ordered results. It is not the provider Batch API, a discount guarantee or evidence of per-item latency. The lab reports unmeasured item duration as null.
- A compatible endpoint may omit usage or extra fields. Inspect integration docs instead of inventing counts or concluding that all providers behave identically.
- Missing integration imports point to environment/dependency issues; unsupported temperature is a model capability mismatch; neither is fixed by prompt tweaking.

## Acceptance and later review
A complete gate explains an actual message sequence, deliberate prompt modification and reconstructed streaming envelope; live proof needs approved access. Authored message/chunk tests prove deterministic operations only. Review later with an unfamiliar content block and a new prompt variable, then compare genuine tool results in Module 04. Use goal→observed mismatch→cause→next action feedback; do not certify mastery from running the supplied source.
