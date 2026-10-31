# LangChain from foundations to advanced practice

A hands-on Python course: 16 modules, 64 short lessons, 16 runnable labs, exercises with separate solutions, and a capstone support assistant. You learn LangChain and LangGraph by running small, inspectable programs: model calls, tools, memory, retrieval and RAG, evaluation, graph workflows, human approval, security, multi-agent, MCP and production serving.

Most of the course runs **free, offline and without an API key**. Steps that call a real model are marked `--live` and cost money, so they stay off until you turn them on.

## Who it is for

- You can read basic Python. The first module covers environments, JSON, validation and async, but it is not a Python tutorial.
- You are happy to run commands in a terminal.
- Not sure about your level? Take the [prerequisite diagnostic](ROADMAP.md#2-prerequisite-diagnostic) first.
- You want to understand how the pieces work and fail, not just copy a working demo.

## Quickstart (about 5 minutes)

You need **Python 3.14** and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/smilad/langchain.git && cd langchain
uv sync --locked --system-certs      # install the locked dependencies
uv run --locked langchain-learning check   # confirm the environment, no model request
uv run --locked langchain-learning run 00 --check   # first lab, fully offline
```

If all three succeed you are ready. If not, see [troubleshooting](reference/TROUBLESHOOTING.md).

## How to read the course

1. Open the **lesson index**: [`lessons/README.html`](lessons/README.html) in a browser (or [`lessons/README.md`](lessons/README.md) on GitHub). GitHub shows the Markdown files; the `.html` pages are for reading on your own machine, with previous/next links.
2. Each lesson opens with an **In plain words** summary, then a warm-up, a mental model, a worked example, practice, and a check you can use to see whether you understood it.
3. Run the lesson's lab, then try the module exercise in [`exercises/`](exercises/) **before** opening its solution in [`solutions/`](solutions/).
4. Every lab README ends with real captured `--check` output, so you can compare your run with it.

Suggested pace: 91–127 hours in total. Move on when you can demonstrate the module's gate in [the roadmap](ROADMAP.md), not when you have read every page.

## Free checks and paid live runs

| Mode | Command | Needs | Cost |
|---|---|---|---|
| Check | `uv run --locked langchain-learning run NN --check` | nothing | free |
| Live | `uv run --locked langchain-learning run NN --live` | API key, model, consent | pays your provider |

Live runs refuse to start unless `OPENAI_API_KEY`, `COURSE_MODEL` and `COURSE_ALLOW_LIVE=1` are set (plus `COURSE_EMBEDDING_MODEL` for semantic or hybrid retrieval). Copy `.env.example` to `.env` (it is git-ignored) and fill it in:

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | your provider key |
| `COURSE_MODEL` | an accessible chat model with tool calling and structured output |
| `COURSE_ALLOW_LIVE` | set to `1` to consent to remote requests and charges (default `0`) |
| `COURSE_EMBEDDING_MODEL` | only for semantic and hybrid retrieval |
| `OPENAI_BASE_URL` | optional OpenAI-compatible endpoint; it must support the APIs a lab uses (Module 01 needs the Responses API) |
| `COURSE_STATE_DIR` | optional folder for local state (default `.course/`) |
| `COURSE_AUTH_TOKENS` | module 14 only: JSON map of bearer token to user (`alice`, `bob`, `finance`) |
| `LANGSMITH_TRACING` | `false` by default; `true` uploads inputs and outputs to LangSmith |

Model IDs and prices are not hard-coded. Never commit `.env`, tokens, local state or private traces.

## Run the tests

```bash
uv run pytest -q
```

## The 16 labs

`uv run --locked langchain-learning list` prints the lesson and lab for each module. Or run a lab directly: `uv run python labs/04_tools_agents/main.py --check`.

| Stage | Modules | You will build or learn |
|---|---|---|
| Foundations | 00–03 | Reproducible environment, model calls, messages, typed output |
| Applications | 04–08 | Tool assistant, memory, retrieval and RAG, traces, evaluation |
| Advanced control | 09–13 | Graph workflows, durable approval, security, multi-agent, MCP |
| Production and transfer | 14–15 | A served application, a measured capstone, a tutorial for someone else |

Projects: **A** catalog assistant, **B** policy-document assistant, **C** approval workflow, and the **capstone** support assistant that combines them.

## Repository layout

| Path | What is in it |
|---|---|
| `lessons/` | 64 lessons in Markdown and HTML, plus the index |
| `labs/` | One runnable lab and README per module |
| `exercises/`, `solutions/` | Independent tasks and their separate solutions |
| `src/langchain_learning/` | The course library (catalog tools, retrieval, RAG, workflow, service) |
| `data/` | Synthetic catalog, policy corpus and evaluation cases |
| `reference/` | Glossary, API map, troubleshooting |
| `docs/` | Teaching guide and the author's [verification record](docs/VERIFICATION.md) |
| `tests/` | Regression tests |
| `scripts/` | `build_html.py` (render Markdown to HTML), `check_links.py` |

## Regenerate the HTML

The `.html` files are generated from the `.md` files. Edit the Markdown, then rebuild:

```bash
uv run --with markdown python scripts/build_html.py
python3 scripts/check_links.py     # verify links and #anchors
```

## Notes you should know

- **Package index.** `pyproject.toml` pins the Tsinghua PyPI mirror because the author could not reach PyPI when setting up. If you can reach PyPI, you may change the `[[tool.uv.index]]` URL, run `uv lock`, and review the new `uv.lock` before committing. Changing the index is an environment decision, not a silent fix.
- **Python name.** The package is `langchain_learning`, so `import langchain` still means the real library.
- **Source checkout only.** Labs read repository files, so run them from a clone, not from an installed wheel.
- **Scope of the evidence.** [The verification record](docs/VERIFICATION.md) is the author's run on 2026-10-12 against one OpenAI-compatible endpoint. It shows what was exercised, not a promise about your provider. Live quality, cost and peer feedback are not claimed.

## Teaching approach

Official sources and version-aware examples; short explanations followed by worked examples, practice and failure diagnosis; retrieval practice and delayed review; results traced and measured, because a fluent answer is not proof. See [the mission](MISSION.md), [the roadmap](ROADMAP.md), [resources](RESOURCES.md) and [the teaching guide](docs/TEACHING_GUIDE.md).
