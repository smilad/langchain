# LangChain learning resources

Research baseline: **2026-10-12**. Prefer these sources over unversioned tutorial collections. Read only the resource needed for the current lesson; the list is a reference map, not a requirement to consume everything before coding.

## Knowledge

### First resources: orientation and foundations

| Resource | When to use it | What to extract / caveat |
|---|---|---|
| [Official Python Learn index](https://docs.langchain.com/oss/python/learn) | Orientation and finding current tutorials | Ecosystem/use-case map. A card's title does not guarantee its implementation layer: the RAG Agent card currently points to Deep Agents material. |
| [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview) | Modules 01–04 | LangChain `create_agent`, LangGraph, Deep Agents, and LangSmith responsibilities. Our primitive-first teaching order differs from the docs' fastest-start Deep Agents recommendation. |
| [Introduction to LangChain — Python, Academy](https://academy.langchain.com/courses/foundation-introduction-to-langchain-python) | Modules 02–05, then revisit for 11–13 | Verified public curriculum: models, tools, short-term memory, multimodal messages, MCP, context/state, multi-agent, middleware, HITL, and projects. Listed free with 30 lessons and 1.5 hours of video; video duration is not lab completion time. Enrollment may be needed for lesson access. |
| [Python quickstart](https://docs.langchain.com/oss/python/langchain/quickstart) | First agent in Module 04 | Model/tool/prompt setup and message-based invocation. Adapt model availability and provider credentials; do not copy its Python 3.11 setup into this project's `>=3.14` constraint. |
| [LangChain v1 migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1) | Before adapting any external example | Modern agent APIs, middleware, structured output, content blocks, provider packages, and namespace changes. This is a compatibility reference, not the primary beginner lesson. |
| [Trace LangChain applications](https://docs.langchain.com/langsmith/trace-with-langchain) | Trace concepts from Module 02; full lab in 08 | Model/tool/retrieval execution, metadata, projects, and tracing configuration. Hosted tracing requires an account/key and care with sensitive inputs/outputs. |

### Retrieval and evidence-based application evaluation

| Resource | When to use it | What to extract / caveat |
|---|---|---|
| [Build a semantic search engine](https://docs.langchain.com/oss/python/langchain/knowledge-base) | Module 06 | Documents, loaders, splitting, embeddings, vector stores, similarity search, retrievers. In-memory examples do not establish durable indexing; integrations are separate dependencies. |
| [Retrieval / RAG architectures](https://docs.langchain.com/oss/python/deepagents/retrieval) | Module 07 | Two-step, agentic, and hybrid retrieval; reuse existing knowledge sources where appropriate. The conceptual page is under Deep Agents but also uses LangChain examples. Verify incidental older URLs/imports before copying. |
| [LangSmith evaluation quickstart](https://docs.langchain.com/langsmith/evaluation-quickstart) | Module 08 | Dataset + target function + evaluator + experiment. Model-based grading has its own cost and error modes; cloud evaluation is optional for initial learning. |
| [Evaluate a RAG application](https://docs.langchain.com/langsmith/evaluate-rag-tutorial) | Modules 07–08 | Distinguish answer correctness, answer relevance, groundedness, and retrieval relevance. A small tutorial dataset is not evidence of production reliability. |
| [Evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts) | Modules 08 and 14 | Offline dataset comparisons versus evaluation of live runs/threads. Feed observed failures back into regression datasets without contaminating the held-out benchmark. |

### Graph state, durable execution, and human approval

| Resource | When to use it | What to extract / caveat |
|---|---|---|
| [Introduction to LangGraph — Python, Academy](https://academy.langchain.com/courses/intro-to-langgraph) | Modules 09–10 | State, reducers, routers, memory, streaming/HITL, parallelization, subgraphs, long-term memory, deployment. Listed free, 55 lessons, 6 hours of video. Review older breakpoint examples against current interrupt guidance. |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Modules 05 and 10 | Thread-scoped checkpoints versus cross-thread stores; stable thread identity. An in-memory checkpointer cannot demonstrate recovery after process restart. |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Module 10 | `interrupt()` and `Command(resume=...)`; same-thread continuation. Resumed nodes restart from their beginning: placement/idempotency of side effects matters. Newer response-schema features have version floors. |
| [LangChain human-in-the-loop middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) | Modules 10–11 | Tool approval via `HumanInTheLoopMiddleware`, checkpointing, and decisions. Current docs include approve/edit/reject/respond; `respond` is not rejection. |
| [LangGraph v1 migration guide](https://docs.langchain.com/oss/python/migrate/langgraph-v1) | Auditing graph notebooks | Custom graphs retain the core state/checkpoint/interrupt model; deprecated prebuilt-agent APIs are a separate concern. Do not label every older graph example invalid. |

### Integration, advanced harnesses, and deployment

| Resource | When to use it | What to extract / caveat |
|---|---|---|
| [Multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent/index) | Module 12 | Subagents, handoffs, skills, routers, and custom workflows; context ownership and token/latency tradeoffs. Complex tasks do not automatically need multiple agents. |
| [LangChain MCP integration](https://docs.langchain.com/oss/python/langchain/mcp/index) | Module 13 | Current Python docs use `langchain.mcp.MCPAdapter` and `list_tools()`, with async lifecycle and transport/auth concerns. The namespace is beta and requires `langchain[mcp]>=1.4.0`; re-check at authoring time. |
| [MCP adapter migration](https://docs.langchain.com/oss/python/migrate/langchain-mcp-adapters) | Auditing MCP examples | The previous `MultiServerMCPClient` path is not the current docs' baseline. The new wrapper does not implement every protocol capability; teach tools separately from the wider protocol's resources/prompts. |
| [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview) | Optional Deep Agents track | Filesystem/context/delegation capabilities and `create_deep_agent`. Planning is opt-in starting in v0.7; persistence/shell/sandbox behavior depends on the backend. Do not treat a virtual filesystem as automatically durable or sandboxed. |
| [Introduction to Deep Agents, Academy](https://academy.langchain.com/courses/foundation-introduction-to-deepagents) | Optional advanced synthesis | Public curriculum covers execution environments, context management, memory, delegation, and combined projects. Listed free with 46 lessons; the short video-time figure does not represent total study time. |
| [LangSmith Deployment course](https://academy.langchain.com/courses/langsmith-deployment) | Module 14, if that deployment path is chosen | Deployment, clients/UI/routes, memory, and authentication/authorization. Listed free with 37 lessons; free learning content does not imply free production hosting. |
| [Deployment concepts and options](https://docs.langchain.com/langsmith/deployment) | Module 14 | Agent runtime versus observability/evaluation hosting, local/cloud/self-hosted choices, and product requirements. Paid hosting is not a prerequisite for the course. |
| [Release policy](https://docs.langchain.com/oss/python/release-policy) and [versioning](https://docs.langchain.com/oss/python/versioning) | Setup and maintenance | Support windows, semantic versioning, package-specific compatibility, and pre-1.0 risks. Current versions must be locked after a real compatibility run, not copied from this document. |
| [LangChain package metadata](https://pypi.org/project/langchain/) | Module 00 compatibility check | Research snapshot: 1.4.4 declares Python `>=3.10,<4.0` and lists 3.14. This does not prove compatibility for all optional integrations; the repository remains `>=3.14`. |

### How to choose a tutorial

1. Check its date, imports, dependency versions, model availability, and actual source URL.
2. For new agents, prioritize `from langchain.agents import create_agent`.
3. Treat `initialize_agent`, `LLMChain`, `ConversationBufferMemory`, old `langchain.chains` imports, and `langgraph.prebuilt.create_react_agent` as legacy signals. Use the migration guide to distinguish obsolete syntax from useful underlying concepts.
4. Do not reject valid Runnable/LCEL composition just because it is not an agent loop.
5. Compare course notebooks with live docs. A course can remain useful while its MCP import or default harness behavior has changed.
6. Separate copying code from testing a concept: reproduce the example, change a constraint, and investigate a failure.

### Teaching and learning evidence

These sources inform the teaching design; none validates this particular adult LangChain course. Review intervals, lesson lengths, and assessment gates in this repository are practical course-policy choices.

| Source | Use in the course | Evidence boundary |
|---|---|---|
| [Dunlosky et al. (2013): effective learning techniques](https://acs.ist.psu.edu/ist521/dunloskyRMNW13.pdf) | Retrieval practice with corrective feedback and practice distributed across sessions | Broad review rates practice testing/distributed practice highly; it is not a LangChain or adult-programming trial. Rereading documentation still has a useful reference role. |
| [Pashler et al. (2007): IES instruction/study practice guide](https://files.eric.ed.gov/fulltext/ED498555.pdf) | Alternate worked solutions with learner attempts; ask explanatory questions and revisit earlier skills | Explicit evidence grades: active-retrieval quizzes strong; spacing/worked-example alternation moderate. Read via the government-hosted ERIC mirror after original endpoints timed out. |
| [Cepeda et al. (2008): spacing and retention](https://pubmed.ncbi.nlm.nih.gov/19076480/) | Schedule delayed retrieval and adapt review to the retention goal | Primary-study abstract plus an accessible manuscript were checked. Fact-learning results do not establish a universal 1/3/7/14-day coding schedule. |
| [Renkl & Atkinson (2003): worked-example fading](https://mrbartonmaths.com/resourcesnew/8.%20Research/Explicit%20Instruction/Structuring%20the%20Transition%20From%20Example%20Study%20to%20Problem%20Solving.pdf) | Full example → complete a missing final step → larger completion task → independent variant | Small studies mainly use probability/physics tasks; near transfer is not proof of broad software-design transfer. The link is an accessible paper mirror. |
| [Hattie & Timperley (2007): feedback](https://assess.ucr.edu/sites/default/files/2019-02/hattietimperley_2007.pdf) | Feedback identifies goal, observed mismatch, and next diagnostic action | Broad review: effects vary and can be negative. Generic praise and always-immediate answers are not equivalent to informative feedback. |
| [EEF: mastery learning](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/mastery-learning) | Fixed objectives, variable support/time, corrective instruction, fresh-task reassessment | School-focused synthesis with low evidence security; do not translate its school outcome estimates or customary percentage thresholds into adult-course guarantees. |

The [teaching guide](docs/TEACHING_GUIDE.md) turns these principles into concrete lesson and assessment mechanics.


## Wisdom (communities)

- [LangChain GitHub](https://github.com/langchain-ai/langchain): use issue discussions and contribution guidance to understand real failure reports; search existing reports before filing a reproducible issue. Package metadata identifies this as the official repository.
- [Official community entry point](https://www.langchain.com/join-community): optional Slack discussion, events, and project sharing. The community guidelines direct technical/product-help questions to the [LangChain Forum](https://forum.langchain.com/); bring a concrete experiment or minimal reproduction there.

No community participation preference has been established; joining is optional.

## Freshness and gaps

- Public official docs and individual Academy course pages were read. Some Academy catalog/collection pages returned HTTP 403; no claim is made that the complete catalog or enrolled videos were reviewed.
- Provider/budget diagnostics remain required before paid labs. The author exercised live generation and tool use against one endpoint, which exposed no embedding models.
- The locked environment is exercised on Python 3.14, including catalog operations, lexical retrieval, durable graph approval, MCP, and localhost serving. [Verification](docs/VERIFICATION.md) separates observed live successes/failures from unverified JSON-schema, embedding quality, currency cost, and hosted evaluation.
- Source URLs and API defaults can change. Re-check before authoring a lesson and after changing a relevant dependency. Annotate the exact exercised versions in each lab README.
- PyPI versions above are discovery snapshots, not compatibility pins.
