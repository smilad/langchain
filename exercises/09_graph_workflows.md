# Independent exercise — graph contracts under a changed constraint

Prerequisites: all [Module 09 lessons](../lessons/09_graph_workflows/01.md). Do not read the [solution](../solutions/09_graph_workflows.md) until you have a route table and a prediction.

1. Run `uv run python labs/09_graph_workflows/main.py --check`. Draw supported, review and unsupported paths from actual updates. Label channels replaced versus reduced and identify where the supported branches join.
2. In your own exercise copy, add an independent `provenance_check` branch that examines evidence requirements without mutating the shared input. Include its event in the reducer. Update the fan-in dependency so draft waits for every required branch. Explain whether this branch can truly run alongside retrieval if it needs retrieval output; move it after retrieval if necessary. Dependency correctness wins over cosmetic parallelism.
3. Change the deterministic classification rules for a new support topic. Write a route matrix first, including an overlap case and an unrelated request. Explain rule precedence. Do not describe fixture text as generated output.
4. Reproduce the missing-reducer and nontermination failures. Predict the colliding key or repeating node before execution. Repair the contract, not just the exception visibility.
5. With explicit provider consent, run all three `--live --question` commands from the lab README and an unfamiliar wording. Record actual classification, source support and draft origin separately. Missing credentials mark the live gate unverified; local graph evidence remains meaningful.

## Submission and gate

Supply commands/output, a node read/write table, the route matrix, your repaired graph and the dependency justification. Practical execution, explanation, fault diagnosis and the changed constraint are required; the model's chosen label need not match your expectation to prove graph execution, but a bad classification must be reported.

## Hint ladder

First locate the node that supplies the missing field. Next inspect the edge/barrier and reducer declaration. Only then consult the official Graph API and solution. A week later draw the graph from memory and implement a fresh branch with documentation allowed. No learning record is created until you demonstrate the behavior.
