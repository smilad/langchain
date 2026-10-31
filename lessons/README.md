# Lesson index

Follow [the roadmap](../ROADMAP.md) and demonstrate the module gates rather than merely reading every file. Each lesson links a real lab, an independent exercise, a separate solution, and primary sources. Read [the verification report](../docs/VERIFICATION.md) for exercised behavior and remaining live/review prerequisites.

## Foundations

| Module | Lesson 1 | Lesson 2 | Lesson 3 | Lesson 4 |
|---|---|---|---|---|
| 00 Setup | [Environment](00_setup/01.md) | [Python/data](00_setup/02.md) | [Validation/HTTP](00_setup/03.md) | [Async/tracebacks](00_setup/04.md) |
| 01 LLM baseline | [Tokens/context](01_llm_baseline/01.md) | [Instructions/sampling](01_llm_baseline/02.md) | [Direct call](01_llm_baseline/03.md) | [Framework boundary](01_llm_baseline/04.md) |
| 02 Models/messages | [Initialization](02_models_messages/01.md) | [Message content](02_models_messages/02.md) | [Prompts/context](02_models_messages/03.md) | [Streaming/async/batch](02_models_messages/04.md) |
| 03 Structured output | [Schemas](03_structured_output/01.md) | [Typed model/agent output](03_structured_output/02.md) | [Composition](03_structured_output/03.md) | [Failures/limits](03_structured_output/04.md) |

## Applications and measured quality

| Module | Lesson 1 | Lesson 2 | Lesson 3 | Lesson 4 |
|---|---|---|---|---|
| 04 Tools/agents | [Tool schemas](04_tools_agents/01.md) | [Request versus execution](04_tools_agents/02.md) | [Agent loop](04_tools_agents/03.md) | [Inspect failures](04_tools_agents/04.md) |
| 05 Memory/context | [History versus weights](05_memory_context/01.md) | [Threads versus stores](05_memory_context/02.md) | [Context selection](05_memory_context/03.md) | [Isolation/minimization](05_memory_context/04.md) |
| 06 Retrieval | [Documents/provenance](06_retrieval/01.md) | [Chunking](06_retrieval/02.md) | [Embeddings/search](06_retrieval/03.md) | [Filters/index updates](06_retrieval/04.md) |
| 07 RAG | [Two-step baseline](07_rag/01.md) | [Support/abstention](07_rag/02.md) | [Measured improvement](07_rag/03.md) | [Agentic retrieval](07_rag/04.md) |
| 08 Evaluation | [Traces](08_evaluation/01.md) | [Datasets/splits](08_evaluation/02.md) | [Evaluators/feedback](08_evaluation/03.md) | [Offline/live monitoring](08_evaluation/04.md) |

## Explicit control and integration

| Module | Lesson 1 | Lesson 2 | Lesson 3 | Lesson 4 |
|---|---|---|---|---|
| 09 Graphs | [State/nodes/edges](09_graph_workflows/01.md) | [Routing/termination](09_graph_workflows/02.md) | [Reducers/updates](09_graph_workflows/03.md) | [Parallel branches](09_graph_workflows/04.md) |
| 10 Durable approval | [Checkpoints/threads](10_durable_approval/01.md) | [Interrupt/resume](10_durable_approval/02.md) | [Replay/idempotency](10_durable_approval/03.md) | [Stores/state inspection](10_durable_approval/04.md) |
| 11 Security | [Middleware](11_middleware_security/01.md) | [Policies/budgets](11_middleware_security/02.md) | [Injection/privilege](11_middleware_security/03.md) | [Authorization/redaction](11_middleware_security/04.md) |
| 12 Multi-agent | [Baseline/cost](12_multi_agent/01.md) | [Patterns](12_multi_agent/02.md) | [Context/handoffs](12_multi_agent/03.md) | [Comparison/errors](12_multi_agent/04.md) |
| 13 MCP | [Protocol roles](13_mcp/01.md) | [Real local server](13_mcp/02.md) | [Auth/lifecycle](13_mcp/03.md) | [Failure/disconnect](13_mcp/04.md) |

## Operations and transfer

| Module | Lesson 1 | Lesson 2 | Lesson 3 | Lesson 4 |
|---|---|---|---|---|
| 14 Production | [Application/config](14_production/01.md) | [Concurrency/deadlines](14_production/02.md) | [Storage/data handling](14_production/03.md) | [Deploy/rollback](14_production/04.md) |
| 15 Capstone | [Specify architecture](15_capstone/01.md) | [Run/recover/review](15_capstone/02.md) | [Evaluate/improve](15_capstone/03.md) | [Transfer/teach](15_capstone/04.md) |

## How to practice

1. Answer the retrieval warm-up before seeing corrections.
2. Run the small worked example and inspect intermediate representations.
3. Attempt the module exercise with a changed constraint; documentation lookup is allowed.
4. Diagnose the named failure from evidence before opening the solution.
5. Explain why the repair addresses the cause and what remains unverified.
6. Revisit a fresh conceptual/coding variation later; record mastery only after actual learner evidence.

Model-free `--check` paths never claim generated-answer quality. `--live` requires a real configured provider and explicit spending consent. Optional advanced tracks remain described in the roadmap and are not substitutes for core module gates.
