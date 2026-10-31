# Changelog

## Unreleased

- Render every Markdown page as readable HTML (`scripts/build_html.py`) with lesson previous/next links and GitHub-style heading anchors; add `scripts/check_links.py` for links and `#anchors`.
- Normalize all lesson titles to `MM.L — Title` and add an "In plain words" summary to every lesson.
- Add real captured `--check` output to each lab README.
- Remove authoring-session notes from learner-facing files and correct statements that contradicted the verification record.
- Replace the Deep Agents retrieval link in lessons 07 and 15.1 with the LangChain retrieval guide.
- Remove repeated disclaimer and hint-ladder boilerplate; keep the practice policy once in `lessons/README.md`.
- Rewrite the root README as a usage guide: quickstart, free versus live runs, environment variables, layout, tests and HTML rebuild.

## Unreleased — 2026-10-12

- Implement all sixteen core modules: sixty-four lessons, sixteen real Python labs/runbooks, independent exercises and separate solutions, source references, navigation, glossary, API map, and troubleshooting.
- Deliver catalog tools, isolated conversation state, permission/provenance-aware lexical/semantic/hybrid retrieval, two-step/optional agentic RAG, frozen evaluation protocol, explicit graph workflows, durable human approval, bounded specialist comparison, actual MCP, localhost serving, and integrated support capstone.
- Rename the course distribution/package to `langchain-learning` / `langchain_learning` so the external library imports correctly. Preserve the original `neuron` function; replace the obsolete generated greeting with course navigation/check/run CLI. No legacy aliases.
- Lock the Python 3.14-compatible environment and explicitly configure the Tsinghua package index (see README). Exclude private configuration, tokens, local state, and transient output.
- Enforce live configuration/consent before persisting model-driven workflow starts, including empty-evidence requests. Apply human semantic review to saved reports offline rather than rerunning the graded target; preserve grader and boundary failures.
- Fix live-discovered tool-runtime injection and specialist budget failures without weakening identity/source validation. Distinguish malformed model output from caller input as HTTP 502, and ensure the HTTP outage fixture actually reaches generation.
- Record actual local CLI/MCP/HTTP execution and meaningful regression coverage in [verification](docs/VERIFICATION.md), plus the author's live-run successes and capability failures. No model-quality, currency-cost, or learner-mastery result is fabricated.
