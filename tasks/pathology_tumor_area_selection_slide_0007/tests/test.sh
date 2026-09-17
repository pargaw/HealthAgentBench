#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier /logs/artifacts

# The image ships no slide-reading libraries (the agent must source its own),
# so install the verifier's dependencies here, at verification time.
for attempt in 1 2 3; do
    if python -m pip install --quiet --no-cache-dir \
        requests numpy tifffile imagecodecs; then
        break
    fi
    echo "[verifier] pip install failed (attempt $attempt), retrying..." >&2
    sleep 10
done

python /tests/verify_meta_task.py   --submission /workspace/submission.json   --answer-key /tests/task_answer_key.json   --reward-txt /logs/verifier/reward.txt   --results-json /logs/verifier/meta_results.json   --error-analysis-file /logs/artifacts/error_analysis.json
