"""Real bounded agent comparison; deterministic mode checks contracts, not agent quality."""
from langchain_learning.advanced import compare_case, validate_handoff
from langchain_learning.rag import GroundedAnswer
from langchain_learning.retrieval import PolicyIndex
from langchain_learning.runtime import emit, lab_parser, model_settings, preflight, run_lab


def main() -> None:
    parser = lab_parser(__doc__)
    parser.add_argument("--trials", type=int, default=2)
    parser.add_argument("--fail-specialist", action="store_true",
                        help="Corrupt a real specialist handoff to demonstrate a boundary stop")
    args = parser.parse_args()
    if not 1 <= args.trials <= 5:
        raise ValueError("Declare 1..5 trials")
    emit({"preflight": preflight()})
    cases = [("What is the return policy?", "alice"),
             ("How long does shipping take?", "bob"),
             ("What is the policy for teleporting a parcel?", "alice"),
             ("What is the confidential finance reimbursement limit?", "bob")]
    if not args.live:
        rows = []
        for question, user in cases:
            docs = PolicyIndex().search(question, user)
            ids = {doc.metadata["source_id"] for doc in docs}
            validate_handoff(GroundedAnswer(answer="Evidence unavailable", source_ids=[], abstained=True), ids)
            try:
                validate_handoff(GroundedAnswer(answer="A deliberately invalid boundary fixture",
                                                source_ids=["not-retrieved"], abstained=False), ids)
            except ValueError:
                rejected = True
            else:
                raise AssertionError("Out-of-scope handoff accepted")
            rows.append({"question": question, "user_id": user, "evidence_ids": sorted(ids),
                         "invalid_handoff_rejected": rejected})
        emit({"contract_cases": rows, "live_gate": "Unverified: real single/specialist generation, quality, timing and usage."})
        return
    model_settings()  # Fail configuration before starting a paid comparison.
    rows = []
    for trial in range(1, args.trials + 1):
        order = ["single", "specialist"] if trial % 2 else ["specialist", "single"]
        for case_id, (question, user) in enumerate(cases, 1):
            for pattern in order:
                row = {"trial": trial, "case_id": case_id,
                       **compare_case(question, user, pattern=pattern,
                                      fail_specialist=args.fail_specialist and pattern == "specialist")}
                rows.append(row)
                emit(row)
    emit({"trials": args.trials, "runs": len(rows), "failed_runs": sum(r["status"] == "failed" for r in rows),
          "decision": "Not automatic. Apply semantic review rubric; retain specialist only for measured benefit.",
          "pricing": "No cost invented: use reported usage and dated provider pricing; failed calls may still cost."})
    if any(row["status"] == "failed" for row in rows) and not args.fail_specialist:
        raise RuntimeError("Comparison contains failed trials; inspect emitted error categories")


if __name__ == "__main__":
    run_lab(main)
