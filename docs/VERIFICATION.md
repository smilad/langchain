# Course verification — 2026-10-12

> **About this record.** This is the course author's execution record from 2026-10-12. Live model runs went through the author's own OpenAI-compatible endpoint, not a standard public API key. Your results can differ: use your own key and model (see the README), and treat everything here as evidence of what was run, not a guarantee.

**Artifacts are implemented; all sixteen local checks and real gateway-mediated model paths have been exercised. JSON-schema compatibility, embeddings, and general model quality remain explicit limits. Advisor review was waived by the user.** Read [the course entry point](../README.md), [lesson index](../lessons/README.md), and [implementation plan](superpowers/plans/2026-10-12-langchain-learning-resources.md) for navigation and remaining evidence gates.

## Environment actually exercised

Darwin arm64, Python **3.14.0**, `uv` **0.12.19**. Locked dependencies:

| Package | Exercised version |
|---|---|
| langchain | 1.4.4 |
| langchain-core | 1.6.9 |
| langchain-openai | 1.7.0 |
| langgraph | 1.2.14 |
| langgraph-checkpoint-sqlite | 3.1.1 |
| fastmcp | 4.1.0 |
| pydantic | 2.14.1 |

`uv sync --locked --system-certs` passed. It also passed in a **fresh temporary project environment**, followed by the actual `langchain-learning run 00 --check`, `langchain-learning list` (all sixteen modules), and `python -m langchain_learning check` entry points. External `langchain` resolved to that environment's `site-packages`, not the course source. The temporary environment was removed afterward.

PyPI artifact DNS timed out during setup; the reachable Tsinghua TUNA mirror is explicitly configured in `pyproject.toml` and recorded in `uv.lock`. No TLS verification was disabled. The smoke is from this checkout on the stated OS/interpreter, not certification of every platform or standalone wheel packaging.

## Actual module checks

Executed `uv run --no-sync python labs/<module>/main.py --check` for **all sixteen modules**, all exit **0**. After the live-discovered fixes below, affected checks also passed. This table describes check-mode scope, not live generation.

| Module | Observed local scope | Exit |
|---|---|---|
| 00 setup | Interpreter, import origin, schemas/configuration checks | 0 |
| 01 LLM baseline | Actual deterministic input/configuration boundaries; no SDK generation | 0 |
| 02 models/messages | Actual message/prompt construction; no streamed model answer | 0 |
| 03 structured output | Actual typed validation/composition; no model extraction | 0 |
| 04 tools/agents | Real catalog tools, quantities/stock/missing-item boundaries | 0 |
| 05 memory/context | Real graph/checkpointer/store, identity separation, trimming; authored summary snapshots | 0 |
| 06 retrieval | Real lexical ranking, provenance, source edit/refresh, permission/current filtering | 0 |
| 07 RAG | Evidence inspection, empty-evidence abstention, citation-membership rejection/counterexample | 0 |
| 08 evaluation | Frozen twenty-case dataset, development retrieval and per-case report | 0 |
| 09 graph workflows | Actual state/routes/reducers and deterministic outcomes | 0 |
| 10 durable approval | Actual SQLite checkpoints/actions, review and replay boundaries | 0 |
| 11 middleware/security | Actual local authorization/validation/security boundaries | 0 |
| 12 multi-agent | Authored handoff fixtures and outside-source rejection; no quality comparison | 0 |
| 13 MCP | Real FastMCP stdio server, tool discovery/invocation, invalid quantity and cleanup | 0 |
| 14 production | Real HTTP server, authentication/ownership, concurrency, disconnect, restart, idempotent approval/rejection, consent and deadline | 0 |
| 15 capstone | Real retrieval and durable control with an explicit human-authored draft | 0 |

Module 13's additional `--scenario unavailable` and `--scenario disconnect` passed against actual transports. The unavailable endpoint stopped with a reported exception; the real direct client's call after context exit failed. The expected `LangChainBetaWarning` is visible, not suppressed.

Module 08 additionally ran twelve development and eight held-out cases against a development-frozen **local** configuration: all returned evidence obeyed current/audience filtering, generated answers remained null, and model calls were zero. Changing k after freezing exited **2**; attempting human grading of a saved report with no generated answer exited **2**.

## Regressions and fixes

`uv run --no-sync python -m pytest -q`: **16 passed**. These cover retrieval freshness/access, persistent ownership/rejection/edit, separate-process interrupt restoration, idempotent replay, checkpoint/sink binding, live configuration before registration, human-review identity/absence/reassessment, and real tool-runtime owned/forbidden status reads.

- The initial real HTTP smoke accepted an unconsented live start when lexical retrieval found no evidence: deterministic abstention bypassed the later model constructor. A failing-before regression reproduced it. The workflow now validates actual live intent/configuration before registering a new model-driven thread; the regression and complete HTTP smoke pass. No question special case or relaxed assertion was used.
- An evaluation report initially attached a human semantic grade to an ungenerated answer; the reproduction showed `generated_answer: null` with one reported reviewed case. Human review now annotates a **saved** report offline, never a newly generated stochastic result. Unknown/unproduced case grades are rejected, and inappropriate abstention remains a semantic failure. Grader execution errors remain explicit and cause a nonzero CLI exit.
- Real specialist runs initially failed all four coordinator trials: a global one-tool limit counted the structured-response tool as well as delegation. Limits now target `retrieve_policy` and `policy_specialist` individually; all eight paired runs completed within the unchanged business-tool/model bounds. An injected invalid citation after a real specialist result stopped with zero validated handoffs and no replacement answer.
- The HTTP live smoke used a lexical query with no evidence, so it never reached generation and incorrectly expected a provider outage. Both live fixtures now use a corpus-matching returns question. A separate actual service request with evidence and an unreachable configured endpoint returned **502 / OpenAIConnectionError**.
- A genuine malformed model response was initially mislabeled HTTP **400**. The RAG generation boundary now raises `ModelOutputError`, separately handled as sanitized HTTP **502**; the actual same request path proved the corrected classification. Input/state errors still remain 400.
- The first live security trace exposed errors even for the owned Alice thread: an explicit schema forbade the framework-injected `runtime` argument. Inferred tool schema preserves runtime injection while the application still validates public arguments/identity. A real ToolNode reproduction failed before and returned minimal pending status after; the subsequent live agent read Alice, denied Bob, and left both action counts zero. The live lab now rejects missing successful owned inspection.

Tests are deterministic boundary/state proof, not a substitute for the actual MCP/HTTP/CLI smokes or generated semantic review.

## Prerequisites exercised as failures

With key/model/embedding settings empty and consent disabled, actual `--live` commands for Modules 01, 02, 03, 04, 06 semantic, 07, 12, 14, and 15 exited **2** visibly. No substitute provider, canned model answer, secret output, or paid request was used.

To exercise real model-dependent gates, privately configure an accessible model and key, confirm required capabilities, and explicitly choose `COURSE_ALLOW_LIVE=1`. Semantic/hybrid retrieval needs an accessible embedding model. Hosted LangSmith tracing/evaluation additionally requires credentials and permission to upload content.

## Documentation coverage and rendered surface

Rendered **124 Markdown documents** with the actual Markdown CLI. Verified all **64 lessons** (four per module), **16 lab runbooks**, **16 exercises**, and **16 separate solutions**. Checked **750 local link occurrences**: no missing targets. Counted 244 external reference links; this is not a claim that every remote URL/fragment was freshly reachable.

Opened the rendered documentation in a real browser and followed README → sixteen-row lesson index → Module 08 lesson → evaluation runbook. Observed the real offline-review instructions and captured the rendered surface. The temporary preview tab/server were closed; no HTML course platform or scaffolding was added to the repository.

## Additional offline evaluator smoke

The actual Module 08 CLI annotated an explicitly **human-authored saved-report fixture**, preserved the graded answer and original input file, and recorded inappropriate abstention as a semantic failure even with high numeric fixture grades. Exit **0**. This proves the offline annotation boundary, not a model-quality result.

With configuration/consent empty, actual `--live --judge` execution produced twelve development rows, including one explicit missing-configuration grader error with no valid grade, and exited **2**. No provider request or successful model grade was substituted.

## Gateway-mediated live execution

With explicit bounded-run consent, exercised real **`openai-codex/gpt-6.1-sol:low`** through OMP's credential-backed stdio gateway and a temporary authenticated loopback HTTP bridge. The bridge used a genuine local bearer credential; provider credentials stayed inside the native gateway. It forwarded actual model requests/responses without canned answers or output repair. No public OpenAI API key was provisioned or committed. Model fallback/native retries were disabled for these runs.

| Path | Actual observation |
|---|---|
| 01 direct SDK | Responses classification returned `billing`, completed, 74 input / 5 output tokens; elapsed 3.649 seconds |
| 02 execution modes | `--live --mode all` completed invoke, stream aggregation, async, and two-item batch; labels included billing/technical |
| 03 extraction | Function-calling method passed complete, missing, contradictory, and irrelevant cases with supported/unknown/contradictory/irrelevant records; default JSON Schema returned an invalid category and was rejected |
| 04 catalog agent | Model requested/executed the real two-notebook quote: 2598 USD cents, no stock reservation; bounded termination |
| 05 memory/context | Actual model/tool calls completed same-thread follow-up, separate user/new thread, model summary, and full/trimmed/summarized-context comparisons; not a general recall-quality score |
| 07 agentic RAG | Actual ToolStrategy path answered the 30-calendar-day unused-item policy with RETURN citation, abstained on teleportation, and declined secret/unlimited-refund instructions while citing trusted RETURN rather than MALICIOUS |
| 07 two-step / 09 graph / 10 approval / 15 capstone | Actual JSON-schema generation/classification failed output validation; no accepted model draft or successful live end-to-end approval is claimed |
| 08 frozen evaluation | Actual twelve-row dev and eight-row held-out runs with the same frozen lexical/model/judge configuration both exited 2; failures published below |
| 11 security | After the runtime-schema fix, actual model-selected Alice inspection succeeded, Bob inspection was denied, and action counts stayed zero |
| 12 comparison | After the named-budget fix, all eight one-trial single/specialist runs completed; single used two model calls/one business tool, specialist four/two; invalid real-result handoff was separately rejected |
| 13 MCP | Live agent completed real model-selected tool invocation against the actual FastMCP stdio server; beta warning remains visible |
| 14 HTTP failures | Real configured-client transport failure and actual malformed model-output failure each returned sanitized 502; complete live RAG service scenario remains blocked by JSON-schema output incompatibility |

The stdio gateway **buffers SSE until the stream ends**. Stream reconstruction is exercised; real-time chunk arrival/first-token latency and the interactive input variant are not certified.

Observed **122 gateway model-response frames**, all HTTP 200 at the gateway boundary; application validation still rejected unsuitable outputs. **121 JSON responses** reported a total **41,401 input / 5,085 output tokens**. One SSE response lacks gateway-level aggregate usage in this accounting: unknown, not zero. Counts include failed application trials and before/after runs. No currency charge, public-API pricing equivalence, or exact physical-provider-request count is invented.

Frozen live development rows recorded **11 execution/output-validation failures and one model-grader failure**. Held-out rows recorded **seven execution/output-validation failures, one model-grader failure, and one retrieval miss**; failure categories can overlap. No valid quality score or human-reviewed case grade is claimed. The gateway returned natural text/invalid typed output on JSON-schema requests; schema validation was not relaxed or replaced with fake JSON.

On this small paired sample the specialist doubled logical model calls without adding supported shipping facts; both arms also exposed a lexical returns miss. This is an engineering observation, not calibrated quality or a general architecture ranking.

Temporary bridge processes exited **0**, their listeners stopped, and owned overlay/state directories were removed. No course credential, trace-upload permission, or gateway wrapper was persisted.

## Explicitly unverified or blocked

- **Advisor review waived:** the user explicitly chose to skip the review and disable the session-only native advisor. The setting is false; no persistent configuration change or advisor sign-off is claimed. Earlier task-agent dispatch used the wrong interface.
- Direct public-provider endpoint compatibility and successful provider-native JSON-schema output. The available gateway failed those output checks; two-step RAG, live graph classification, model-drafted approval/capstone, rewrite/rerank, and valid model grades still need a compatible endpoint/model.
- Learned semantic/hybrid embedding relevance: the credential-backed catalog exposes no embedding model, and no public embedding API credential/model is configured. No fake vectors, provider substitution, or semantic-quality claim is used.
- Currency cost, interactive input, real-time stream delivery, stochastic robustness, and independent human grader calibration. Recorded token usage and limited generated examples do not prove them.
- Hosted tracing/evaluation/deployment and public/multi-host production suitability. The service is a bounded localhost/POSIX/SQLite lab, not a production security certification.
- Actual learner mastery, delayed retention, peer teach-back, and learning records. Authoring a course or running examples cannot establish them.
- Context7/codebase-memory MCP operations and graph-index updates: those tools were not exposed. LSP reference operations reported no configured server. Current official sources, file reads, runtime execution, and deterministic regressions were used instead; unavailable tooling is not claimed as successful.

At the initial baseline, course key/model/live consent were absent. User-approved temporary child environments subsequently enabled genuine OpenAI-Codex gateway calls. That access does not supply public OpenAI JSON-schema/embedding capabilities. The remaining prerequisite is privately configured compatible provider/embedding access; advisor review is no longer a completion requirement.
