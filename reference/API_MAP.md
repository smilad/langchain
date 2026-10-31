# API map and tested-version baseline

`uv.lock` is the dependency authority. Installed on Python **3.14.0**: LangChain **1.4.4**, langchain-core **1.6.9**, langchain-openai **1.7.0**, LangGraph **1.2.14**, SQLite checkpointer **3.1.1**, FastMCP **4.1.0**, Pydantic **2.14.1**, OpenAI SDK **3.29.0**. Installation alone is not runtime/capability proof; see [the verification report](../docs/VERIFICATION.md) for exercised paths and blockers.

## Framework boundaries

| Concept | API / module | Course location |
|---|---|---|
| Direct model request | `openai.OpenAI.responses.create`, Responses request/response | [01 baseline](../lessons/01_llm_baseline/01.md) |
| LangChain model | `langchain_openai.ChatOpenAI`, `invoke`, `stream`, `ainvoke`, `batch` | [02 messages/models](../lessons/02_models_messages/01.md) |
| Prompt/data composition | `langchain_core.prompts.ChatPromptTemplate`, Runnable composition | [03 typed output](../lessons/03_structured_output/01.md) |
| Model structured output | `ChatOpenAI.with_structured_output` plus Pydantic schema | [03 typed output](../lessons/03_structured_output/02.md) |
| Agent construction | `langchain.agents.create_agent`; `system_prompt`, tools, middleware/checkpointer | [04 tools/agents](../lessons/04_tools_agents/01.md) |
| Typed tools | `langchain.tools.tool`; Pydantic input validation | [04 catalog](../labs/04_tools_agents/README.md) |
| Messages/context | `langchain.messages` / `langchain_core.messages`; content blocks and context selection | [05 memory/context](../lessons/05_memory_context/01.md) |
| Evidence | `langchain_core.documents.Document`; metadata survives ingestion/retrieval | [06 retrieval](../labs/06_retrieval/README.md) |
| Learned semantic embeddings | `langchain_openai.OpenAIEmbeddings`; actual configured embedding model required | [06 retrieval](../lessons/06_retrieval/03.md) |
| Graph workflow | `langgraph.graph.StateGraph`, `START`, `END`, conditional edges, reducers | [09 graphs](../labs/09_graph_workflows/README.md) |
| Durable state | `langgraph.checkpoint.sqlite.SqliteSaver` | [10 approval](../labs/10_durable_approval/README.md) |
| Human review | `langgraph.types.interrupt`, `Command(resume=...)` | [10 approval](../lessons/10_durable_approval/02.md) |
| MCP client/server | `langchain.mcp.MCPAdapter`, `list_tools`; `fastmcp.FastMCP` | [13 MCP](../labs/13_mcp/README.md) |
| Local serving | `langchain_learning.service`, localhost HTTP, token-bound identity | [14 production](../labs/14_production/README.md) |

Provider feature support is checked per model/endpoint. The same import path does not make tool calling, structured output, content blocks, or usage metadata identical across providers.

## Course domain APIs

### Catalog

`lookup_item(item_id)` reads the actual synthetic catalog; missing IDs are explicit. `quote_total(item_id, quantity)` validates stock/quantity and computes integer cents. `catalog_tools()` exposes those real functions as LangChain tools. `build_catalog_agent(checkpointer=...)` requires live provider consent/configuration.

### Retrieval and generated answers

`PolicyIndex(strategy="lexical").search(question, user_id, k=3)` returns authorized current `Document` values. Lexical retrieval is a genuine local baseline, not a substitute claiming learned semantic capabilities. The semantic strategy calls the configured embedding provider; it has no silent lexical fallback.

`rag.answer(question, user_id, strategy="lexical", k=3)` returns `GroundedAnswer(answer, source_ids, abstained)`. Inspect selected evidence independently. Schema/source-membership validation does not establish that every claim is supported.

### Persistent review

```python
from langchain_learning.runtime import state_dir
from langchain_learning.workflow import SupportWorkflow

folder = state_dir()
with SupportWorkflow(folder / "checkpoints.sqlite", folder / "actions.sqlite") as flow:
    pending = flow.start("alice", "reference-thread", "Review my policy question",
                         draft="Explicitly human-authored draft for a no-model exercise")
    inspected = flow.inspect("alice", "reference-thread")
    completed = flow.decide("alice", "reference-thread", "approve")
```

The example records a synthetic local action after approval. The user/thread ownership binding survives restart. Repeat matching decisions reuse the result; conflicting decisions are rejected. Do not describe this as exactly-once delivery to an external service.

## Navigation and modes

```bash
uv run langchain-learning list
uv run langchain-learning check
uv run langchain-learning run 06 --check
uv run langchain-learning run 15 --check
```

Each lab README lists topic-specific options. `--check` is model-free real local behavior; `--live` requires model/key configuration and explicit consent. Neither mode claims a completed learner mastery gate by itself.

**Sources:** [v1 migration](https://docs.langchain.com/oss/python/migrate/langchain-v1), [models](https://docs.langchain.com/oss/python/langchain/models), [interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts), [MCP](https://docs.langchain.com/oss/python/langchain/mcp/index).
