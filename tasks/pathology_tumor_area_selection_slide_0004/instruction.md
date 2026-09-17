# Tumor Area Selection

You are working inside a pathology task environment that contains:

- the current whole-slide H&E image at `/data/slide/current/slide.tif` (a multi-resolution pyramidal TIFF), with grid parameters in `/data/slide/current/manifest.json`
- a public task row in `/workspace/benchmark_tasks.json`
- an editable single-row submission in `/workspace/submission.json`

No whole-slide-image or pathology tooling is preinstalled. You have root and internet access inside the container and may install whatever libraries you need to read and inspect the slide.

## Analysis grid

The benchmark analysis grid uses 256x256 tiles at downsample 16, so each grid tile spans 4096x4096 full-resolution (level-0) pixels (`4096 = 256*16`). Grid tile `(x, y)` covers the level-0 region with horizontal extent `x*4096` to `(x+1)*4096` (x = column) and vertical extent `y*4096` to `(y+1)*4096` (y = row). The grid has `ceil(slide_width/4096)` columns (indexed by x) and `ceil(slide_height/4096)` rows (indexed by y), where `slide_width` and `slide_height` are the level-0 dimensions. Report tumor tiles using these integer `(x, y)` grid coordinates.

## What counts as a tumor tile

A tile counts as tumor when tumor covers at least 20% of its valid in-slide area (`tumor_threshold` = 0.2 in `benchmark_tasks.json`).

## Your Task

Find the fixed-grid tiles that contain metastatic carcinoma. Localize tumor from the provided H&E images. Identify all and only the tumor tiles on the analysis grid and record them in `/workspace/submission.json`:

- set `contains_tumor` to `true` if the slide contains any tumor tile, otherwise `false`
- populate `predicted_tumor_tiles` with dictionaries of the form `{ "x": <int>, "y": <int> }`, one per tumor tile (leave it empty if you believe the slide has no tumor)
- include every tile you believe is a tumor tile and do not include tiles you believe are not
- do not modify `task_id`

Your submission is scored by tile-level F1 between `predicted_tumor_tiles` and the gold tumor tiles derived from expert annotations. The task passes when F1 is at least 0.9, so both missed tumor tiles and spurious tiles count against you; selecting every tissue tile will not pass.

## Rules

- You have a budget of 1.5 hours to complete this task.
- Be mindful of your time budget: work efficiently, avoid unnecessary or repetitive analysis, and make sure you finish and write your submission well within the time limit.
- You should not cheat and you should not directly look up the end solutions (for example, the slide's published annotations or masks) from the internet.
- Work autonomously until the submission is complete.
- Do not train models or fine-tune weights.
- Update `submission.json` with a JSON-aware tool such as Python.

## Resources

The container is limited to the following, and Docker enforces these limits regardless of what system tools report:

- 2 CPUs
- 8 GiB of memory
- 20 GiB of disk
- no GPU

Tools such as `nproc`, `free -h`, `/proc/cpuinfo`, `/proc/meminfo` and `os.cpu_count()` report the host machine (over 100 CPUs and terabytes of RAM), not this container's limits.