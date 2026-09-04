# Step 3A Defense Facts

## Corpus

- Source: FLORES-101 release archive: https://dl.fbaipublicfiles.com/flores101/dataset/flores101_dataset.tar.gz
- Version: 1.0.0
- Split: `devtest`
- Archive SHA256: `49fa80207b09fcc0eca8253ed13303b3a0ae0f16081af862601c73ac76f2cba6`
- Languages and IDs: English `eng`, Hindi `hin`, Tamil `tam`, Telugu `tel`, Kannada `kan`
- Available IDs: 1,012
- Selected/evaluated aligned IDs: 1,000 (`1` through `1000`)
- Parallel construction: one FLORES sentence ID is used across all five language files; no pairwise stitching or generated sentences.

## Tokenizers

- GPT-2: `tiktoken` encoding `gpt2`
- Multilingual tokenizer: Hugging Face `xlm-roberta-base` via `transformers.AutoTokenizer`
- Every sentence is independently encoded.
- Special tokens: disabled for both tokenizers.
- Normalization: NFC during corpus preparation; no lowercasing.
- Truncation: none; no maximum length applied.
- Model/tokenizer files are downloaded or resolved through the local Hugging Face/tiktoken cache at runtime; they are not stored in the repository.

## Primary Corpus-Level Metrics

Values are summed token counts divided by summed denominators. `tok/grapheme` uses Unicode extended grapheme clusters counted with the `regex` library's Unicode `\\X` pattern. `tok/byte` uses UTF-8 bytes.

| Language | Tokenizer | Tok/sentence | Tok/word | Tok/grapheme | Tok/byte |
|---|---|---:|---:|---:|---:|
| English | GPT-2 | 26.744 | 1.235460 | 0.205105 | 0.204900 |
| English | XLM-R | 30.306 | 1.400009 | 0.232422 | 0.232191 |
| Hindi | GPT-2 | 198.124 | 7.811229 | 2.330871 | 0.594694 |
| Hindi | XLM-R | 37.806 | 1.490538 | 0.444776 | 0.113479 |
| Tamil | GPT-2 | 415.467 | 25.034165 | 4.212422 | 0.996489 |
| Tamil | XLM-R | 40.902 | 2.464570 | 0.414706 | 0.098103 |
| Telugu | GPT-2 | 346.939 | 20.699183 | 4.578482 | 0.991685 |
| Telugu | XLM-R | 39.949 | 2.383450 | 0.527199 | 0.114190 |
| Kannada | GPT-2 | 363.247 | 22.804131 | 4.064893 | 0.978709 |
| Kannada | XLM-R | 41.017 | 2.574989 | 0.458998 | 0.110514 |

## Strongest Finding

The token-count gap is tokenizer-dependent. GPT-2 produces very high Indic-script counts, while XLM-R substantially reduces them; XLM-R uses 13.318875% more English tokens than GPT-2 on this sample.

## Original Report Claims

- Supported as a supplied-sample observation: the original GPT-2 Hindi/English fertility result reproduces at approximately 5.89x.
- Not supported as universal: the controlled GPT-2 Hindi/English ratios are 6.31x by corpus tok/word and 7.41x by mean tokens/sentence; XLM-R gives approximately 1.07x and 1.25x respectively.
- Not supported: script complexity alone is established as the cause.
- Not supported: the penalty is tokenizer-independent.
- Not supported: Hindi is inherently 6x more expensive to serve. The experiment measures token counts, not serving cost.

## Reproducibility

Commands from the repository root:

```text
python submission/partA/tokenizer/scripts/download_corpus.py --limit 1000
python submission/partA/tokenizer/scripts/prepare_corpus.py
python submission/partA/tokenizer/scripts/validate_corpus.py
python submission/partA/tokenizer/scripts/run_tokenizer_comparison.py
python submission/partA/tokenizer/scripts/verify_results.py
```

The full analysis was run twice from the same prepared corpus. Relevant result-file hashes matched. The independent verifier reported `corpus_metric_checks=90/90`, `sentence_rows=10000`, and `deterministic=True`.

## Caveats

- FLORES-101 is a professionally translated multilingual benchmark drawn from a Wikipedia/news-oriented evaluation domain, not a representative production request distribution.
- The selected sample is the first 1,000 `devtest` IDs, not a random sample.
- Word counts are whitespace-delimited operational counts.
- Grapheme counts are Unicode extended grapheme clusters, not linguistic morphemes or words.
- UTF-8 byte normalization is a representation-level metric, not a semantic measure.
- GPT-2 and XLM-R are different tokenizer/model families; the comparison isolates tokenizer behavior on this text but does not compare model quality or serving systems.
- Cached tokenizer files are environment dependencies and are resolved dynamically at runtime.
