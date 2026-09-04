# Investigation Notebook

This notebook records the reasoning process behind the assignment.

The purpose is to preserve:

- hypotheses;
- experiments;
- observations;
- rejected explanations;
- decisions;
- and changes in reasoning.

---

# Investigation Log

## Day 1 — Project Setup

### Objective

Establish a reproducible baseline using the supplied starter kit.

### Initial Questions

1. Can the supplied tokenizer result be reproduced?
2. What exactly does the existing fertility implementation measure?
3. Which parts of the previous report are direct observations?
4. Which parts are interpretations?

### Status

- [x] Starter kit preserved
- [x] Environment recorded
- [x] Baseline reproduced
- [x] Initial anomalies documented

## Day 1 — Baseline Reproduction

### Objective

Reproduce the supplied fertility analysis before modifying the implementation.

### Experiment A1

#### Hypothesis

The reported baseline result should be reproducible from the supplied implementation and sample corpus.

#### Procedure

- Executed the original `fertility.py` command against the English and Hindi sample corpora.
- Recorded Python and tokenizer versions.
- Verified the printed benchmark output against the original report.

#### Observation

The output matched the previous report to the displayed precision:

- English fertility: 1.27 tok/word
- Hindi fertility: 7.45 tok/word
- tok/char: 0.226 and 1.579 respectively
- Hindi is 5.89x the fertility of English

#### Status

- [x] Baseline reproduction completed
- [x] Result matched the supplied report to the reported precision

### Experiment A2.1 — Whitespace

#### Procedure

Compared the baseline implementation to a whitespace-normalized variant using repeated spaces, tabs, leading/trailing whitespace, and blank lines.

#### Observation

For the supplied corpus, whitespace normalization changes fertility by approximately 0.0036 for English and 0.13 for Hindi, which is small relative to the baseline but measurable.

#### Status

- [x] Whitespace sensitivity measured

### Experiment A2.2 — Unicode normalization

#### Procedure

Compared NFC and NFD-normalized variants of the same corpus.

#### Observation

No measurable change was observed for the supplied sample data because the corpus is already normalized and canonically consistent.

#### Status

- [x] Unicode normalization sensitivity measured

### Experiment A2.3 — Case

#### Procedure

Compared original, lowercase, and uppercase variants.

#### Observation

The measured fertility was unchanged for the supplied corpus after lowercasing; the default implementation lowercases each line before counting.

#### Status

- [x] Case sensitivity measured

### Experiment A2.4 — Aggregation

#### Procedure

Compared the implementation's mean-of-lines metric with a corpus-level ratio.

#### Observation

The difference was small but non-zero for both languages:

- English: 1.265 vs 1.253
- Hindi: 7.448 vs 7.403

This reflects line-length imbalance rather than a tokenizer bug.

#### Status

- [x] Aggregation methodology measured

### Interpretation

The supplied report is reproducible for the starter-kit corpus and implementation. The numbers are not fabricated; they are produced by a specific metric definition. The effect of whitespace, normalization, and case is small for the current sample, but the aggregation method is distinct from a corpus-level ratio and should be reported explicitly.

### Rejected hypotheses

- The report does not contain a hidden code change beyond the supplied script.
- The major numerical claims are supported for the supplied sample data.
- The raw corpus does not show a meaningful Unicode normalization discrepancy.

### Open questions

- Whether the supplied metric is appropriate for broad multilingual comparison remains unresolved.
- Whether the same conclusions generalize beyond the sample corpus remains untested.

---

# Part A

## Hypothesis Log

| ID | Hypothesis | Test | Result | Status |
|---|---|---|---|---|
| A-H1 | TBD | TBD | TBD | Open |

---

# Part B

## Hypothesis Log

| ID | Hypothesis | Test | Result | Status |
|---|---|---|---|---|
| B-H1 | TBD | TBD | TBD | Open |

---

# Part C

## Decision Log

| Decision | Evidence | Confidence |
|---|---|---|
| TBD | TBD | TBD |

---

# Rejected Hypotheses

This section records explanations that were investigated but
not supported by evidence.

---

# Open Questions

Questions that remain unresolved will be recorded here rather
than silently converted into assumptions.
