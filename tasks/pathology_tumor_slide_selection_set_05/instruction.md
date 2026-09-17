# Tumor Slide Selection

The directory `/data/slides/` contains 8 whole-slide H&E pathology images (`slide_1.svs`, `slide_2.svs`, `slide_3.svs`, `slide_4.svs`, `slide_5.svs`, `slide_6.svs`, `slide_7.svs`, `slide_8.svs`). Any number of them, possibly none, may contain tumor. Identify every slide that contains tumor.

Write your answer to `/workspace/submission.json` as the list of tumor-containing slides (an empty list if none does), for example:

```json
{"tumor_slides": ["slide_N.svs", "slide_M.svs"]}
```

No whole-slide-image or pathology tooling is preinstalled. You have root and internet access inside the container and may install whatever you need to read and inspect the slides.

## Rules

- You have a budget of 2 hours to complete this task.
- Be mindful of your time budget: work efficiently, avoid unnecessary or repetitive analysis, and make sure you finish and write your submission well within the time limit.
- You should not cheat and you should not look up the answer (for example, the slides' source records or labels) from the internet.
- Work autonomously until the submission is complete.
- Do not train models or fine-tune weights.

## Resources

The container is limited to 2 CPUs, 8 GiB of memory, 20 GiB of disk and no GPU. Docker enforces these limits regardless of what tools such as `nproc`, `free -h` or `os.cpu_count()` report.
