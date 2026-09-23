# Clinical Compositional Question Answering

You are working inside a task environment that contains a MIMIC-IV DuckDB
database and 60 numerical clinical questions about ICU patients. Your job is
to answer each question and write all answers to `/workspace/submission.json`.

## Question types

The 60 questions span five types, recorded in each item's `question_type` field:

- `direct`: a score, or one named component of a score, as defined by the reference implementation.
- `aggregation`: an aggregate over the ICU stay, such as a maximum stage or score or an average dose.
- `temporal`: a value anchored to a time window or time point (first 24 hours, ICU admission, time of suspected infection). "How many hours after ICU admission" questions expect a signed number of hours; when the reference implementation finds no qualifying event, the expected answer is 0.
- `derived`: a sum of named sub-scores, or a signed difference between two quantities (first minus second, not absolute).
- `comparative`: by how many units a value exceeds a stated threshold. When it does not exceed the threshold, the expected answer is 0, never negative.

## What you have

- `/workspace/data/mimic4.db` — DuckDB database with two schemas:
  `mimiciv_hosp` and `mimiciv_icu`. There are no pre-computed derived
  tables — you must build any aggregates you need from the raw hospital
  and ICU tables. Always use fully-qualified table names (e.g.
  `mimiciv_icu.icustays`). IDs follow the chain `subject_id` (patient) →
  `hadm_id` (admission) → `stay_id` (ICU stay).
- `/workspace/questions.json` — a JSON array of 60 questions. Each item has
  a unique `question_id`, the natural-language `question`, and the patient
  identifiers (`subject_id`, `hadm_id`, `stay_id`) for which the question is
  to be answered.
- `/workspace/train.json` — 1200 labeled examples, twenty for each question
  variant. Use these examples to validate your computations.

- Pre-installed Python data tools: `duckdb`, `pandas`, `numpy`, `pyarrow`.
  Use them however you like. Bash and standard CLI tools are also available.
- `/workspace/submission.json` — pre-populated with one row per question,
  with `answer` set to `null`. Fill in the `answer` field for each row.

## How to answer

For each question:

1. Read its `question` text and the patient identifiers.
2. Compute the answer by querying the MIMIC-IV DuckDB. You can use SQL
   (via `duckdb`), `pandas`, or any combination. The questions ask for
   numerical clinical values such as severity scores, organ-failure stage
   numbers, or counts.
3. Validate your calculations against the labeled examples in `train.json`.
   The answers use a MIMIC-IV-specific implementation; item IDs, time windows,
   unit conventions, and edge cases may differ from textbook definitions.
   Refine your formulas using these examples before answering the test questions.

4. Write the numerical answer into the corresponding row of
   `/workspace/submission.json`.

## Submission format

`/workspace/submission.json` is a JSON list. Each row contains exactly two
fields:

    {"question_id": "<string>", "answer": <number or null>}

- The verifier expects a number. Strings, booleans, and `null` all score as
  wrong.
- If you genuinely cannot compute an answer, leave it `null`. It will score
  as wrong but the verifier will still run.
- Do not add or remove rows. Do not rename `question_id` values.
- Do not write anything outside `/workspace/submission.json`.

## Scoring

Each answer is scored independently. An answer is correct if

    |answer - gt_answer| <= max(0.5, 1e-3 * |gt_answer|)

Overall reward is binary: 1 (pass) only if all 60 questions are answered
correctly in a valid submission; otherwise 0 (fail). Per-question accuracy
and per-concept accuracy are reported as diagnostic metrics only.

## Rules

- Do not use the internet to look up answers directly.
- Do not modify files outside `/workspace/submission.json`.

## Resources

The container is limited to the following, and Docker enforces these limits regardless of what system tools report:

- 2 CPUs
- 4 GiB of memory
- 8 GiB of disk
- no GPU

Tools such as `nproc`, `free -h`, `/proc/cpuinfo`, `/proc/meminfo` and `os.cpu_count()` report the host machine (over 100 CPUs and terabytes of RAM), not this container's limits.
