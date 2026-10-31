# Module 02 — inspect and reconstruct message boundaries

**Objective:** Explain roles/blocks, render prompts locally and reconstruct streaming output while preserving metadata. Prerequisite: Module 01 and async readiness; [lessons](../lessons/02_models_messages/01.md), [runbook](../labs/02_models_messages/README.md). Do not confuse an authored message fixture with generated output.

## Retrieval and prediction
Name the three separate packages for course application, core interfaces and provider integration. Predict which operation first contacts the provider. Can an empty text chunk still matter? Attempt before viewing [solutions](../solutions/02_models_messages.md).

## Guided fading
1. Create a two-message prompt with system instructions and `{text}` human input. Render it and inspect roles without a model. Supply the missing caller key after intentionally using a wrong variable name.
2. Construct an explicitly authored AIMessage with a text block and a reasoning block. Inspect raw content, text projection and normalized blocks. Explain which you would display and why.
3. Reconstruct an authored sequence of two text chunks plus an empty usage-bearing chunk. Write the accumulator yourself. Show what a list of text strings loses. Keep usage values clearly labeled exercise data, not provider reporting.

## Independent variations
- Add a separate `{context}` variable while keeping user input distinct. Choose where trusted application context belongs and explain why this is not an authorization boundary.
- Change the classification rubric without changing the message/transport interface. Try user data containing braces and an instruction-like sentence; check rendering first, then investigate live instruction-following only with approved access.
- Add an authored ToolMessage linked to a call ID. Explain how this differs from an AIMessage requesting a tool and from the actual Python tool execution introduced later.
- Design an inspection function that explicitly marks missing usage unavailable instead of reporting zero. Do the same for unmeasured per-batch-item latency.

## Failure investigation
Predict and locate: missing prompt variable, wrong interpreter/integration, unsupported model sampling parameter, a metadata-only chunk skipped by a renderer, halfway stream failure and batch input/output misalignment. Preserve provenance: a partial stream is not a completed answer. Do not provoke paid failures or assume every provider exposes the same blocks.

## Approved live variation
If configured and permitted, choose **one** path first: invoke, stream, async or batch. Interactive streaming reads one line. Record actual complete message separately from displayed text and note usage absence honestly. Batch sends two requests; all sends five. Explain client-side concurrency versus a provider Batch API and why concurrent I/O can hit rate limits. If you compare modes, declare inputs/trials and report what was actually measured, not invented speedups.

## Exit and spaced transfer
Gate evidence includes rendered message sequence, intentional prompt change, complete stream reconstruction and a capability-aware comparison. Without provider access, deterministic rendering/aggregation can pass while live streaming remains pending. Next session reconstruct a fresh chunk sequence without the example; next week explain roles on an unfamiliar content type. Apply the distinction again in Module 04 tools and Module 05 history.

Use the hint ladder: name the stage, inspect its intermediate value, read its contract, then request a smaller example. [Verification](../docs/VERIFICATION.md) tracks course run evidence, not learner mastery.
