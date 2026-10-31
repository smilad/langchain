# Module 12 solutions — extra agents must earn their overhead

Attempt [the exercises](../exercises/12_multi_agent.md) first. [Verification](../docs/VERIFICATION.md) records local contract proof; paid comparisons are not invented.

## 1. Pattern selection

A single agent owns one tool loop. A router selects an appropriate bounded destination. A handoff transfers conversational control and requires explicit context/identity ownership. Delegation returns a specialist result to an owner who remains accountable. Skills may change one agent's instructions without creating another process or authority. This lab compares one bounded specialist against a single-agent baseline; it does not implement every pattern named in the conceptual lesson.

## 2. Evidence scope

The application retrieves authorized evidence for the original request and fixes permitted source IDs outside model arguments. `validate_handoff` rejects outside-source citations and inconsistent abstention. Its accepted shape does not prove the draft's claims follow from those sources. The check-mode answer fixtures are labeled authored boundary inputs, not real model outputs or a successful quality experiment.

## 3. Comparison

Four questions × two patterns × two trials produces sixteen real runs. Alternate pattern order to reduce one order effect; preserve evidence and question between patterns. The specialist path includes orchestration plus specialist calls, so compare total nested work, not only the final outer message. Keep enough actual outputs for human support/security review.

## 4. Bounds and accounting

Single pattern bounds four logical model calls and two tool calls; the nested specialist pattern bounds seven logical model calls and three tool calls across its outer and inner loops. Recursion limits bound graph execution as well. Provider retries may produce more network requests than callbacks count, and long generations change monetary cost. Report actual boundary counts, provider-reported tokens where present, missing usage, and elapsed time. Do not turn absent usage into zero spend.

## 5. Fault injection

After a real specialist result, the explicit fault mode replaces its source IDs with an outside ID. The handoff validator must reject it; the trial records a failed status/error type and performs no action. That demonstrates a boundary stop, not natural model failure frequency. The ordinary comparison raises visibly for failed trials; explicit fault mode records expected failures for diagnosis.

## 6. Decision

Review correctness, grounding, abstention, instruction resistance, latency, and reported usage case by case. Retain the specialist only when the measured benefit justifies complexity. Without credentials, a useful completed local exercise proves the handoff guard and specifies the comparison protocol; it cannot choose a winner from imaginary model results.
