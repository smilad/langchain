# Mission: LangChain from foundations to advanced practice

## Why
Build a detailed, reusable learning repository that teaches LangChain from the basics through advanced application development. The user's stated goal is both to learn and to create learning resources; the curriculum should make understanding, practice, and troubleshooting visible rather than collect copied tutorials.

## Success looks like
- Explain model calls, tools, retrieval, agent loops, graph state, and evaluation in your own words.
- Build and debug a tool-using assistant, a source-grounded document assistant, and a resumable workflow.
- Measure quality, latency, and cost; demonstrate failure handling and safe tool boundaries.
- Produce lessons another learner can follow from a clean checkout, with cited sources, exercises, solutions, and observable acceptance criteria.

## Constraints
- Repository: Python `>=3.14`, `uv_build`, locked LangChain/provider/LangGraph/MCP dependencies; course package `langchain_learning`, distinct from the external library.
- The course content and applications are implemented. [Verification](docs/VERIFICATION.md) distinguishes local execution, actual gateway-mediated OpenAI-Codex requests, and remaining provider-capability gates.
- Prior Python knowledge, weekly availability, and a numeric API budget are not established. No public API/embedding credentials or hard spending cap are assumed; live runs need your own key and consent.
- Authoring defaults: English Markdown, runnable Python labs, small lessons, official documentation first. Learning records require learner evidence; installed software and authored lessons are not demonstrated mastery.

## Out of scope for the core course
- Provisioning paid services, uploading private traces/documents without permission, or public/multi-host production certification.
- Claiming live model quality, measured provider cost, peer teach-back, or advisor approval without observed evidence.
- Training foundation models or replacing Python fundamentals with framework memorization. Optional tracks remain optional, not missing core modules.
