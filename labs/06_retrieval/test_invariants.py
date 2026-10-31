"""Real corpus/security regressions; no mocks, model output or text-wiring assertions."""
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from langchain_learning.rag import GroundedAnswer, validate_citations
from langchain_learning.retrieval import PolicyIndex
from langchain_learning.runtime import DATA


class RetrievalBoundaryTests(unittest.TestCase):
    def test_access_is_checked_before_ranking(self):
        index = PolicyIndex()
        for user in ("alice", "bob"):
            docs = index.search("finance reserve ceiling code", user, k=10)
            self.assertTrue(all(d.metadata["current"] and d.metadata["audience"] == "public" for d in docs))
            self.assertNotIn("FINANCE", {d.metadata["source_id"] for d in docs})
        privileged = index.search("finance reserve ceiling code", "finance", k=10)
        self.assertIn("FINANCE", {d.metadata["source_id"] for d in privileged})
        for unknown in ("", "unknown", "ALICE"):
            with self.assertRaises(PermissionError):
                index.search("returns", unknown)

    def test_edit_and_delete_replace_active_index(self):
        with TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for source in (DATA / "policies").glob("*.json"):
                shutil.copyfile(source, directory / source.name)
            index = PolicyIndex(directory=directory)
            original = index.fingerprint
            source = directory / "return-v2.json"
            record = json.loads(source.read_text())
            record["text"] = "Returns are accepted within 37 calendar days of delivery."
            source.write_text(json.dumps(record))
            documents = index.search("returns", "alice", k=10)
            current = [d for d in documents if d.metadata["source_id"] == "RETURN"]
            self.assertEqual(len(current), 1)
            self.assertIn("37 calendar", current[0].page_content)
            self.assertNotEqual(index.fingerprint, original)
            self.assertEqual(current[0].metadata["version"], 2)
            source.unlink()
            self.assertNotIn("RETURN", {d.metadata["source_id"] for d in index.search("returns", "alice", k=10)})

    def test_duplicate_active_source_is_rejected(self):
        with TemporaryDirectory() as temporary:
            directory = Path(temporary)
            record = json.loads((DATA / "policies" / "return-v2.json").read_text())
            (directory / "one.json").write_text(json.dumps(record))
            record["version"] = 3
            (directory / "two.json").write_text(json.dumps(record))
            with self.assertRaises(ValueError):
                PolicyIndex(directory=directory)

    def test_citations_cannot_reference_missing_or_untrusted_sources(self):
        evidence = PolicyIndex().search("returns malicious override", "alice", k=10)
        for source in ("FINANCE", "MALICIOUS", "NONEXISTENT"):
            proposed = GroundedAnswer(answer="Human-authored boundary test", source_ids=[source], abstained=False)
            with self.assertRaises(ValueError):
                validate_citations(proposed, evidence)
        with self.assertRaises(ValueError):
            GroundedAnswer(answer="Abstain", source_ids=["RETURN"], abstained=True)


if __name__ == "__main__":
    unittest.main()
