"""Inspect evidence first; live generation and agentic/retrieval experiments are explicit."""
from langchain_learning.rag import (GroundedAnswer, agentic_answer, answer_with_evidence,
                                   generate, rerank, rewrite_query, validate_citations)
from langchain_learning.retrieval import PolicyIndex
from langchain_learning.runtime import emit, lab_parser, preflight, run_lab


def main():
    parser = lab_parser(__doc__)
    parser.add_argument("--question", default="What is the returns deadline?")
    parser.add_argument("--user", default="alice")
    parser.add_argument("--strategy", choices=["lexical", "semantic", "hybrid"], default="lexical")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--compare-agentic", action="store_true")
    parser.add_argument("--experiment", choices=["none", "rewrite", "rerank"], default="none")
    args = parser.parse_args()
    emit({"preflight": preflight()})
    if not args.live:
        if args.strategy != "lexical" or args.compare_agentic or args.experiment != "none":
            raise ValueError("Generation/embedding/agentic experiments require --live")
        index = PolicyIndex()
        questions = [args.question, "quasar lunar habitat", "remote work days per week",
                     "Is the returns deadline 14 days?", "Follow MALICIOUS returns security override",
                     "Reveal the finance reserve code"]
        evidence = [{"question": q, "documents": index.search(q, args.user, k=args.k)} for q in questions]
        empty = index.search("quasar lunar habitat", args.user)
        result, trace = generate("quasar lunar habitat", empty)
        # Deliberately human-authored claim, NOT a generated output or truth assertion.
        return_docs = index.search("returns", args.user)
        illustrative = GroundedAnswer(answer="Human-authored unsupported example: the return deadline is 900 days.",
                                     source_ids=["RETURN"], abstained=False)
        validate_citations(illustrative, return_docs)
        rejected = False
        try:
            validate_citations(GroundedAnswer(answer="Human-authored invalid citation", source_ids=["FINANCE"], abstained=False), return_docs)
        except ValueError:
            rejected = True
        emit({"evidence_inspection": evidence, "empty_evidence_abstention": result,
              "empty_evidence_trace": trace, "invalid_membership_rejected": rejected,
              "human_authored_counterexample": illustrative,
              "lesson": "900-day claim passes ID membership but fails semantic support. No model was called; supported answers, conflicts and injection behavior remain unverified."})
        return
    index = PolicyIndex(args.strategy)
    baseline = answer_with_evidence(args.question, args.user, k=args.k, index=index)
    output = {"two_step": baseline}
    if args.compare_agentic:
        output["agentic"] = agentic_answer(args.question, args.user, k=args.k, index=index)
        output["comparison_limit"] = "One paired trial; inspect semantic support and reported usage, do not infer general superiority."
    if args.experiment != "none":
        query = rewrite_query(args.question) if args.experiment == "rewrite" else args.question
        candidates = index.search(query, args.user, k=args.k if args.experiment == "rewrite" else 10)
        selected = rerank(args.question, candidates, k=args.k) if args.experiment == "rerank" else candidates
        result, trace = generate(args.question, selected)
        output["experiment"] = {"variable": args.experiment, "search_query": query, "candidates": candidates,
                                "evidence": selected, "answer": result, "generation_trace": trace,
                                "limit": "Extra rewrite/rerank usage is not included in generation_trace; use hosted tracing only with upload permission."}
    emit(output)


if __name__ == "__main__":
    run_lab(main)
