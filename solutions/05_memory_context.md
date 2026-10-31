# Module 05 solution — Scope, retention and request selection

Attempt the [exercise](../exercises/05_memory_context.md) first. The examples explain executable mechanics but do not claim an observed learner/model result. Python >=3.14 target; exact dependencies are in the lockfile, with integration verification pending.

## Part A: actual stores and checkpoints

Use the lab's helpers in a local copy, or load their definitions without executing the CLI:

```python
import runpy
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

lab = runpy.run_path("labs/05_memory_context/main.py")
store, saver, sessions = InMemoryStore(), InMemorySaver(), lab["Sessions"]()
save = lab["save_preference"]
select = lab["selected_preference"]
save(store, "alice", "short", consent=True)
save(store, "bob", "detailed", consent=True)
graph = lab["checkpoint_graph"](store, saver)
a = sessions.config("alice", "alice-shopping")
a_new = sessions.config("alice", "alice-new")
b = sessions.config("bob", "bob-shopping")
graph.invoke({"user_id": "alice", "messages": [HumanMessage("Budget 4500 cents.")]}, a)
graph.invoke({"user_id": "alice", "messages": [HumanMessage("Look up desk-lamp.")]}, a)
graph.invoke({"user_id": "alice", "messages": [HumanMessage("New conversation.")]}, a_new)
graph.invoke({"user_id": "bob", "messages": [HumanMessage("Look up pen-set.")]}, b)
assert len(graph.get_state(a).values["messages"]) == 2
assert len(graph.get_state(a_new).values["messages"]) == 1
assert graph.get_state(a_new).values["selected_preference"] == {"style": "short"}
assert graph.get_state(b).values["selected_preference"] == {"style": "detailed"}
try:
    sessions.config("bob", "alice-shopping")
except PermissionError:
    pass
else:
    raise AssertionError("Cross-user checkpoint access permitted")
```

The reject occurs before `.get_state` or `.invoke`; redacting a final answer would be too late. The registry is a process-local demonstration, not an authentication system. In production, derive identity from authenticated context and enforce durable thread ownership at every read/write/resume boundary.

For consent and value validation, catch `PermissionError` for `consent=False` and `ValueError` for an unsupported style; compare the exact store document before/after. Do not catch all exceptions, because an unrelated bug must not masquerade as correct rejection. Delete with `store.delete(("preferences", "alice"), "response_style")`. Future selection returns `{}`, but previous graph snapshots still contain the earlier selection. That observation disproves a claim of comprehensive erasure.

## Part B: why reconstruction is not restart proof

The same saver/store objects own their dictionaries independently of the compiled graph. A new graph referencing them can recover state; new objects have no history. All disappear at process exit. A database-backed checkpointer addresses thread-state durability; a persistent store addresses cross-thread documents. Neither automatically authenticates users, persists our registry or implements complete data erasure. Module 10 handles durable checkpoints and Module 14 adds stronger request boundaries.

## Part C: a controlled context experiment

List original facts before comparing answers. With the early budget, a long unrelated message and a last quote request, recent trimming can remove the budget entirely. The latest agent should not reconstruct 4500 cents from catalog price or another user's history. A human-authored summary may explicitly retain it; label that text as supplied human context, never generated output.

The live lab uses a real model to produce a summary, then separate fresh `create_agent` instances for full, trimmed and summarized inputs. This prevents saved history from silently restoring discarded details. Inspect the supplied message lists, summary and new tool calls. Current stock/price must be rechecked. A generated summary might omit units or change the budget; those are summarization errors, not integer-cent arithmetic defects.

One comparison is mechanism evidence, not a reliable ranking of context strategies. Declare trial count for variability and evaluate support, omissions and token usage separately. When credentials are missing, retain deterministic state/context evidence and mark generated-summary/recall behavior unverified.

## Teach-back and review

History is thread-scoped application state; explicit style is user-scoped store data; selected context is the current model request; neither is model-weight training. Prompt language does not authorize a namespace or authenticate a thread. Request trimming does not delete storage. Review with new identities/constraints in Modules 11 and 14.

Sources consulted 2026-10-12: [short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory), [long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory), [runtime](https://docs.langchain.com/oss/python/langchain/runtime).
