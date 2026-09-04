# Multilingual Tokenization & Inference Audit

## Overview

This repository contains a reproducible investigation of the
multilingual tokenization and inference-capacity claims provided
in the assignment starter kit.

The investigation is divided into three parts:

- Part A — Multilingual tokenizer audit
- Part B — Inference capacity and throughput reconciliation
- Part C — Product and model recommendation

## Research Principles

The investigation follows four principles:

1. Reproduce before modifying.
2. Separate observed evidence from interpretation.
3. Test competing hypotheses rather than assuming bugs.
4. Ensure every final numerical claim is reproducible.

## Repository Structure

```text
data/       Raw, processed, and external data
partA/      Tokenizer audit
partB/      Inference capacity analysis
partC/      Product/model decision analysis
reports/    Final deliverables
```

## Reproducibility
## Environment

- Python: 3.x
- Tokenization: `tiktoken` GPT-2 encoding and Hugging Face `xlm-roberta-base`
- Corpus: FLORES-101 devtest subset, 1,000 aligned sentences across English, Hindi, Tamil, Telugu, and Kannada
- Text preprocessing: Unicode NFC normalization; no lowercasing or truncation
- Reproducibility: Part A includes corpus metadata, scripts, result CSVs, and verification outputs

## Evidence Policy
Every important claim in the final submission should be classified
as one of:

- OBSERVED — directly measured from an experiment or supplied evidence.
- DERIVED — calculated from observed/supplied values.
- HYPOTHESIS — an explanation being tested.
- ASSUMPTION — an explicit assumption required for an analysis.
- RECOMMENDATION — an engineering decision based on the evidence.
AI-generated claims are not considered evidence unless independently
verified.

## Final Findings

- The starter Hindi fertility result (~5.89x English) is reproducible on the supplied sample, but it does not generalize as a universal language penalty.
- On the controlled FLORES-101 evaluation, GPT-2 shows much larger token expansion for Hindi and the Dravidian languages than XLM-R.
- XLM-R reduces relative expansion substantially: Hindi 1.25x, Tamil 1.35x, Telugu 1.32x, and Kannada 1.35x relative to English.
- Token/word alone is not sufficient for cross-language comparison because segmentation and whitespace conventions differ; the audit therefore reports word, grapheme, and byte-normalized measures.
- The original claim that Hindi's higher fertility directly implies approximately 6x serving cost is not established by the starter experiment.

## Final Recommendation

Use a multilingual tokenizer such as XLM-R rather than routing Indic-language traffic through the GPT-2 tokenizer. The controlled evaluation shows substantially lower relative token expansion for Hindi, Tamil, Telugu, and Kannada under XLM-R.

For production routing and cost estimation, use a tokenizer-specific token-based measure rather than the starter report's Hindi fertility headline. The main caveat is that FLORES-101 is a relatively small, formal parallel-sentence corpus and may not represent production conversational traffic. A production rollout should therefore validate token usage and latency on representative user traffic.
