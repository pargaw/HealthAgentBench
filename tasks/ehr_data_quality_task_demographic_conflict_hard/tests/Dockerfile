FROM python:3.12-slim
# Used only by Harbor's separate verifier environment (task.toml [verifier]).
# It holds the answer key; the agent's main container never receives /tests.
RUN pip install --no-cache-dir pandas==3.0.1 numpy==2.4.2
WORKDIR /workspace
COPY harbor_evaluator.py verify.py labels.csv test.sh /tests/
RUN mkdir -p /logs/verifier && chmod +x /tests/test.sh
CMD ["sleep", "infinity"]
