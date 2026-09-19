FROM python:3.12-slim

# Agent image. Only the agent-visible workspace is baked in; the bootstrap
# material (bootstrap.sh, stage_mri.py, task_manifest.json) is bind-mounted
# into the separate bootstrap service and never reaches this image.
RUN apt-get update && apt-get install -y --no-install-recommends bash ca-certificates jq tmux asciinema && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir numpy==2.4.2 pillow==12.1.1 matplotlib==3.10.8
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /workspace
COPY environment/workspace/ /workspace/
RUN mkdir -p /workspace/mri /logs/verifier /logs/artifacts

# No ENTRYPOINT/CMD: Harbor keeps main alive; the bootstrap service runs
# bootstrap.sh via an explicit command in docker-compose.yaml.
