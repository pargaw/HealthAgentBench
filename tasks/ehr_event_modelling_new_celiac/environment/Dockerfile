FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash ca-certificates curl util-linux unzip \
    && rm -rf /var/lib/apt/lists/*

# numpy + pandas + a pinned scikit-learn are pre-installed: the verifier
# (tests/evaluate.py) computes AUROC/AUPRC/Brier with sklearn.metrics, and
# the pin keeps scoring identical across trials and machines. The agent
# installs any other ML libraries it wants at runtime. ``redivis`` lives in
# the separate bootstrap image (Dockerfile.bootstrap) because it drags in
# polars/pyarrow/geopandas and an unpinned scikit-learn.
RUN pip install --no-cache-dir \
    numpy==2.1.3 \
    pandas==2.2.3 \
    scikit-learn==1.5.2

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /workspace
# Nothing task-specific or source-revealing is baked into this image.
# The bootstrap entrypoint (bootstrap.sh) and the slicer (stage_data.py) are
# bind-mounted into the bootstrap service ONLY (see docker-compose.yaml); the
# scorer (evaluate.py) ships in tests/ (mounted only at verify time). So the
# agent's main container cannot read any of them.
RUN mkdir -p /workspace/submission /workspace/data

# No ENTRYPOINT/CMD: Harbor's docker-compose-build.yaml overrides main's
# command to ``sleep infinity``. The bootstrap service uses an explicit
# ``command:`` in docker-compose.yaml to run /bootstrap.sh and exit cleanly.
