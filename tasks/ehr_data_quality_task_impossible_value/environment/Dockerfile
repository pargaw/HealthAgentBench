FROM python:3.12-slim

# Agent image. Deliberately package-free: the agent is expected to install
# whatever tooling it needs (pandas, duckdb, ...) itself. The data-staging
# pipeline runs in a separate image (Dockerfile.bootstrap) that carries the
# pinned scientific stack, so nothing leaks into the agent's environment.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash ca-certificates curl wget util-linux \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /workspace
# Compose's build context is the parent (task root), so the path is
# environment/workspace/ rather than workspace/. Match xray_report_gen.
COPY environment/workspace/ /workspace/
RUN mkdir -p /workspace/data /workspace/submission /logs/verifier

# No ENTRYPOINT / CMD: Harbor's docker-compose-build.yaml overrides main's
# command to ``sleep infinity`` so the container stays alive for the agent
# + verifier. The bootstrap service uses an explicit ``command:`` in
# docker-compose.yaml to run /bootstrap.sh (bind-mounted) and exit.
