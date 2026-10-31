"""Human-authored fixtures test review identity and unexercised-answer boundaries."""
import unittest

from langchain_learning.evaluation import apply_human_reviews


def report_fixture(answer):
    return {
        "cases": [{"case_id": "a01", "strategy": "lexical", "trial": 1,
                   "generated_answer": answer, "human_review": None,
                   "failure_categories": ["retrieval_miss"]}],
        "summary": {"lexical": {"human_reviewed": 0, "failures": {"retrieval_miss": 1}}},
    }


def review_fixture(*, appropriate=True):
    return {("a01", "lexical", 1): {
        "reviewer": "human-authored boundary fixture",
        "grade": {"groundedness": 2, "correctness": 2, "relevance": 2,
                  "abstention_appropriate": appropriate},
    }}


class HumanReviewTests(unittest.TestCase):
    def test_no_generated_answer_cannot_receive_semantic_grade(self):
        report = report_fixture(None)
        with self.assertRaises(ValueError):
            apply_human_reviews(report, review_fixture())
        self.assertIsNone(report["cases"][0]["human_review"])
        self.assertEqual(report["summary"]["lexical"]["human_reviewed"], 0)

    def test_review_cannot_move_to_another_case(self):
        report = report_fixture({"answer": "Human-authored abstention", "source_ids": [], "abstained": True})
        review = review_fixture()
        review[("a02", "lexical", 1)] = review.pop(("a01", "lexical", 1))
        with self.assertRaises(ValueError):
            apply_human_reviews(report, review)
        self.assertIsNone(report["cases"][0]["human_review"])

    def test_reassessment_changes_semantic_failure_without_hiding_retrieval_miss(self):
        report = report_fixture({"answer": "Human-authored abstention", "source_ids": [], "abstained": True})
        apply_human_reviews(report, review_fixture(appropriate=False))
        self.assertEqual(report["summary"]["lexical"]["failures"],
                         {"retrieval_miss": 1, "human_semantic_rubric_failure": 1})
        apply_human_reviews(report, review_fixture(appropriate=True))
        self.assertEqual(report["summary"]["lexical"]["failures"], {"retrieval_miss": 1})


if __name__ == "__main__":
    unittest.main()
