# Module 05 independent exercise — Two users, three threads, one minimal memory

Prerequisites: [Module 05 lessons](../lessons/05_memory_context/01.md), the [lab](../labs/05_memory_context/README.md) and actual tool contracts. Attempt first; [solutions](../solutions/05_memory_context.md) are separate. This is an explicit **long-term store preference exercise**, not an instruction to infer user traits from conversation.

## Part A — Prediction and implementation

In a local copy of the lab's deterministic path, use its `Sessions`, `checkpoint_graph`, `save_preference` and `selected_preference` helpers with genuine `InMemoryStore`/`InMemorySaver` objects.

1. With explicit synthetic consent, retain Alice's style `short` and Bob's style `detailed`.
2. Create Alice-shopping, Alice-new and Bob-shopping threads. Append two human messages to the first and one to each other thread.
3. Before running, write which histories/preferences each thread should contain. Prove Alice-new shares her style but not Alice-shopping messages.
4. Attempt Bob access to Alice-shopping through the ownership guard. Prove rejection happens before reading checkpoint state, not after passing another user's context to a model.
5. Reject a preference write without consent and a raw arbitrary preference value. Demonstrate that the rejected operation leaves the existing document unchanged.
6. Delete only Alice's store preference. Explain what future store lookup sees, what old checkpoint snapshots still contain and what you cannot conclude about provider records.

Use real state/store values for assertions. Do not mock `.get`, `.put` or graph invocation. Do not print real private information; the entire exercise is synthetic.

## Part B — Scope versus durability

Rebuild the graph using the same saver and store, then rebuild using new objects. Predict and inspect the difference. Explain why neither case proves process-restart durability. Identify which additional persistent backend and durable ownership binding would be needed before turning this into an authenticated service; do not deploy the lab wrapper.

## Part C — Change the context constraint

Create a conversation with an early 4500-cent budget, one long unrelated discussion and a latest request to quote desk-lamp. Compare the full context, a complete-message recent trim and an explicitly human-authored summary. List every retained/discarded fact.

If credentials, remote consent and budget are available, obtain a real generated summary and run real `create_agent` calls on all three selected contexts. Record exact model inputs, summary omissions and tool-supported totals. Do not invent a generated summary when live execution is blocked. Do not reuse a hidden checkpoint for the comparison, because it would contaminate the experiment.

## Acceptance and diagnosis

Pass with distinct histories, distinct user preferences, rejected cross-user access, consent enforcement, deletion-copy limitations and visible context selection. Explain the difference between actual state leakage and a model guessing an unknown fact. The code guard is the isolation mechanism; a sentence telling the model “do not leak” is not.

Hints: inspect `thread_id`; inspect the exact namespace/key; inspect the original checkpoint versus selected input; then read the solution. Review with a fresh user/thread during Modules 11 and 14. No progress is recorded until you supply genuine evidence.

Sources consulted 2026-10-12: [short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory), [long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory). [Verification](../docs/VERIFICATION.md) records exercised local state/store behavior and unverified real model recall.
