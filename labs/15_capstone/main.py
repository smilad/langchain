"""Integrate evidence retrieval, durable human review, ownership and local actions."""

from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_learning.retrieval import PolicyIndex
from langchain_learning.runtime import emit, lab_parser, preflight, run_lab, state_dir
from langchain_learning.workflow import SupportWorkflow


def local_demo() -> dict:
    """Exercise real retrieval and persistent control with an explicit human draft."""
    index = PolicyIndex()
    question = "What is the returns deadline for an unused item?"
    evidence = index.search(question, "alice")
    with TemporaryDirectory(prefix="langchain-capstone-") as directory:
        db = Path(directory) / "checkpoints.sqlite"
        sink = Path(directory) / "actions.sqlite"
        with SupportWorkflow(db, sink) as workflow:
            pending = workflow.start("alice", "capstone-approved", question,
                                     draft="Human-authored exercise draft: verify the return conditions before replying.")
            assert pending["status"] == "pending", pending
            assert not workflow.actions("alice"), "A draft must not cause an action before review"
        # New connections reopen the persisted checkpoint; the README also shows process restart.
        with SupportWorkflow(db, sink) as workflow:
            recovered = workflow.inspect("alice", "capstone-approved")
            assert recovered["status"] == "pending", recovered
            edited = workflow.decide("alice", "capstone-approved", "edit",
                                      edited_draft="Human-approved exercise draft: include the verified source and applicable conditions.")
            assert edited["status"] == "recorded", edited
            repeated = workflow.decide("alice", "capstone-approved", "edit",
                                       edited_draft="Human-approved exercise draft: include the verified source and applicable conditions.")
            assert len(workflow.actions("alice")) == 1, "Repeated approval must not duplicate the local record"
            workflow.start("bob", "capstone-rejected", question,
                           draft="Human-authored draft that the reviewer will reject.")
            rejected = workflow.decide("bob", "capstone-rejected", "reject")
            assert rejected["status"] == "rejected", rejected
            assert not workflow.actions("bob"), "Rejected draft must have no recorded action"
            try:
                workflow.inspect("bob", "capstone-approved")
            except PermissionError:
                cross_user_denied = True
            else:
                raise AssertionError("Another user inspected Alice's thread")
            actions = workflow.actions("alice")
    return {
        "mode": "local integration with human-authored draft, not generated-agent proof",
        "retrieved_evidence": [{"source_id": doc.metadata["source_id"], "text": doc.page_content} for doc in evidence],
        "persisted_pending_recovered": recovered["status"],
        "edited_action": actions,
        "retry_status": repeated["status"],
        "rejection_status": rejected["status"],
        "cross_user_denied": cross_user_denied,
        "model_request_sent": False,
        "remaining_live_gates": ["model-grounded draft quality", "held-out generated answers", "prompt-injection response behavior"],
    }


def main() -> None:
    parser = lab_parser(__doc__)
    parser.add_argument("--action", choices=("demo", "start", "inspect", "approve", "reject", "edit"), default="demo")
    parser.add_argument("--user", choices=("alice", "bob", "finance"), default="alice")
    parser.add_argument("--thread", default="capstone-alice")
    parser.add_argument("--question", default="What is the returns deadline for an unused item?")
    parser.add_argument("--draft", help="Explicit human-authored draft; never claimed as model output")
    parser.add_argument("--edited-draft")
    args = parser.parse_args()
    if args.action == "demo" and not args.live:
        emit({"environment": preflight(), "integration": local_demo()})
        return
    directory = state_dir() / "capstone"
    directory.mkdir(parents=True, exist_ok=True)
    with SupportWorkflow(directory / "checkpoints.sqlite", directory / "actions.sqlite") as workflow:
        if args.action in ("start", "demo"):
            if not args.live and args.draft is None:
                raise ValueError("Provide --draft for an explicit human-authored run, or --live for real model drafting")
            result = workflow.start(args.user, args.thread, args.question, draft=args.draft, live=args.live)
        elif args.action == "inspect":
            result = workflow.inspect(args.user, args.thread)
        else:
            result = workflow.decide(args.user, args.thread, args.action, edited_draft=args.edited_draft)
    emit(result)


if __name__ == "__main__":
    run_lab(main)
