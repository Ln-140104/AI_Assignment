# Evidence matrix

| ID | Claim | Evidence | Calculation | Status |
|---|---|---|---|---|
| R1 | English fertility is 1.27 tok/word | starter_kit/fertility.py output and baseline reproduction | Mean of per-line `len(tokens) / len(words)` over the English corpus | SUPPORTED |
| R2 | Hindi fertility is 7.45 tok/word | starter_kit/fertility.py output and baseline reproduction | Mean of per-line `len(tokens) / len(words)` over the Hindi corpus | SUPPORTED |
| R3 | Hindi fertility is 5.89x English fertility | starter_kit/fertility.py output | `7.45 / 1.27` | SUPPORTED |
| R4 | The result is robust because `tok/char` agrees | starter_kit/REPORT_v0.md plus implementation | `1.579 / 0.226` roughly 7.0x, but this is an independent ratio comparison not a direct reproduction of the same metric | PARTIALLY SUPPORTED |
| R5 | Root cause is Unicode script complexity, not tokenizer behavior | starter_kit/REPORT_v0.md only | Not directly measured in the provided starter kit | NOT SUPPORTED |
| R6 | Long prompts have better throughput | bench_log.csv | Observed in benchmark rows where longer prompt length yields higher reported throughput at some batch sizes | SUPPORTED |
| R7 | Batch 48 should give ~3200 tok/s | starter_kit/REPORT_v0.md | This is extrapolation from observed data and is not a directly measured value | PARTIALLY SUPPORTED |
| R8 | Serving Hindi costs ~6x more per request than English | REPORT_v0.md | Derived from fertility ratio, assuming per-token cost scales proportionally | PARTIALLY SUPPORTED |
