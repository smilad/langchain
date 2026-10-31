# LangChain learning lab

A Python learning repository for understanding LangChain from foundations to advanced applications—and creating detailed resources that other learners can reuse.

**Implementation status:** sixteen modules, sixty-four lessons, sixteen runnable labs, separate exercises/solutions, and Projects A/B/C/capstone are authored. All sixteen local lab checks pass. Bounded live OpenAI-Codex checks have exercised real generation and tools; JSON-schema output and embeddings remain provider-dependent limits. The user explicitly waived advisor review; the session-only advisor is disabled. See [verification and limits](docs/VERIFICATION.md).

## Start here

1. Read [MISSION.md](MISSION.md) for the learning goal and current assumptions.
2. Attempt the [prerequisite diagnostic](ROADMAP.md#2-prerequisite-diagnostic).
3. Follow [ROADMAP.md](ROADMAP.md): sixteen core modules, four projects, practical mastery gates, and optional advanced tracks.
4. Use [RESOURCES.md](RESOURCES.md) for annotated official documentation, courses, teaching research, and skill recommendations.
5. Open the [lesson index](lessons/README.md), then attempt each module's exercises before reading its separate solution.
6. Use [the teaching guide](docs/TEACHING_GUIDE.md) for teach-back and delayed review. The [implementation plan](docs/superpowers/plans/2026-10-12-langchain-learning-resources.md) records delivered artifacts and remaining live/learner evidence, not a learner-completion certificate.

## Run the course

From this checkout with Python 3.14 and `uv`:

```bash
uv sync --locked --system-certs
uv run --locked langchain-learning list
uv run --locked langchain-learning check
uv run --locked langchain-learning run 00 --check
```

Continue with `run 01 --check` through `run 15 --check`, or use each lab's direct Python command. Checks exercise real local schemas, tools, retrieval, graph/store persistence, MCP, and localhost HTTP where relevant; they do not substitute fake model output. Each lab README explains what its check does and does not prove.

For paid/live work, copy `.env.example` to a private `.env` only if none exists, then set an actual `OPENAI_API_KEY`, an accessible `COURSE_MODEL`, and deliberate `COURSE_ALLOW_LIVE=1`. Semantic/hybrid retrieval additionally needs `COURSE_EMBEDDING_MODEL`. OpenAI is the implemented provider baseline; compatible endpoints must support the specific API/capability used, including the Responses API in Module 01. Model IDs and prices are not hardcoded.

```bash
uv run --locked langchain-learning run 01 --live
```

Never commit `.env`, local state, bearer tokens, or private traces. Hosted LangSmith uploads and paid deployment are separate optional decisions. Missing live prerequisites produce visible errors, not canned successes.

## Learning progression

| Stage | Modules | Outcome |
|---|---|---|
| Foundations | 00–03 | Reproducible environment, model calls, messages, typed outputs |
| Applications | 04–08 | Tool assistant, memory, retrieval/RAG, traces, evaluation |
| Advanced control | 09–13 | Graph workflows, durable approval, security, multi-agent and MCP boundaries |
| Production and transfer | 14–15 | Operational application, measured capstone, reusable tutorial |

Suggested core effort: **91–127 hours**, adaptable to prior knowledge. Progress depends on demonstration, not watching every video.

## Projects you will build

- **A — Catalog assistant:** real local read-only lookup and calculation tools.
- **B — Policy-document assistant:** retrieval, source-supported answers, abstention, evaluation.
- **C — Approval workflow:** explicit graph state, persistent pause/resume, safe synthetic side effects.
- **Capstone — Support assistant:** combine grounding, evaluation, approval, and operational checks; teach another learner to reproduce it.

## Environment decisions

The course distribution/package is now `langchain-learning` / `langchain_learning`; external `import langchain` resolves to the installed library. The original user-authored `neuron` function is preserved in the renamed package; the generated greeting is replaced by the course CLI, without legacy aliases.

Python 3.14.0, the lockfile, real MCP calls, and persistent local workflows were exercised together. The configured package index is the Tsinghua TUNA mirror: PyPI artifact DNS was unreachable during setup, while this mirror supported the observed locked install. Hashes remain in `uv.lock`; review index/network policy before intentionally changing resolution. Labs run from the source checkout because lessons, corpora, and entry points are repository resources—not a claimed standalone wheel bundle.

## Teaching principles

- Official sources and version-aware examples, not a collection of outdated tutorials.
- Short explanations followed by worked examples, guided practice, independent variations, and failure diagnosis.
- Retrieval practice and delayed review; keep solutions separate from exercise prompts.
- Trace actual execution and measure results; a fluent answer is not proof of correctness.
- Record demonstrated understanding rather than marking topics learned because they were covered.

Research and execution baseline: **2026-10-12**. Consult [resource freshness](RESOURCES.md#freshness-and-gaps), [tested versions and blockers](docs/VERIFICATION.md), and [troubleshooting](reference/TROUBLESHOOTING.md). Authored content and passing checks do not establish learner mastery.
