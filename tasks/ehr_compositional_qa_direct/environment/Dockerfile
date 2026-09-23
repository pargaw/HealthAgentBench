FROM python:3.12-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir duckdb==1.5.3 pandas==2.2.2 numpy==1.26.4 pyarrow==15.0.2
WORKDIR /workspace
# Only public inputs. Neither bootstrap code nor verifier labels enter this image.
COPY workspace/ /workspace/
RUN mkdir -p /workspace/data
CMD ["sleep", "infinity"]
