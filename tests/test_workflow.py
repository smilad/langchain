"""Real SQLite/LangGraph regressions: persistence, identity, approval, replay."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from langchain_learning.workflow import SupportWorkflow


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.db, self.sink = root / "state.sqlite", root / "actions.sqlite"

    def flow(self):
        return SupportWorkflow(self.db, self.sink)

    def test_live_configuration_is_checked_before_thread_registration(self):
        configuration = {"OPENAI_API_KEY": "", "COURSE_MODEL": "", "COURSE_ALLOW_LIVE": "0"}
        with patch.dict(os.environ, configuration), self.flow() as flow:
            with self.assertRaises(ValueError):
                flow.start("alice", "unconsented", "zzznomatchingpolicy", live=True)
            with self.assertRaises(ValueError):
                flow.inspect("alice", "unconsented")
            self.assertEqual(flow.actions("alice"), [])

    def test_reject_has_no_effect_across_reopen(self):
        with self.flow() as flow:
            self.assertEqual(flow.start("alice", "reject", "question", draft="human draft")["status"], "pending")
            self.assertEqual(flow.actions("alice"), [])
        with self.flow() as flow:
            self.assertEqual(flow.decide("alice", "reject", "reject")["status"], "rejected")
            flow.decide("alice", "reject", "reject")
            self.assertEqual(flow.actions("alice"), [])

    def test_edit_and_immutable_decision(self):
        with self.flow() as flow:
            flow.start("alice", "edit", "question", draft="original")
            with self.assertRaises(ValueError):
                flow.decide("alice", "edit", "edit", edited_draft=" ")
            self.assertEqual(flow.inspect("alice", "edit")["status"], "pending")
            result = flow.decide("alice", "edit", "edit", edited_draft="corrected human text")
            self.assertEqual(result["actions"][0]["draft"], "corrected human text")
        with self.flow() as flow:
            flow.decide("alice", "edit", "edit", edited_draft="corrected human text")
            with self.assertRaises(ValueError):
                flow.decide("alice", "edit", "approve")
            self.assertEqual(len(flow.actions("alice")), 1)

    def test_ownership_cannot_change_on_restart(self):
        with self.flow() as flow:
            flow.start("alice", "private", "original", draft="private draft")
        with self.flow() as flow:
            for operation in (
                lambda: flow.inspect("bob", "private"),
                lambda: flow.decide("bob", "private", "approve"),
                lambda: flow.start("bob", "private", "overwrite", draft="attack"),
            ):
                with self.assertRaises(PermissionError):
                    operation()
            result = flow.start("alice", "private", "overwrite", draft="replacement")
            self.assertEqual(result["state"]["question"], "original")
            self.assertEqual(flow.actions("bob"), [])
            flow.decide("alice", "private", "approve")
            self.assertEqual(flow.actions("bob"), [])

    def test_process_restart_restores_interrupt(self):
        script = """
import json, sys
from pathlib import Path
from langchain_learning.workflow import SupportWorkflow
with SupportWorkflow(Path(sys.argv[1]), Path(sys.argv[2])) as flow:
    print(json.dumps(flow.start('alice', 'process', 'question', draft='human process draft')))
"""
        process = subprocess.run([sys.executable, "-c", script, str(self.db), str(self.sink)], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(process.stdout)["status"], "pending")
        with self.flow() as flow:
            self.assertEqual(flow.inspect("alice", "process")["pending_review"][0]["draft"], "human process draft")
            flow.decide("alice", "process", "approve")
        with self.flow() as flow:
            self.assertEqual(len(flow.actions("alice")), 1)

    def test_replaying_record_node_is_idempotent(self):
        with self.flow() as flow:
            flow.start("alice", "replay", "question", draft="approved draft")
            flow.decide("alice", "replay", "approve")
            # Trusted history replay reexecutes the actual graph node, not a mocked sink.
            before_record = next(snapshot for snapshot in flow._graph.get_state_history(flow._config("replay")) if snapshot.next == ("record",))
            flow._graph.invoke(None, before_record.config)
            self.assertEqual(len(flow.actions("alice")), 1)
            self.assertEqual(flow.actions("alice")[0]["draft"], "approved draft")
        with self.flow() as flow:
            flow.decide("alice", "replay", "approve")
            self.assertEqual(len(flow.actions("alice")), 1)

    def test_checkpoint_cannot_be_rebound_to_empty_sink(self):
        with self.flow() as flow:
            flow.start("alice", "bound", "question", draft="human draft")
        with self.assertRaises(ValueError):
            with SupportWorkflow(self.db, self.sink.with_name("different.sqlite")):
                pass


if __name__ == "__main__":
    unittest.main()
