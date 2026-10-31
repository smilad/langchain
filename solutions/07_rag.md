# Module 07 solutions — inspect claims, not just structure

Attempt [the exercises](../exercises/07_rag.md) first. [Verification](../docs/VERIFICATION.md) separates local boundaries from unexercised generated behavior.

## 1. Boundaries

Retrieval returns authorized `Document` evidence. The generation prompt receives evidence as data, including IDs and trust; it must not promote document instructions to application policy. `GroundedAnswer` requires an answer, citations for non-abstention, no citations for abstention, and no duplicate citations. `validate_citations` rejects IDs not present in trusted selected evidence. That check cannot establish that the text actually supports every assertion.

## 2. Failure taxonomy

A current deadline should use the current return source, not the obsolete fourteen-day revision. Unrelated evidence should produce abstention, not a guessed policy. Two current contradictory remote-work sources require uncertainty/conflict handling, not choosing the prettier answer. Alice's finance query must not expose finance-only text. The malicious public fixture is untrusted retrieved data; its presence must not make its instruction authoritative. Local inspection proves filtering and data boundaries, not how an unrun model responds to an injection.

## 3. Citation counterexample

A nine-hundred-day answer can cite a retrieved `RETURN` source and pass ID membership while directly contradicting its thirty-day text. Evaluate period, calendar versus business days, delivery versus purchase as start event, unused condition, and receipt. Record a passage supporting each claim or mark lack of support. The local nine-hundred-day example is explicitly human-authored to demonstrate this logical gap; it is not an observed hallucination.

## 4. Actual generation

With a configured model, inspect selected evidence, parsed answer, timing, and usage. Check substantive claims before approving the draft. Empty evidence returns an explicit deterministic abstention with zero model calls; it does not generate a fake successful answer. With evidence, the code calls the real configured model and reports structural/citation errors rather than using canned replacement prose. A missing provider leaves supported-answer quality unverified.

## 5. Rewrite and rerank

Rewrite changes the search query; it can recover a paraphrase or lose important constraints. Reranking changes which candidates become final evidence; it can improve ordering or remove needed conditions. Both add real model calls. The final generation trace covers only that generation step, so do not present it as total experiment cost. Tune on development cases, keep the baseline, and report the added calls separately.

## 6. Agentic decision

The agent may choose queries/tool calls, which increases flexibility and adds control/failure overhead. Identity is bound outside model arguments and evidence must still be authorized. One paired example cannot establish a general improvement. Prefer the two-step design when review finds no measured benefit from agentic complexity; carry the quality comparison into Module 08's explicit protocol.
