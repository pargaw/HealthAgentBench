#!/usr/bin/env python3
"""Strict exam-level exact match: all three answers must be correct."""

import argparse
import json
from pathlib import Path

KEYS = {"abnormal", "acl", "meniscus"}


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"Duplicate JSON key: {key}")
        obj[key] = value
    return obj


def score(payload, expected):
    if not isinstance(payload, dict) or set(payload) != KEYS:
        return {
            "reward": 0.0,
            "correct_answers": 0,
            "error": "Expected exactly abnormal, acl, and meniscus.",
        }
    if any(type(v) is not int or v not in (0, 1) for v in payload.values()):
        return {
            "reward": 0.0,
            "correct_answers": 0,
            "error": "Answers must be integers 0 or 1.",
        }
    correct = sum(payload[k] == expected[k] for k in KEYS)
    return {
        "reward": float(correct == 3),
        "correct_answers": correct,
        "total_questions": 3,
        "error": None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--submission", type=Path, default=Path("/workspace/submission.json")
    )
    parser.add_argument("--gold", type=Path, default=Path("/tests/gold.json"))
    parser.add_argument("--output", type=Path, default=Path("/logs/verifier"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    # Fail closed even if infrastructure/answer-key loading fails.
    (args.output / "reward.txt").write_text("0.0\n")
    expected = json.loads(args.gold.read_text())["answers"]
    if set(expected) != KEYS or any(
        type(v) is not int or v not in (0, 1) for v in expected.values()
    ):
        raise ValueError("Invalid verifier answer key")
    try:
        if args.submission.stat().st_size > 65536:
            raise ValueError("Submission is too large")
        payload = json.loads(
            args.submission.read_text(), object_pairs_hook=unique_object
        )
        metrics = score(payload, expected)
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        metrics = {"reward": 0.0, "correct_answers": 0, "error": str(exc)}
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (args.output / "reward.txt").write_text(f"{metrics['reward']:.1f}\n")
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
