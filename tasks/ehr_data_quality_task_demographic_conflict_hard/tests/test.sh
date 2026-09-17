#!/bin/bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p /logs/verifier /logs/artifacts
# The task image ships no third-party packages (the agent installs its own);
# the verifier needs pandas, so install it here, at scoring time only.
python -m pip install --quiet --disable-pip-version-check "pandas==3.0.1"
python verify.py
