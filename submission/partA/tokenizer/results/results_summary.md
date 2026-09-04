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
The final sample contains 1000 shared sentence IDs selected contiguously from `devtest` (1,012 available). For each sentence and tokenizer, the experiment records token count, whitespace-delimited word count, Unicode code points, and UTF-8 bytes. It reports sentence-level means and medians, standard deviation, P25/P75/P90/P95, mean-of-sentence tok/word, aggregate tok/word, tok/char, tok/byte, and relative expansion.

## Main Results
- English / gpt2: mean tok/sentence=26.744, median=26.000, mean tok/word=1.245, aggregate tok/word=1.235, tok/char=0.2072, tok/byte=0.2070, relative expansion=1.000x.
- English / xlm-roberta-base: mean tok/sentence=30.306, median=29.000, mean tok/word=1.413, aggregate tok/word=1.400, tok/char=0.2344, tok/byte=0.2342, relative expansion=1.000x.
- Hindi / gpt2: mean tok/sentence=198.124, median=190.000, mean tok/word=7.851, aggregate tok/word=7.811, tok/char=1.5286, tok/byte=0.5947, relative expansion=7.408x.
- Hindi / xlm-roberta-base: mean tok/sentence=37.806, median=36.000, mean tok/word=1.506, aggregate tok/word=1.491, tok/char=0.2940, tok/byte=0.1146, relative expansion=1.247x.
- Tamil / gpt2: mean tok/sentence=415.467, median=399.000, mean tok/word=25.237, aggregate tok/word=25.034, tok/char=2.7233, tok/byte=0.9961, relative expansion=15.535x.
- Tamil / xlm-roberta-base: mean tok/sentence=40.902, median=39.000, mean tok/word=2.485, aggregate tok/word=2.465, tok/char=0.2690, tok/byte=0.0986, relative expansion=1.350x.
- Telugu / gpt2: mean tok/sentence=346.939, median=331.500, mean tok/word=20.817, aggregate tok/word=20.699, tok/char=2.6436, tok/byte=0.9906, relative expansion=12.973x.
- Telugu / xlm-roberta-base: mean tok/sentence=39.949, median=38.000, mean tok/word=2.407, aggregate tok/word=2.383, tok/char=0.3062, tok/byte=0.1152, relative expansion=1.318x.
- Kannada / gpt2: mean tok/sentence=363.247, median=344.500, mean tok/word=23.006, aggregate tok/word=22.804, tok/char=2.6595, tok/byte=0.9785, relative expansion=13.582x.
- Kannada / xlm-roberta-base: mean tok/sentence=41.017, median=39.000, mean tok/word=2.603, aggregate tok/word=2.575, tok/char=0.3021, tok/byte=0.1114, relative expansion=1.353x.

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
- Claim A: the original 5.89x Hindi/English tok/word result reproduces on the supplied sample, but it does not generalize as a fixed value.
- Claim B: script complexity as the root cause is not established because tokenizer choice materially changes the gap.
- Claim C: tokenization inefficiency is not language-invariant; tokenizer choice changes relative expansion.
- Claim D: an inherent language penalty is not established by these measurements.

## What the Experiment Establishes
The five languages can be compared on the same 1,000 aligned IDs. Tokenizer choice materially affects the observed language differences.

## What the Experiment Does Not Establish
It does not establish causality, serving cost, model quality, or an intrinsic property of a language.

## Limitations
The sample is the first 1,000 `devtest` IDs rather than a random sample; FLORES-101 is a translation benchmark domain; whitespace word counts are an operational denominator; byte-normalized values are representation-level metrics.
