"""Regression tests for the all-correct benchmark contract."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evaluator import is_correct, score_submission


class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.key = Path(__file__).with_name("answer_key.json")
        self.answers = [
            {"question_id": r["question_id"], "answer": r["gt_answer"]}
            for r in json.loads(self.key.read_text())
        ]
        self.submission = self.root / "submission.json"
        self.n = len(self.answers)

    def score(self, answers):
        self.submission.write_text(json.dumps(answers))
        return score_submission(self.submission, self.key)

    def test_all_correct_passes(self):
        metrics = self.score(self.answers)
        self.assertTrue(metrics["passed"])
        self.assertEqual(metrics["correct"], self.n)
        self.assertTrue(all("expected" not in row and "gt_answer" not in row
                            for row in metrics["per_question"]))

    def test_each_single_wrong_answer_fails(self):
        for index in range(self.n):
            with self.subTest(index=index):
                answers = copy.deepcopy(self.answers)
                answers[index]["answer"] += 100
                metrics = self.score(answers)
                self.assertFalse(metrics["passed"])
                self.assertEqual(metrics["correct"], self.n - 1)
                self.assertAlmostEqual(metrics["pass_rate_overall"], (self.n - 1) / self.n)

    def test_invalid_submission_fails(self):
        for answers in [self.answers[:-1], self.answers + [self.answers[0]], {}, [],
                        self.answers + [{"question_id": [], "answer": 0}]]:
            with self.subTest(answers_type=type(answers)):
                self.assertFalse(self.score(answers)["passed"])

    def test_missing_and_malformed_file_fail(self):
        self.assertFalse(score_submission(self.submission, self.key)["passed"])
        self.submission.write_text("{")
        self.assertFalse(score_submission(self.submission, self.key)["passed"])

    def test_non_numeric_and_non_finite_answers_fail(self):
        for value in [None, True, False, "2", [], {}, float("nan"), float("inf")]:
            with self.subTest(value=value):
                answers = copy.deepcopy(self.answers)
                answers[0]["answer"] = value
                self.assertFalse(self.score(answers)["passed"])

    def test_numerical_tolerance_boundaries(self):
        self.assertTrue(is_correct(2.5, 2))
        self.assertFalse(is_correct(2.5001, 2))
        self.assertTrue(is_correct(10010, 10000))
        self.assertFalse(is_correct(10010.1, 10000))

    def test_cli_writes_binary_reward(self):
        for delta, expected in [(0, 1.0), (100, 0.0)]:
            answers = copy.deepcopy(self.answers)
            answers[0]["answer"] += delta
            self.score(answers)
            subprocess.run([
                sys.executable, str(Path(__file__).with_name("evaluator.py")),
                "--submission", str(self.submission), "--answer-key", str(self.key),
                "--metrics-out", str(self.root / "metrics.json"),
                "--reward-out", str(self.root / "reward.json"),
            ], check=True, capture_output=True)
            self.assertEqual(json.loads((self.root / "reward.json").read_text()),
                             {"reward": expected})


if __name__ == "__main__":
    unittest.main()
