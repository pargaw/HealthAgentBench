# `ehr_compositional_qa_aggregation`

One of five tasks in HealthAgentBench's **EHR Compositional QA** category, partitioned
by question type. This task holds the **10 `aggregation` questions**: maxima and averages over the ICU stay.
Concepts covered: aki, kdigo_stages, meld, norepinephrine_equivalent_dose, sofa.

**Training:** `train.json` holds 200 labeled examples, twenty per question variant (the complete generator pool for these variants).
The per-variant split is retained from the original benchmark; patients can appear
across variants, so this is not a patient-disjoint evaluation.

**Pass condition:** all **10/10** answers correct in a valid submission.
The numerical tolerance is `max(0.5, 1e-3 * abs(gt_answer))`.
The verifier reports diagnostic accuracy separately from the binary reward.

Data: public MIMIC-IV-demo v2.2, downloaded by a bootstrap service at runtime; no dataset
credentials required. The database contains raw hospital/ICU tables only.

## Run

```bash
uv run harbor run --path tasks/ehr_compositional_qa_aggregation \
  --agent codex --model gpt-6-astra --agent-kwarg reasoning_effort=xhigh \
  --n-attempts 1 --n-concurrent 1
```

Run all five with `uv run harbor run -c jobs/ehr_compositional_qa.yaml`.
See the [category overview](../../research/ehr_compositional_qa/README.md).

## Bootstrap and label isolation

Harbor starts a one-shot `bootstrap` service before `main`. Bootstrap downloads
the public demo on first use, builds a raw-only DuckDB, and stages it into a named
volume. A shared host cache under `assets/ehr_compositional_qa/` avoids repeated
downloads; only bootstrap can access that cache. Main mounts the raw-data volume
read-only and cannot access bootstrap files or any test labels.

Grading uses Harbor's `environment_mode = "separate"`: a dedicated verifier image
built from `tests/` contains the answer key. Harbor transfers the submission into
that container after the agent finishes. It never uploads `/tests` or the answer
key into main. The verifier has no internet access and no shared task-data volume.
Verifier metrics omit expected answer values so shared logs do not disclose gold
labels.
