# LangChain Learning Resources Implementation Plan

> **Execution status:** all core lesson/lab/exercise/solution artifacts are delivered. Checked items mean authored or exercised work, not learner mastery or provider quality. The user explicitly waived advisor review and the session-only advisor is disabled. Bounded real OpenAI-Codex gateway runs have exercised generation and tools; JSON-schema compatibility and embedding access remain explicit limits. No advisor sign-off is claimed.

**Goal:** Turn the researched curriculum into a detailed, runnable Python learning course, from first model call to a measured, resumable support-assistant capstone.

**Architecture:** Markdown lessons explain one concept at a time; Python labs exercise real behavior; separate exercise/solution files support retrieval and independent practice. Four evolving projects reuse earlier work instead of creating unrelated demos. Learning records are created only after demonstrated understanding.

**Tech stack:** Existing Python `>=3.14` and `uv_build`; `uv` for environment/locking; current LangChain 1.x APIs and separately installed integrations; LangGraph where explicit control is needed; optional LangSmith tracing/evaluation. Verify actual resolved versions and provider capabilities at implementation time.

**Spec:** [MISSION.md](../../../MISSION.md), [ROADMAP.md](../../../ROADMAP.md), and [TEACHING_GUIDE.md](../../TEACHING_GUIDE.md).

## Global constraints

- This living authoring plan records implemented artifacts and outstanding evidence. See [VERIFICATION.md](../../VERIFICATION.md) for observed execution, version pins, and blockers.
- Keep the existing Python requirement `>=3.14` unless a reproduced integration incompatibility requires an explicit compatibility decision.
- Rename the local distribution/package to `langchain-learning` / `langchain_learning` before adding the external `langchain` dependency. Remove old names/entrypoints in that same cutover; no aliases.
- Core curriculum: Modules 00–15, four lessons each, the stated module gates, and Projects A/B/C/capstone. Optional tracks are not substitutes for missing core material.
- English Markdown and runnable Python are authoring defaults, not confirmed learner preferences. Do not build an HTML course platform merely to follow a skill's default layout.
- Use synthetic/public data. Secrets, private documents, paid deployment, and hosted trace uploads require an explicit learner decision.
- No invented model answers, fake lookup tools, mocks presented as integrations, or unsupported claims of successful execution.
- Re-read current official documentation before implementing an API example; record versions actually exercised. Do not pin a release number merely because it was current during research.
- Every required lab has a no-secret setup check and an explicit live-run mode. A missing credential is a reported prerequisite, not a successful model-call demonstration.

## Review focus

1. Clean checkout / wrong interpreter: environment commands and external-library imports must work outside the author's IDE.
2. Unknown answer / invalid structured output: fail or abstain explicitly rather than fabricate data.
3. Two users / filtered documents: histories and retrieval permissions must not leak across identities.
4. Restart / interrupt replay: approved synthetic actions must not be duplicated and rejected actions must not occur.
5. Nondeterministic generation / evaluation leakage: report per-case evidence and variability; keep held-out cases out of tuning.

These conditions belong in the module lab gates below. Permanent regression tests should cover deterministic boundaries and state transitions where useful; live smoke evidence remains required for model/integration behavior.

## File structure and responsibilities

Files created by the planning deliverable:

| File | Responsibility |
|---|---|
| `README.md` | Entry point and honest status |
| `MISSION.md` | Goal, observable success, and assumptions |
| `ROADMAP.md` | Prerequisite sequence, lesson topics, projects, gates |
| `RESOURCES.md` | Annotated sources, skill recommendations, freshness |
| `docs/TEACHING_GUIDE.md` | Lesson format, feedback, mastery and retention |
| This plan | Ordered implementation tasks and verification |

Implemented artifact layout (learning records are created only after learner demonstration):

| Path | Responsibility |
|---|---|
| `src/langchain_learning/__init__.py` | Renamed existing course package; migrate existing entrypoint consistently |
| `uv.lock` | Reproducible tested dependency resolution |
| `.env.example` | Variable names and safe examples only |
| `.gitignore` | Exclude credentials, local state/indexes, and transient output |
| `lessons/<module-id>_<slug>/01.md` through `04.md` | Four scoped lessons, each with source links and a lab/exercise pointer |
| `labs/<module-id>_<slug>/main.py` | Module lab with a documented direct command |
| `labs/<module-id>_<slug>/README.md` | Setup, input cases, expected behavior, observed evidence, limits |
| `exercises/<module-id>_<slug>.md` | Independent prompts without their answers |
| `solutions/<module-id>_<slug>.md` | Explanations, troubleshooting, and worked solutions |
| `data/catalog.json`, `data/policies/` | Small synthetic catalog and versioned source documents |
| `data/evaluations/rag.jsonl` | Labeled synthetic cases with stable IDs and development/held-out splits |
| `reference/GLOSSARY.md` | Consistent definitions and boundaries |
| `reference/API_MAP.md` | Verified APIs by concept and tested version, not a legacy alias list |
| `reference/TROUBLESHOOTING.md` | Diagnoses grounded in actually encountered failures |
| `learning-records/0001-<insight>.md` | First evidence-backed learning record; created only after learner demonstration |

The module directory names below are the contract for lesson/lab links. Do not create empty directories or placeholder lessons in advance.

## Shared lesson-authoring loop

Apply this loop to each module in Tasks 2–6, using its exact topics and gate in the roadmap:

- [x] Read primary references and record source URLs/date, required credentials, and capability limits; central verification records exercised versions.
- [x] Write four lessons per module with explanations, worked examples, input/output shapes, and references.
- [x] Implement every lab plus independent exercise and separate solution using actual local behavior and real provider paths.
- [ ] Run the actual lab. Exercise the normal path and each named failure case; record observed behavior in its README, without publishing secrets or private data.
- [ ] Check the practical gate, teach-back, diagnosis, and transfer criteria. Add a deterministic regression test only for a meaningful boundary/invariant, not source text or mocked forwarding.
- [x] Maintain the glossary, API map, and root/lesson navigation for delivered content.

A completed lesson has explanations, runnable behavior, exercise feedback, and evidence. A file with headings or a mock-backed demonstration does not satisfy this loop.

## Task 1: Resolve setup hazards and deliver the first runnable module

**Files:** modify `pyproject.toml`; rename `src/langchain/__init__.py` to `src/langchain_learning/__init__.py`; create `uv.lock`, `.env.example`, `.gitignore`, `lessons/00_setup/01.md`–`04.md`, `labs/00_setup/main.py`, `labs/00_setup/README.md`, `exercises/00_setup.md`, and `solutions/00_setup.md`.

**Consumes:** existing metadata and source behavior, read before editing; prerequisite diagnostic.

**Produces:** non-conflicting course package, reproducible environment, setup checker, documented commands.

- [x] Inspect existing source; preserve the user-authored `neuron`, remove the obsolete generated greeting.
- [x] Cut over to `langchain-learning` / `langchain_learning` and `langchain_learning.cli:main`; remove the conflicting old package and entrypoint without aliases.
- [x] Lock and exercise the selected LangChain/OpenAI/LangGraph/SQLite/MCP dependencies on Python 3.14.
- [x] Deliver a no-request setup checker with interpreter/library versions, import origin, and non-secret configuration-presence evidence.
- [x] Author Module 00 and its diagnostic exercise/solution, including interpreter and missing-configuration diagnosis.
- [x] Run locked sync and the actual setup CLI in a fresh temporary environment; external `langchain` resolves to that environment's site-packages.
- [x] Publish setup results/navigation; distinguish implemented later modules from their unverified provider-dependent gates.

**Acceptance:** Module 00 gate, reproducible commands, no namespace conflict, and no secret exposure. Setup success alone is not evidence of a successful provider request.

## Task 2: Deliver the model-call foundations

**Modules / directories:** `01_llm_baseline`, `02_models_messages`, `03_structured_output`.

**Consumes:** Task 1 environment; current model/messages/structured-output references.

**Produces:** direct-call baseline, equivalent LangChain model lab, schema-based extraction lab, and twelve lessons.

- [x] Author Modules 01–03 and actual direct-provider/model/structured-output paths, with local checks and independent practice.
- [x] Document `--live` commands and actual provider/model/consent prerequisites. Missing configuration fails visibly.
- [ ] Show response shape and reported usage from a real run. Exercise missing credentials, streamed content/events, and unsupported/invalid structured-output behavior where the chosen provider allows it.
- [x] Explain direct SDK versus LangChain responsibilities and actual Runnable/LCEL extraction composition without legacy agent aliases.

**Acceptance:** Modules 01–03 gates, not copied documentation output. No prerequisite is silently replaced with a fake model.

## Task 3: Deliver Project A and conversation-state lessons

**Modules / directories:** `04_tools_agents`, `05_memory_context`.

**Additional files:** `data/catalog.json`.

**Consumes:** typed outputs/model invocation; synthetic catalog owned by this task.

**Produces:** real local lookup/calculation tools, `create_agent` demonstration, isolated conversation state, eight lessons.

- [x] Author Modules 04–05, their actual tools/state labs, independent exercises, and solutions.
- [x] Define and exercise real synthetic-catalog identifiers, stock/integer-price rules, and missing-item behavior.
- [ ] Run the assistant and inspect requested tool arguments, actual tool outputs, and the final message for present/absent items and invalid arguments.
- [x] Exercise two identities/threads, graph/store operations, context trimming, and human-authored snapshots, then actual gateway-backed follow-up, personalization context, model summary, and context variants. These runs are not a general memory-quality or learner-mastery claim.

**Acceptance:** Modules 04–05 gates, bounded execution, explicit unavailable-item result, and no cross-user state.

## Task 4: Deliver Project B and an evaluation baseline

**Modules / directories:** `06_retrieval`, `07_rag`, `08_evaluation`.

**Additional files:** `data/policies/`, `data/evaluations/rag.jsonl`.

**Consumes:** invocation/structured output; trace concepts from Project A.

**Produces:** provenance-preserving index, two-step RAG assistant, evaluation report, twelve lessons.

- [x] Author Modules 06–08 with actual retrieval/generation/evaluation paths and separate practice.
- [x] Deliver provenance/version/permission metadata, current conflicts, and an explicitly untrusted malicious fixture.
- [x] Implement two-step RAG before optional agentic retrieval; expose evidence and preserve explicit failures.
- [x] Freeze exactly twenty cases and the 12/8 split; exercise configuration registration, mismatch rejection, and local development/held-out retrieval. Human grades annotate saved outputs without rerunning generation.
- [ ] Run normal, no-answer, conflicting/outdated, authorization-filter, and malicious-source cases. Verify citation support, not only citation formatting.
- [ ] Change one retrieval variable and compare per-case held-out outcomes, latency, and reported usage/cost when available. Clearly label estimated cost and its pricing assumptions.

**Acceptance:** Modules 06–08 gates and documented limitations of a small benchmark. Cloud tracing is optional; private data upload is never automatic.

## Task 5: Deliver Project C, durable approval, and security

**Modules / directories:** `09_graph_workflows`, `10_durable_approval`, `11_middleware_security`.

**Consumes:** Project B retrieval/evaluation and isolated state concepts.

**Produces:** explicit graph, persistent human-review pause, safe local action sink, twelve lessons.

- [x] Author Modules 09–11, actual graphs/approval/security paths, exercises, and solutions.
- [x] Exercise deterministic routes, partial updates, and reducers before optional real model classification.
- [x] Persist checkpoints/ownership/action identity; interrupt before the local synthetic action and enforce replay idempotency.
- [x] Exercise rejection, approval, edit, separate-process restoration, actual HTTP server restart, and owned action state.
- [x] Exercise local thread/tool/secret boundaries and treat retrieved instructions as data. Model injection resistance remains a live gate.
- [x] Preserve meaningful deterministic rejection/replay/ownership/consent regressions. Real agent-dependent traces remain unverified.

**Acceptance:** Modules 09–11 gates. Persistent pause/resume and no duplicate effect must be demonstrated across process restart.

## Task 6: Deliver advanced integration and operational lessons

**Modules / directories:** `12_multi_agent`, `13_mcp`, `14_production`.

**Consumes:** Project C, evaluation cases, and established security boundaries.

**Produces:** measured specialist experiment, actual local MCP client/server interaction, locally served workflow, twelve lessons.

- [x] Author Modules 12–14, actual bounded comparison/MCP/HTTP paths, exercises, solutions, and runbooks.
- [ ] Compare one specialist pattern against the single-agent baseline. A finding that the baseline is better is a valid lesson result.
- [x] Run the actual FastMCP server/client/tool adapter, invalid quantities, unavailable endpoint, disconnect, and context cleanup. Model-selected MCP tools remain unverified.
- [x] Deliver and exercise localhost HTTP serving with authentication, bounded workers/deadlines, durable state, and documented startup/shutdown.
- [ ] Launch the served application and exercise concurrent identities, a cancelled request, an upstream failure, and resumption after restart. Report observed latency and state behavior.

**Acceptance:** Modules 12–14 gates, no fake server, no unbounded execution, and a runbook usable without the IDE.

## Task 7: Deliver capstone and learning-transfer evidence

**Module / directory:** `15_capstone`.

**Consumes:** verified Projects A/B/C, evaluation method, and operational runbook.

**Produces:** integrated support assistant, four lessons, reproducible tutorial, evaluation/limitations report.

- [x] Author Module 15's integrated capstone, four lessons, runbook, exercise, and solution.
- [x] Run the local capstone with actual retrieved evidence, explicit human draft, restored review, ownership checks, reject/edit/approve, and exactly one idempotent local action. Fresh locked environment/setup CLI is also exercised; real model drafting remains unverified.
- [ ] Evaluate held-out and adversarial cases; publish failures as well as successes and distinguish estimated from observed cost.
- [ ] Ask the learner to adapt one corpus/input constraint independently and teach back the data/control flow. Record demonstrated understanding only after this occurs.
- [x] Publish authored/implemented status with local/live execution evidence and explicit remaining provider/learner gates. Advisor review was waived by the user; keep optional tracks separate.

**Acceptance:** complete core curriculum and runnable capstone, not an integrated happy-path demo alone.

## Handoff

Recommended sequence: implement Task 1 first, then review one completed lesson and its lab before multiplying the format. Tasks 2–7 consume earlier projects; they are not independent work to dispatch blindly in parallel. Within a later task, source curation or independent exercise authoring may run concurrently once APIs and file ownership are fixed.

Execution evidence is in [VERIFICATION.md](../../VERIFICATION.md). Real OpenAI-Codex model requests were sent with explicit user consent through the credential-backed gateway; no embedding calls, hosted uploads, learner-mastery record, or advisor sign-off are fabricated. Remaining unchecked gates require compatible provider/embedding access or an actual learner demonstration.
