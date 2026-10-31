"""Persistent approval commands; explicit drafts are human-authored inputs."""
from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_learning.runtime import emit, lab_parser, preflight, run_lab, state_dir
from langchain_learning.workflow import SupportWorkflow


def check():
    with TemporaryDirectory(prefix="course-approval-") as directory:
        db, actions = Path(directory) / "checkpoints.sqlite", Path(directory) / "actions.sqlite"
        with SupportWorkflow(db, actions) as flow:
            for thread in ("approve", "reject", "edit"):
                result = flow.start("alice", thread, "Return policy?", draft="Human-authored original draft")
                assert result["status"] == "pending" and not result["actions"]
            assert flow.actions("alice") == []
        # Real close/reopen; independent CLI commands additionally prove process restart.
        with SupportWorkflow(db, actions) as flow:
            assert flow.inspect("alice", "approve")["pending_review"]
            assert flow.decide("alice", "reject", "reject")["status"] == "rejected"
            assert flow.decide("alice", "approve", "approve")["status"] == "recorded"
            assert flow.decide("alice", "edit", "edit", edited_draft="Human-reviewed corrected text")["actions"][0]["draft"] == "Human-reviewed corrected text"
            flow.decide("alice", "approve", "approve")
            assert len(flow.actions("alice")) == 2
            for operation in (
                lambda: flow.inspect("bob", "approve"),
                lambda: flow.decide("bob", "approve", "approve"),
                lambda: flow.start("bob", "approve", "Overwrite attempt", draft="attacker"),
            ):
                try:
                    operation()
                except PermissionError:
                    pass
                else:
                    raise AssertionError("Cross-owner operation succeeded")
            assert not flow.actions("bob")
            return {"approved": flow.inspect("alice", "approve"), "rejected": flow.inspect("alice", "reject"), "edited": flow.inspect("alice", "edit"), "cross_owner": "inspection/resumption/restart denied", "limits": "Close/reopen verified by this command; separate CLI invocations are the process-restart gate. Exactly-once concerns only atomic local SQLite records.", "live_gate": "Model drafting unverified without --live and provider consent"}


def main():
    parser = lab_parser(__doc__)
    parser.add_argument("--operation", choices=["start", "inspect", "decide", "actions"])
    parser.add_argument("--user", default="alice", help="Trusted local demo identity, not authentication")
    parser.add_argument("--thread", default="support-1")
    parser.add_argument("--question", default="What is the return policy?")
    parser.add_argument("--draft", help="Explicit human-authored text; not model output")
    parser.add_argument("--decision", choices=["approve", "reject", "edit"])
    parser.add_argument("--edited-draft")
    parser.add_argument("--db", type=Path)
    parser.add_argument("--actions-db", type=Path)
    args = parser.parse_args()
    emit({"preflight": preflight()})
    if args.operation is None and not args.live:
        emit(check())
        return
    if args.live and args.operation not in (None, "start"):
        raise ValueError("--live is only for starting model drafting")
    directory = state_dir()
    with SupportWorkflow(args.db or directory / "support.sqlite", args.actions_db or directory / "actions.sqlite") as flow:
        operation = args.operation or "start"
        if operation == "start":
            emit(flow.start(args.user, args.thread, args.question, draft=args.draft, live=args.live))
        elif operation == "inspect":
            emit(flow.inspect(args.user, args.thread))
        elif operation == "decide":
            emit(flow.decide(args.user, args.thread, args.decision, edited_draft=args.edited_draft))
        else:
            emit(flow.actions(args.user))


if __name__ == "__main__":
    run_lab(main)
