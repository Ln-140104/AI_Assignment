# Controlled Multilingual Tokenizer Evaluation

## Research Question
Does the Hindi tokenization penalty generalize to a controlled five-language parallel corpus, and how much does tokenizer choice affect the result?

## Dataset
FLORES-101 version 1.0.0 from https://dl.fbaipublicfiles.com/flores101/dataset/flores101_dataset.tar.gz; pinned archive SHA256 49fa80207b09fcc0eca8253ed13303b3a0ae0f16081af862601c73ac76f2cba6. Split: devtest. The archive is CC-BY-SA-4.0 and documents professionally translated, multilingual-aligned sentences.

## Languages
English (`eng`), Hindi (`hin`), Tamil (`tam`), Telugu (`tel`), and Kannada (`kan`).

## Tokenizers
GPT-2 via `tiktoken` encoding `gpt2`; XLM-RoBERTa-base via Transformers. Both use no special tokens, no truncation, and no lowercasing. Corpus text is NFC-normalized.

## Methodology
The final sample contains 1000 shared sentence IDs selected contiguously from `devtest` (1,012 available). For each sentence and tokenizer, the experiment records token count, whitespace-delimited word count, Unicode code points, Unicode extended grapheme clusters measured with `regex` `\X`, and UTF-8 bytes. It reports sentence-level means and medians, standard deviation, P25/P75/P90/P95, mean-of-sentence ratios, aggregate ratios, and relative expansion.

## Main Results
- English / gpt2: mean tok/sentence=26.744, median=26.000, mean tok/word=1.245, aggregate tok/word=1.235, mean tok/grapheme=0.2072, aggregate tok/grapheme=0.2051, tok/byte=0.2070, aggregate tok/byte=0.2049, relative expansion=1.000x.
- English / xlm-roberta-base: mean tok/sentence=30.306, median=29.000, mean tok/word=1.413, aggregate tok/word=1.400, mean tok/grapheme=0.2344, aggregate tok/grapheme=0.2324, tok/byte=0.2342, aggregate tok/byte=0.2322, relative expansion=1.000x.
- Hindi / gpt2: mean tok/sentence=198.124, median=190.000, mean tok/word=7.851, aggregate tok/word=7.811, mean tok/grapheme=2.3365, aggregate tok/grapheme=2.3309, tok/byte=0.5947, aggregate tok/byte=0.5947, relative expansion=7.408x.
- Hindi / xlm-roberta-base: mean tok/sentence=37.806, median=36.000, mean tok/word=1.506, aggregate tok/word=1.491, mean tok/grapheme=0.4481, aggregate tok/grapheme=0.4448, tok/byte=0.1146, aggregate tok/byte=0.1135, relative expansion=1.247x.
- Tamil / gpt2: mean tok/sentence=415.467, median=399.000, mean tok/word=25.237, aggregate tok/word=25.034, mean tok/grapheme=4.2136, aggregate tok/grapheme=4.2124, tok/byte=0.9961, aggregate tok/byte=0.9965, relative expansion=15.535x.
- Tamil / xlm-roberta-base: mean tok/sentence=40.902, median=39.000, mean tok/word=2.485, aggregate tok/word=2.465, mean tok/grapheme=0.4156, aggregate tok/grapheme=0.4147, tok/byte=0.0986, aggregate tok/byte=0.0981, relative expansion=1.350x.
- Telugu / gpt2: mean tok/sentence=346.939, median=331.500, mean tok/word=20.817, aggregate tok/word=20.699, mean tok/grapheme=4.6018, aggregate tok/grapheme=4.5785, tok/byte=0.9906, aggregate tok/byte=0.9917, relative expansion=12.973x.
- Telugu / xlm-roberta-base: mean tok/sentence=39.949, median=38.000, mean tok/word=2.407, aggregate tok/word=2.383, mean tok/grapheme=0.5305, aggregate tok/grapheme=0.5272, tok/byte=0.1152, aggregate tok/byte=0.1142, relative expansion=1.318x.
- Kannada / gpt2: mean tok/sentence=363.247, median=344.500, mean tok/word=23.006, aggregate tok/word=22.804, mean tok/grapheme=4.0654, aggregate tok/grapheme=4.0649, tok/byte=0.9785, aggregate tok/byte=0.9787, relative expansion=13.582x.
- Kannada / xlm-roberta-base: mean tok/sentence=41.017, median=39.000, mean tok/word=2.603, aggregate tok/word=2.575, mean tok/grapheme=0.4614, aggregate tok/grapheme=0.4590, tok/byte=0.1114, aggregate tok/byte=0.1105, relative expansion=1.353x.

## Parallel-Sentence Analysis
Relative expansion is computed per aligned sentence as non-English token count divided by the English count under the same tokenizer. Distribution data and raw observations are in `sentence_level_measurements.csv`.

## Tokenizer Comparison
- English token-count reduction from GPT-2 to XLM-RoBERTa: -13.32%.
- Hindi token-count reduction from GPT-2 to XLM-RoBERTa: 80.92%.
- Tamil token-count reduction from GPT-2 to XLM-RoBERTa: 90.16%.
- Telugu token-count reduction from GPT-2 to XLM-RoBERTa: 88.49%.
- Kannada token-count reduction from GPT-2 to XLM-RoBERTa: 88.71%.

## Robustness Across Metrics
Language rankings are saved in `language_rankings.csv` for mean tok/sentence, relative expansion, and mean tok/word. These metrics use different denominators, so agreement is a robustness observation rather than proof of linguistic causality.
Per-sentence expansion mean, median, standard deviation, P25, P75, P90, and P95 are saved in `relative_expansion.csv`.

## Validation of Previous Report
- Exact command: `python submission/partA/tokenizer/scripts/run_tokenizer_comparison.py`.
- Claim A: supplied sample GPT-2 Hindi/English tok/word ratio = 5.89x; controlled GPT-2 corpus tok/word ratio = 6.31x and mean sentence ratio = 7.41x; XLM-R ratios = 1.07x and 1.25x. The supplied-sample observation reproduces, but 5.89x is not universal.
- Claim B: GPT-2 Hindi mean tokens/sentence = 198.124 versus XLM-R = 37.806 on the same IDs. Script complexity alone is not established as the cause.
- Claim C: GPT-2 versus XLM-R relative expansion differs for every Indic language. The penalty is not tokenizer-independent.
- Claim D: token counts were measured, but serving cost was not. Hindi is not established as inherently 6x more expensive to serve.

## What the Experiment Establishes
The five languages can be compared on the same 1,000 aligned IDs. Tokenizer choice materially affects the observed language differences.

## What the Experiment Does Not Establish
It does not establish causality, serving cost, model quality, or an intrinsic property of a language.

## Limitations
The sample is the first 1,000 `devtest` IDs rather than a random sample; FLORES-101 is a translation benchmark domain; whitespace word counts are an operational denominator; byte-normalized values are representation-level metrics.
