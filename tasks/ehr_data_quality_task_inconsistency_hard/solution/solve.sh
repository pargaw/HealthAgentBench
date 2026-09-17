#!/bin/bash
# Reference (oracle) solution: a label-blind, rule-based data-quality audit.
# The task image ships no third-party packages, so install what the audit needs.
set -euo pipefail
python -m pip install --quiet --disable-pip-version-check pandas numpy
python "$(dirname "$0")/oracle.py" \
    --data-dir /workspace/data \
    --output /workspace/submission/flagged_rows.csv \
    --families inconsistency
