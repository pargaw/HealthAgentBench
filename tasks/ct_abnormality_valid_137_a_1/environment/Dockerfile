FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash ca-certificates curl util-linux \
    && rm -rf /var/lib/apt/lists/*

# huggingface_hub is needed only by the bootstrap service (CT-RATE download).
# No CT / imaging libraries are preinstalled: the agent installs what it needs.
RUN pip install --no-cache-dir huggingface_hub==0.27.0

# Don't write .pyc files anywhere -- keeps the bind-mounted /tests dir free of
# root-owned __pycache__ residue that the host can't delete.
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /workspace
# No COPY of environment/workspace/: that directory is intentionally empty
# for ct_abnormality (the bootstrap service populates /workspace/data/
# via a named compose volume at runtime), and Docker BuildKit refuses to
# COPY an empty directory ("failed to compute cache key").
# NOTE: bootstrap.sh and gold_derivation.py are deliberately NOT COPY'd into
# the image. They are bind-mounted into the *bootstrap* service only (see
# docker-compose.yaml), so the agent's ``main`` container can never read them.
# bootstrap.sh names the CT-RATE source + the exact HF report path, and
# gold_derivation.py is the full label-derivation recipe (phrase rules) — both
# would leak provenance/answers to a download-capable agent.
RUN mkdir -p /workspace/submission /workspace/data

# No ENTRYPOINT/CMD: Harbor's docker-compose-build.yaml overrides main's
# command to ``sleep infinity`` so the container stays alive. The bootstrap
# service uses an explicit ``command:`` in docker-compose.yaml to run
# /bootstrap.sh and exit cleanly.
