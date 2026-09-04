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

## A3 Validation — Multilingual Coverage

### Initial problem

The first controlled run reported only English and Hindi from OPUS-100 `en-hi`.
It did not satisfy the required English, Hindi, Tamil, Telugu, and Kannada coverage.

### Investigation

The official FLORES-200 Hub files were inaccessible without authentication. A public,
documented FLORES-101 release archive was therefore used instead of fabricating access
or joining unrelated bilingual corpora. Its `devtest` split contains shared IDs across
the five required languages.

### Resolution

The pipeline now downloads the pinned FLORES-101 version 1.0.0 archive, verifies its
SHA256, NFC-normalizes the selected text, validates alignment, and evaluates GPT-2 and
XLM-RoBERTa-base. It writes sentence-level observations and independent aggregate checks.

### Final corpus

FLORES-101 `devtest`, source archive SHA256
`49fa80207b09fcc0eca8253ed13303b3a0ae0f16081af862601c73ac76f2cba6`, languages
`eng`, `hin`, `tam`, `tel`, and `kan`.

### Final sample

1,000 contiguous IDs selected from 1,012 available. All five languages are present for
every selected ID; validation found no duplicates, empty entries, or unexpected
whitespace after documented normalization.

### Results

GPT-2 mean tokens/sentence: English 26.744, Hindi 198.124, Tamil 415.467, Telugu
346.939, Kannada 363.247. XLM-RoBERTa mean tokens/sentence: English 30.306, Hindi
37.806, Tamil 40.902, Telugu 39.949, Kannada 41.017. Full distributions and denominators
are in `partA/tokenizer/results/master_results.csv`.

### Interpretation

The Hindi result is tokenizer-dependent: GPT-2 gives 7.408x sentence expansion versus
English, while XLM-R gives 1.247x. Tamil, Telugu, and Kannada show the same direction,
but not the same magnitude. The original 5.89x sample claim is therefore partially
supported as a sample observation, not as a general constant.

### Rejected hypotheses

- Script complexity alone explains the observed penalty: not established.
- Tokenization inefficiency is language-invariant: not supported.
- The penalty is an inherent property of the language: unresolved by token counts alone.

### Open questions

The experiment does not establish serving cost, model quality, causality, or production
throughput. Those questions remain outside this Step 3 stopping point.

## Hypothesis Log

| ID | Hypothesis | Test | Result | Status |
|---|---|---|---|---|
| A-H1 | TBD | TBD | TBD | Open |

---

# Part B

## Capacity Reconciliation

### B1 - Hypothesis

The model specification's KV dimensions imply a finite full-context concurrency boundary that should align directionally with the benchmark's utilization and preemption transition.

### Experiment/calculation

Ran `python submission/partB/scripts/reconcile_capacity.py` using `model_spec.md` and `bench_log.csv`. Derived `114,688` KV bytes/token, `448 MiB` per 4,096-token sequence, `12.080` decimal GB KV budget, and `25` complete theoretical sequences.

### Result

Long batch 24 logged `0.93` KV utilization and `0` preemptions; batch 32 logged `0.97` and `7`; batch 48 logged `0.97` and `23`.

### Interpretation

The log is directionally consistent with the simplified capacity calculation, while exact equality is not expected because allocator and runtime details are omitted.

### Revision

The practical recommendation is to cap long-context scheduling at batch 24, subject to production validation.

## B2/B3 - Long-Context Throughput

### Hypothesis

The long-prompt throughput increase stops when the scheduler enters a KV-constrained preemption regime, and the report may be treating total processed-token throughput as generated-token goodput.

### Experiment/calculation

Compared long rows at batches 4, 8, 16, 24, 32, and 48. Recomputed batch-24 goodput as both `24 * 512 / 61.16 = 200.916` and `1607.4 * 512 / 4096 = 200.925` generated tokens/s.

### Result

Reported throughput rises to `1607.4` at batch 24, then falls to `1384.0` and `1298.5`; preemptions rise from `0` to `7` and `23`, while TTFT and p95 latency increase. Batch 48 generated goodput is `162.314` tokens/s, not approximately `3200`.

### Interpretation

The report appears to have read `reported_tok_s`, which includes prompt/prefill plus generation, as generated-token throughput.

### Revision

The corrected conclusion distinguishes total processed-token throughput from generated-token goodput and does not recommend packing longer prompts solely to improve throughput.

## B4 - Production Counter

### Hypothesis

Preemption rate is the most direct operational counter for the inferred scheduler/KV saturation mechanism.

### Experiment/calculation

Derived preemption rates from `preempted_seqs / num_requests`: batch 24 `0%`, batch 32 `21.875%`, batch 48 `47.917%`.

### Result

The supplied benchmark provides the expected direction but no production observation.

### Interpretation

Production preemption rate should be monitored alongside KV utilization and latency; degradation with zero preemption and substantial KV headroom would falsify this mechanism.

### Revision

The counter is a proposed validation metric, not an observed production value.

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
