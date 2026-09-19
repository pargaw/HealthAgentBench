# mri_qa_case_01

One knee MRI exam, three binary questions, exact-match reward. See
[the family documentation](../../assets/mri_qa/README.md) for provenance,
label limitations, reproducibility, and validation.

## Run

```bash
uv run harbor run -p tasks/mri_qa_case_01 -a <agent> -m <vision-capable-model>
# whole category:
uv run harbor run -p tasks --include-task-name 'mri_qa_case_*' -a <agent> -m <model>
```

The `bootstrap` compose service runs first. On a cache miss it uses
`REDIVIS_API_TOKEN` from the repo-root `.env` to download only this exam's three
series and the public validation label tables into
`assets/mri_qa/assets/raw_cache/`, verifies every source checksum against
`environment/task_manifest.json`, derives the gold answers for this exam at run
time, writes them to `tests/gold.json` (gitignored), and stages every slice into a
read-only volume for the agent. The token, the manifest, the raw cache, and the
gold never enter the agent image or its container.
