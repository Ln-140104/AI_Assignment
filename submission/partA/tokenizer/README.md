# Part A Tokenizer

This directory stores tokenizer-specific comparisons, experiment
outputs, and result summaries.

The focus is on measuring whether tokenization choices materially affect
cross-language comparisons rather than assuming that any single model is
appropriate for all languages.

## Assignment Requirements

For Part A3, the evaluation must be controlled and evidence-first:

1. Use a parallel multilingual corpus with aligned sentence IDs across languages,
   not a convenience sample from unrelated corpora.
2. Compare at least two tokenizers on the same sentences: GPT-2 and a multilingual
   tokenizer such as XLM-RoBERTa-base.
3. Keep the evaluation corpus fixed across tokenizers so any observed gap reflects
   language/tokenizer behavior rather than a different text sample.
4. Measure multiple denominators on the same sentences: tokens/word, tokens/grapheme,
   tokens/byte, and tokens/sentence. Unicode code points are retained separately for
   auditability; graphemes are counted as Unicode extended grapheme clusters using
   the `regex` library's `\X` pattern.
5. Preserve the original baseline as reference evidence while testing the stronger
   hypothesis that the Hindi penalty generalizes beyond the supplied sample.
6. Record environment details and experiment metadata in the repo so the final result
   is reproducible.

## Required artifacts

The following outputs are expected under this directory:

- results/environment.txt
- data/corpus_metadata.json
- data/corpus_validation.txt
- results/tokenizer_comparison.csv
- results/master_results.csv
- results/sentence_level_measurements.csv
- results/relative_expansion.csv
- results/language_rankings.csv
- results/results_summary.md
- results/claim_validation.csv
- figures/figure1_mean_tokens_per_sentence.png
- figures/figure2_relative_expansion.png
- figures/figure3_expansion_distributions.png
- figures/figure4_word_vs_sentence.png

## Protocol

1. Download FLORES-101 version 1.0.0 from its documented public release URL.
2. Prepare aligned English, Hindi, Tamil, Telugu, and Kannada sentence files with shared IDs.
3. Validate the five-language corpus alignment before running tokenization.
4. Run the tokenizer comparison across both GPT-2 and a multilingual tokenizer.
5. Summarize all language results with relative expansion and a mention of what the
   evidence does and does not establish.

The initial `en-hi` OPUS-100 run is retained only as an incomplete preliminary result;
it is not the final Part A3 corpus.

## Evidence policy

Report the results as observed measurements, derived ratios, and explicit interpretation.
The goal is to separate a robust language effect from a tokenizer-only artifact.
