# Course glossary

Use consistent terms in [the lessons](../README.md) and inspect concrete representations in the corresponding lab. Definitions describe responsibilities; they do not imply that every provider exposes the same capability.

| Term | Meaning and important boundary |
|---|---|
| Model | A learned generator accessed through a provider/local runtime; it is not the complete application. |
| Token | A model's text/content encoding unit used for context limits and usage; not necessarily a word. |
| Context window | The input/output capacity for one model interaction; it is not persistent memory. |
| Prompt | Instructions and context supplied to a model; not an authorization mechanism. |
| Message | A role/content representation in a conversation; content can include structured blocks rather than a plain string. |
| Content block | A typed text, reasoning, tool, image, or other content unit; availability differs by provider. |
| Tool call | The model's request to execute a function with arguments; not proof that execution occurred. |
| Tool | Executable code with an input schema and description; permission checks belong at execution boundaries. |
| Agent | Model plus the surrounding loop/harness that executes tools and updates state. |
| Harness | The application machinery around model calls: prompts, tools, context, middleware, and policies. |
| Structured output | Output conforming to a declared schema; shape validity does not establish factual correctness. |
| Runnable / LCEL | Components and composition for deterministic application data flow; not an obsolete concept merely because agent APIs changed. |
| State | Application data carried between steps; distinguish ephemeral values, checkpoint state, and cross-thread stores. |
| Thread | A workflow/conversation identity selecting persisted run state; ownership must be enforced separately. |
| Checkpoint | A saved graph-state snapshot enabling continuation/inspection; saving alone does not make external effects idempotent. |
| Checkpointer | Persistence implementation for thread-scoped graph state. An in-memory one loses it on process restart. |
| Store | Application-managed cross-thread memory; use an explicit identity namespace and retention policy. |
| Context engineering | Selecting instructions, evidence, messages, tools, and other context for a particular call. |
| Reducer | A rule for merging state updates, especially multiple/parallel updates; wrong rules can lose or duplicate data. |
| Interrupt | A persistent pause awaiting external input; resumed nodes may execute preceding code again. |
| Resume | Continuation of the same paused thread with a decision/value, not a new unrelated request. |
| Idempotency | Repeating an operation preserves the intended result rather than causing another effect. The scope must be named. |
| Local action sink | This course's real SQLite records representing synthetic approved actions; not email or a production ticket system. |
| Document | Retrieved/ingested text plus metadata such as source ID, version, audience, and current status. |
| Chunk | A selected segment of a source; its boundary and provenance affect retrieval and support checks. |
| Embedding | A numeric representation of content. A lexical term vector and a learned semantic embedding have different capabilities. |
| Vector store | Storage/search over numeric representations and metadata; not inherently a durable or authorized database. |
| Retriever | A component selecting evidence for a query under explicit relevance and permission rules. |
| RAG | Retrieval-augmented generation: supplying selected external evidence to generation. Retrieval does not guarantee groundedness. |
| Two-step RAG | Fixed retrieve → generate flow, a useful measured baseline before dynamic agentic retrieval. |
| Groundedness | Whether substantive answer claims are supported by the selected evidence. Citation presence alone is insufficient. |
| Abstention | Explicitly declining to answer because required evidence/capability is missing; not a fabricated substitute answer. |
| Trace | Observed execution records: model calls, tool arguments/results, retrieval, state transitions, timing/errors. |
| Evaluator | A rule/person/model assessing an outcome. Model-based evaluators have their own failure modes and costs. |
| Development split | Cases used for diagnosis/tuning; their scores are not independent confirmation of those choices. |
| Held-out split | Cases reserved for a declared comparison; tuning after inspecting them compromises independence for later claims. |
| Middleware | Hooks/wrappers shaping agent model/tool behavior; it does not replace lower-level access control. |
| Prompt injection | Untrusted input attempting to change application/model instructions or cause unauthorized behavior. |
| Authorization | A code-enforced decision about which identity can access data or execute an operation. |
| Authentication | Establishing an identity from a trusted credential rather than a client-supplied identity field. |
| MCP | A tool/context interoperability protocol; server connection is not automatic trust or a multi-agent architecture. |
| Subagent | A constrained delegated agent; context ownership and termination remain application responsibilities. |
| Handoff | A transfer of responsibility/context, potentially state-driven without a separate process. |
| Deep Agents | A higher-level harness built on LangChain; backend/version choices determine planning, files, and execution behavior. |
| Cancellation | A request to stop work. Client disconnect does not prove that already committed state/effects were rolled back. |

**Sources:** [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview), [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval), [evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts), [MCP](https://docs.langchain.com/oss/python/langchain/mcp/index).
