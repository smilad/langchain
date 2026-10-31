# LangChain learning roadmap

Research baseline: 2026-10-12. Status: **all sixteen core modules authored and implemented**; see [the sixty-four-lesson index](lessons/README.md). [Local verification](docs/VERIFICATION.md) is not a claim that provider-dependent or learner-mastery gates passed.

Read [the mission](MISSION.md), use [the resource guide](RESOURCES.md) for primary sources, and apply [the teaching guide](docs/TEACHING_GUIDE.md) for practice/assessment.

## 1. Design decisions

### Learn the primitives before the harness

The current official overview presents LangChain's `create_agent` as a configurable agent harness, LangGraph as lower-level orchestration, Deep Agents as a more complete harness, and LangSmith as tracing/evaluation tooling. Our **teaching order** is deliberately different from a fastest-start product recommendation:

1. Plain Python and a direct model call: identify what the framework does and does not do.
2. LangChain models/messages, structured output, tools, and agents.
3. Retrieval and a simple two-step RAG baseline before agentic RAG.
4. Explicit LangGraph workflows, persistence, and human approval.
5. Evaluation, security, integration, and production decisions.
6. Optional specialized architectures only after a baseline exists.

LangChain agents already use LangGraph underneath. Learning graphs later is a pedagogical choice, not a prerequisite for `create_agent`. LangSmith concepts start early; a hosted account is not required for the first lessons.

### Depth without giant lessons

Each module contains four narrowly scoped lessons. A lesson has a short explanation and a worked example; its lab supplies the depth. Every module ends with an independent variation, a failure investigation, and a delayed review. Framework API lookup is allowed; conceptual answers and design choices must be the learner's own.

### Pacing, not a promise

The sixteen core modules total **91–127 hours** of suggested study/lab time. This is an authoring estimate, not a measured completion time. At 6–8 hours/week, allow roughly 12–22 weeks, plus remediation. Experienced Python developers can demonstrate the Module 00 gate rather than repeat familiar material. Optional tracks add time and are not required for core completion.

Suggested weekly rhythm: two concept/example sessions, two lab/debugging sessions, and one short retrieval/review session. Advance by demonstrated mastery rather than a calendar date.

## 2. Prerequisite diagnostic

Before a paid model call, attempt these without an AI-written solution:

- Write a typed function that reads JSON, validates required fields, and reports an invalid record.
- Use a virtual environment, install a package, and explain which interpreter executes a script.
- Load a value from an environment variable without printing a secret.
- Explain a HTTP request/response, a timeout, and a 429 response.
- Define a Pydantic schema and interpret a validation error; use its documentation if unfamiliar.
- Explain what `await` changes and identify a blocking operation inside asynchronous code.

If the first three are unfamiliar, take the Python/environment lessons in Module 00 before progressing. HTTP, Pydantic, and async can be remediated just before their first dependent lab. Record actual evidence, not assumed proficiency.

## 3. Core modules

### 00 — Reproducible setup and Python readiness · 3–5 hours

**Prerequisites:** none; use the diagnostic to adapt the lesson depth.

**Lessons**
1. Interpreter, virtual environments, dependency metadata, and a lockfile.
2. Functions, type hints, JSON, exceptions, and environment variables.
3. Pydantic validation and the request/response boundary.
4. Synchronous versus asynchronous work; reading a traceback.

**Lab:** use the locked course environment and configuration-check command. The namespace cutover is implemented: course `langchain-learning` / `langchain_learning`, external library `langchain`, and migrated course CLI. The repository directory can retain its original name.

**Gate:** a clean checkout can reproduce the environment; `import langchain` resolves to the external library, not the course package; missing configuration is reported without exposing secrets. Verify selected integrations on Python 3.14 rather than assuming that core-library support proves every integration works.

**Common trap:** installing into one interpreter while the IDE runs another.

### 01 — LLM mental models and a plain-Python baseline · 3–4 hours

**Prerequisites:** Module 00.

**Lessons**
1. Tokens, context windows, generation, and model versus application state.
2. Instructions, user input, sampling, and why output is not a database fact.
3. One direct provider-SDK call and its response object.
4. What LangChain standardizes, and when ordinary Python is enough.

**Lab:** a small text classifier with a direct call; record input, output, elapsed time, model ID, and reported usage when available. Use a configurable model, not a tutorial's frozen model name.

**Gate:** trace the full request path and diagnose a bad instruction versus a transport error. Explain why low temperature is not a correctness guarantee. No fine-tuning or transformer mathematics is required here.

**Review prompt:** which parts of this program are deterministic?

### 02 — Models, messages, and prompts · 5–7 hours

**Prerequisites:** Module 01.

**Lessons**
1. Model initialization and separately installed provider integrations.
2. Message roles, content blocks, and the distinction between text and tool messages.
3. Prompt templates and explicit input/context separation.
4. Invocation, streaming, batching, and async execution.

**Lab:** rebuild the classifier using the LangChain model interface. Add an interactive streaming view; inspect the complete response separately from displayed text.

**Gate:** explain a message sequence, change a prompt intentionally, and reconstruct a streamed answer without mistaking metadata/tool events for prose. Compare interfaces without claiming providers have identical capabilities.

**Common trap:** treating every message's content as a plain string.

### 03 — Structured output and deterministic composition · 5–7 hours

**Prerequisites:** Module 02.

**Lessons**
1. Schemas, required/optional fields, and semantic versus shape validation.
2. Model-level structured output and agent structured responses.
3. Prompt → model → parse composition; introduce Runnable/LCEL where useful.
4. Unsupported capabilities, invalid outputs, and bounded failure handling.

**Lab:** extract typed fields from synthetic support requests. Include missing, contradictory, and irrelevant inputs; define what an unknown field means.

**Gate:** consumers receive validated data or an explicit error/abstention, not an invented record. Explain provider-native versus tool-based structured-output strategies. Never use a JSON-shaped answer as proof that its facts are correct.

**Common trap:** automatically retrying a semantically impossible request until it looks valid.

### 04 — Tools and a first agent · 6–8 hours

**Prerequisites:** Module 03.

**Lessons**
1. Tool schemas, descriptions, and argument validation.
2. Model-requested tool calls versus actual Python execution.
3. The `create_agent` loop, tool results, and stopping conditions.
4. Inspecting intermediate messages and classifying tool failures.

**Lab / Project A:** a read-only catalog assistant over a small local synthetic dataset. Give it lookup and deterministic calculation tools; use real data access, not fabricated weather responses.

**Gate:** show successful lookup, unavailable item, invalid tool input, and a bounded run. Trace which arguments were supplied and which function executed. The assistant must not invent an item absent from the catalog.

**Common trap:** assuming a tool docstring is an authorization boundary.

### 05 — Conversation state, memory, and context engineering · 5–7 hours

**Prerequisites:** Module 04.

**Lessons**
1. A conversation's message history versus a model's weights.
2. Short-term thread state and persistent long-term information.
3. Trimming, summarization, and explicit context selection.
4. User/thread identifiers, isolation, and data minimization.

**Lab:** extend Project A with two separate conversations and an explicit synthetic preference. Compare full history with a summarized context.

**Gate:** no preference/history crosses between users; the learner can show what was retained, discarded, and supplied to the model. State that a summary may lose relevant details.

**Review prompt:** which state survives restarting the process, and why?

### 06 — Documents, embeddings, and retrieval · 6–8 hours

**Prerequisites:** Module 03; Module 05 is useful but not required for the retrieval lab.

**Lessons**
1. Documents, loaders, metadata, and provenance.
2. Chunk boundaries, overlap, and stable source identifiers.
3. Embeddings, similarity, vector stores, and retriever interfaces.
4. Lexical versus semantic search; filters and index updates.

**Lab:** index a small versioned synthetic policy corpus. Keep source identifiers through ingestion. Inspect retrieved text before asking a model to answer.

**Gate:** answerable queries retrieve relevant passages; metadata filters exclude unauthorized sources; an edited source does not leave an obsolete duplicate active. Include a paraphrase, an exact identifier, and a no-match question.

**Common trap:** changing embedding models without rebuilding the index.

### 07 — Grounded RAG and retrieval improvement · 7–10 hours

**Prerequisites:** Modules 02, 03, and 06.

**Lessons**
1. Two-step retrieval → answer generation as the simplest baseline.
2. Source-grounded answers, citations, and deliberate abstention.
3. Query rewriting, hybrid retrieval, and reranking as measured experiments.
4. Agentic RAG: when dynamic retrieval earns its additional complexity.

**Lab / Project B:** a policy-document assistant returning an answer plus source IDs. Start with two-step RAG, then change only one retrieval variable per experiment.

**Gate:** demonstrate answerable, unanswerable, contradictory, outdated, and malicious-document cases. Citations must identify retrieved passages and those passages must support the answer; citation presence alone does not pass. Compare baseline versus improvement on held-out questions.

**Common trap:** diagnosing generation quality when the relevant passage was never retrieved.

### 08 — Tracing and evaluation · 6–8 hours

**Prerequisites:** Project A and Project B; basic trace inspection also appears in earlier modules.

**Lessons**
1. Trace trees: model calls, tools, retrieval, errors, usage, and timing.
2. Dataset design: expected evidence, rubrics, and dataset splits.
3. Deterministic checks, human review, and calibrated model-based graders.
4. Offline comparisons versus live monitoring; quality/latency/cost tradeoffs.

**Lab:** create a 20-case synthetic RAG evaluation set: 8 answerable, 4 unanswerable, 4 conflicting/outdated, and 4 adversarial/access-boundary cases. Use 12 for development and freeze 8 for held-out review. This small dataset teaches evaluation; it is not a statistically strong production benchmark.

**Gate:** publish per-case outcomes and failure categories, not just an average score. Show a retrieval failure separately from an unsupported generated claim. Repeated model runs use a declared trial count and report variability. Obtain permission before uploading any private content to hosted traces.

**Common trap:** tuning the prompt on the same examples used to claim improvement.

### 09 — Explicit LangGraph workflows · 6–8 hours

**Prerequisites:** Modules 04, 05, and 08.

**Lessons**
1. State schemas, nodes, edges, and compilation.
2. Conditional routing and explicit termination.
3. Partial state updates, reducers, and message accumulation.
4. Parallel branches and deterministic versus model-driven decisions.

**Lab:** route a synthetic support request through classify → retrieve → draft, with separate paths for unsupported requests and human review. Build the routing mechanics without a model first, then add model-based classification.

**Gate:** explain state before/after every node, run all routes, and diagnose an incorrect reducer or non-terminating edge. Justify why this workflow needs an explicit graph rather than an agent loop.

**Common trap:** returning a complete mutated state when a node should return an update.

### 10 — Persistence, durable execution, and human approval · 7–10 hours

**Prerequisites:** Module 09.

**Lessons**
1. Checkpointers, threads, and checkpoint inspection.
2. Interrupt/resume and human edits to proposed actions.
3. Replay, restart boundaries, and idempotent external effects.
4. Persistent stores versus checkpoint state; debugging prior states.

**Lab / Project C:** a support-draft workflow that pauses before a side effect. Use a local synthetic action sink and persistent storage; approve/reject/edit the proposed action explicitly.

**Gate:** stop the process while paused, restart, and resume the same thread. A rejected action has no side effect; approved execution records one action; replay/resume does not duplicate it. An in-memory checkpointer is not sufficient evidence of process-restart durability.

**Common trap:** performing a side effect before an interrupt, then replaying it on resume.

### 11 — Middleware, guardrails, and security boundaries · 6–8 hours

**Prerequisites:** Modules 08 and 10.

**Lessons**
1. Middleware hooks and explicit control of model/tool behavior.
2. Context selection, budgets, and bounded execution policies.
3. Prompt injection, untrusted retrieved content, and least privilege.
4. Authorization, redaction, and human approval outside the prompt.

**Lab:** attack Projects B/C with documents that instruct the agent to reveal secrets or perform an unauthorized action. Use only synthetic secrets. Add code-level boundaries; compare behavior before/after.

**Gate:** show that untrusted content cannot grant permission. Check arguments and identity at the execution boundary. Record limits: guardrails reduce risk; they do not prove immunity to prompt injection.

**Common trap:** expecting an LLM safety instruction to replace access control.

### 12 — Multi-agent patterns and context contracts · 5–7 hours

**Prerequisites:** Modules 08, 09, and 11.

**Lessons**
1. Single-agent baseline and the cost of extra agents.
2. Router, subagent, handoff, and supervisor-style patterns.
3. Context ownership, structured handoffs, and termination.
4. Comparing quality, latency, cost, and error propagation.

**Lab:** implement one constrained specialist pattern for Project C; compare against the single-agent version on the same cases. Do not implement every pattern just to collect APIs.

**Gate:** document a measurable reason to retain the specialist, or deliberately reject the design. Demonstrate failed specialist output and a bounded recovery/stop decision.

**Common trap:** treating more agents as inherently more intelligent.

### 13 — MCP and external integration boundaries · 4–6 hours

**Prerequisites:** Modules 04 and 11; async remediation if needed.

**Lessons**
1. MCP client/server roles, tools, resources, and transport.
2. Connect a local server using current Python integration documentation.
3. Credentials, capability exposure, and lifecycle management.
4. Server failure, timeouts, schema changes, and disconnects.

**Lab:** expose a read-only synthetic catalog tool through an actual local MCP server and invoke it through the agent. Keep the direct Python version as a conceptual comparison, not a compatibility layer.

**Gate:** observe a real client/server call and graceful server shutdown; explain why a connected tool is not automatically trusted. No real production credentials or remote unreviewed tools.

**Common trap:** teaching an adapter's import syntax without teaching the security/transport boundary.

### 14 — Production engineering and deployment · 7–10 hours

**Prerequisites:** Modules 08, 10, and 11.

**Lessons**
1. Application entrypoint, configuration, health/readiness, and request isolation.
2. Concurrency, deadlines, cancellation, rate limits, and bounded retries.
3. Persistent storage, schema changes, logs, and operational data handling.
4. Packaging/deployment choices and an observable rollback procedure.

**Lab:** serve Project C locally with the chosen deployment mechanism; keep hosting optional. Exercise two simultaneous users, cancellation, upstream failure, and restart with pending work.

**Gate:** publish run/deploy instructions that work outside the author's IDE. Demonstrate an end-to-end request, isolated users, persisted approval, and failure visibility. Define latency/cost targets from measured baseline and the intended workload; do not invent universal SLAs.

**Common trap:** calling a notebook demo production-ready because it returns an answer once.

### 15 — Capstone, transfer, and teaching others · 10–14 hours

**Prerequisites:** Modules 00–14 or equivalent demonstrated gates.

**Lessons**
1. Write the problem statement, data boundary, and acceptance criteria.
2. Choose the simplest architecture and produce a baseline.
3. Evaluate, investigate failures, and justify one improvement.
4. Create a clean-checkout tutorial and explain the system to a new learner.

**Capstone default:** evolve Projects B/C into a source-grounded support assistant that drafts a response, pauses for human approval, and records the approved synthetic action. A different domain may replace the dataset without removing the same behavioral requirements.

**Gate:** deliver architecture/data-flow diagrams, runnable application, reproducible environment, held-out evaluation report, restart/approval demonstration, adversarial-case report, and cost/latency measurements. Show one unfamiliar input variation without copying a worked solution. Publish known limitations instead of claiming perfect reliability.

## 4. Beyond the core: optional advanced tracks

| Track | Prerequisites | Questions to answer | Deliverable |
|---|---|---|---|
| Deep Agents and long-horizon work | 10–12 | What does the harness add? How do planning, files, subagents, context compression, and sandbox boundaries behave? | Compare a real multi-step task with `create_agent`; justify the extra harness and measure overhead. |
| Advanced retrieval | 06–08 | When do hybrid search, reranking, metadata design, and incremental indexing improve the actual corpus? | One-variable experiment report with held-out retrieval/answer results. |
| SQL agents | 04, 08, 11 | How are schemas exposed and read-only permissions enforced independently of the prompt? | Query a synthetic database through a restricted account; demonstrate rejected writes and unauthorized tables. |
| Multimodal and real-time interfaces | 02, 08, 14 | Which content blocks/capabilities are provider-specific? How are streaming latency and cancellation handled? | One actual image/audio interaction with provenance and measured latency. |
| Local/open models | 02, 03, 08 | What hardware, context, structured-output, and tool-call limits affect the application? | Run a supported local model and compare with the baseline; report hardware and capability gaps. |
| Open-source contribution and internals | Core capstone | Can you follow agent→graph execution and explain a public API boundary? | Reproduce an upstream issue or improve a verified documentation example; follow upstream contribution policy. |

## 5. Completion and retention

Use the rubric in [the teaching guide](docs/TEACHING_GUIDE.md). Passing a module requires the practical gate, an explanation of the design, a failure diagnosis, and an independent variation. If any is missing, remediate that skill before its dependent module.

At the end of each phase, revisit earlier material without a worked solution:
- After 04: reconstruct model → tool request → tool execution → answer.
- After 08: distinguish a retrieval miss, a hallucinated answer, and a flawed evaluator.
- After 11: recover a paused thread without duplicating a side effect.
- After 15: adapt the architecture to a new small corpus/domain and explain what stays invariant.

Do not mark a topic mastered because the lesson was read or the example ran. Create a learning record only when the learner supplies evidence.
