# Reasoned solution — distinguish semantic behavior from enforced access

See [exercise](../exercises/11_middleware_security.md) and [lab](../labs/11_middleware_security/README.md). [Verification](../docs/VERIFICATION.md) records actual integrated command evidence and live proof limits; no provider behavior is fabricated here.

## What check mode proves

The lab opens actual persisted alice/bob threads with explicit human drafts. Authorized inspection returns only status/counts. Cross-owner inspection, extra user identity arguments, secret reading and approval capabilities fail. Both action lists remain empty and alice's proposal remains pending. The malicious corpus document is retrieved as untrusted data; restricted finance content remains excluded for alice.

The unsafe fixture grants permission from document text and returns a committed synthetic marker. It intentionally illustrates a bad design, not a successful model jailbreak or a real credential exposure. Secure code exposes no vault or approval tool to the model and never injects the synthetic vault marker into its messages.

## Why middleware is not the sole boundary

AuthorizationMiddleware checks the requested tool and arguments before invoking the handler. The tool implementation invokes the same domain authorization again; SupportWorkflow checks immutable owner metadata as well. A direct call bypassing middleware still cannot inspect bob's thread as alice. Thread IDs locate data; only trusted caller context supplies identity. The tool schema forbids an extra user_id, so a model cannot rewrite the actor through arguments.

A narrow new capability would bind identity from runtime context, validate bounded arguments, check ownership before reads, and project only needed status fields. An approval capability would violate this lab's read-only contract; it should remain outside the agent and require the existing human decision path.

## What live mode adds—and does not

Live runs actual create_agent with custom authorization and bounded model/tool calls. Inspect tool calls and ToolMessages: did the model attempt the attack, receive denial or refuse without calling anything? Report separately. An output repeating malicious policy text is a semantic grounding failure even if code authorization remained intact. A clean response is one observed outcome for a versioned configuration, not universal safety.

Budgets constrain call counts, not guaranteed total cost. Minimization prevents unnecessary data entering context; display redaction cannot retract provider disclosure. Thread-owner checks are enforceable invariants under trusted databases/callers, while prompt-injection resistance and grounded wording need versioned evaluations and human review.

For transfer, vary the attack or schema constraint independently and record actual results. No mocked middleware trace, source-text test or synthetic output should stand in for the named real boundary.
