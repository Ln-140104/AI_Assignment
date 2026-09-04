# Part A — Multilingual Tokenizer Audit

## Objective

Determine whether the supplied multilingual tokenizer analysis
is reproducible and whether its methodology supports the claims
made in the previous report.

## Questions

1. Can the baseline result be reproduced?
2. Are there implementation issues?
3. Which suspected issues are real?
4. Which suspected issues do not materially affect results?
5. Is the fertility metric appropriate for cross-language comparison?
6. Does tokenizer choice affect the observed language differences?

## Evidence

The supplied starter kit is preserved under:

`data/raw/starter_kit/`

## Experiment IDs

- A1 — Baseline reproduction
- A2.1 — Whitespace sensitivity
- A2.2 — Normalization sensitivity
- A2.3 — Case sensitivity
- A2.4 — Aggregation methodology
- A3.1 — Corpus comparison
- A3.2 — Tokenizer comparison
- A3.3 — Alternative denominator analysis

## Status

Not yet executed.
