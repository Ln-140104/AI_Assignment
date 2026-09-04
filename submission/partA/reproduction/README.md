# Baseline Reproduction

## Purpose

Reproduce the tokenizer/fertility analysis supplied in the assignment starter kit before introducing methodological changes.

## Experiments

- A1 — Baseline reproduction
- A2.1 — Whitespace sensitivity
- A2.2 — Normalization sensitivity
- A2.3 — Case sensitivity
- A2.4 — Aggregation methodology

## Principle

The supplied implementation is treated as the baseline. Corrections are evaluated separately rather than silently applied to the baseline.

## Reproduction

Command recorded for baseline reproduction:

```bash
python "<path to fertility.py>" --corpus eng=<eng_sample.txt> --corpus hin=<hin_sample.txt> --tokenizer gpt2
```

## Results

Results are stored under:

`results/`
