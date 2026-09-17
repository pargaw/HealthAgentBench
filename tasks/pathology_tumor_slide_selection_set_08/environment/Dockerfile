FROM python:3.12-slim

# Deliberately minimal: no whole-slide-image / pathology tooling (openslide,
# tifffile, pillow, numpy, ...) is preinstalled. The agent has root and
# internet access and is expected to work out how to read the slides itself.
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    wget \
    util-linux \
    jq \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /workspace

# Only the agent-visible workspace is baked into the image. The download URLs
# live in the bind-mounted bootstrap.sh (bootstrap service only), never here.
COPY environment/workspace/ /workspace/

RUN mkdir -p /logs/verifier /logs/artifacts /data/slides

# No ENTRYPOINT/CMD: Harbor keeps main alive; the bootstrap service runs
# bootstrap.sh via an explicit command in docker-compose.yaml.
