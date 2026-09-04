# Part C Defense Facts

## Decision comparison

- [FACT] The assignment offers exactly three paths: (a) SFT on synthetic casualized response pairs, (b) a <=1B inference-time rewriter, and (c) prompt-only.
- [FACT] Constraints are one A100-80GB for two weeks, one reviewer covering Hindi and Kannada for 10 hours/week, a launch review in three weeks, and no external API budget.
- [ASSUMPTION] One engineer is available for the two-week implementation/evaluation window.
- [DECISION] Choose (c) prompt-only.
- [DERIVED] Prompt-only has no training job and no additional model call per response; it is reversible by reverting the prompt.
- [ASSUMPTION] SFT planning comparison: 500 synthetic pairs per target language, 6 languages, gives `500 * 6 = 3,000 pairs`.
- [ASSUMPTION] Average pair size is 256 total input/output tokens.
- [DERIVED] SFT planning volume is `3,000 * 256 = 768,000 tokens`; this is not a measured dataset or training result.
- [DECISION] SFT loses on schedule risk because synthetic-data QA, training, and evaluation must fit two weeks and the reviewer cannot natively validate four target languages.
- [DECISION] The rewriter loses on serving risk because it adds a model call to every response and its latency/memory behavior is not supplied or measured; the <=1B limit does not prove acceptable production latency.
- [DECISION] Prompt-only wins on reversibility, zero added model serving dependency, and fit to the three-week review.

## Reviewer budget

- [FACT] Reviewer availability is 10 hours/week for two weeks before the launch review.
- [DERIVED] `10 hours/week * 2 weeks = 20 reviewer-hours`.
- [ASSUMPTION] The fixed evaluation set has 120 prompts: 20 per target language.
- [ASSUMPTION] Each native paired judgment takes 8 minutes.
- [DERIVED] `40 native judgments * 8 minutes = 320 minutes = 5.33 hours`; the 40 are 20 Hindi and 20 Kannada.
- [DECISION] Allocate 4 hours to rubric calibration, 5.33 hours to 40 paired Hindi/Kannada judgments, 6.67 hours to semantic/regression review and final adjudication, and 4 hours contingency.
- [FACT] The reviewer covers Hindi and Kannada only.
- [DECISION] Native validation is not claimed for Tamil, Telugu, Bengali, or Marathi.

## Success metric

- [ASSUMPTION] Fixed evaluation set: 120 prompts, 20 per target language.
- [DECISION] Prompt-only succeeds if it wins at least 26 of 40 native-rated paired judgments: `26 / 40 = 65%`.
- [DECISION] It must also keep semantic-preservation regressions at or below 5% on the same test set.
- [FACT] These are decision thresholds, not observed results.

## Kill criterion

- [DECISION] Abandon prompt-only by the end of week 2 if preference is below `26/40` or semantic regressions exceed `5%`.
- [FACT] The deadline is chosen because the launch review is in week 3.
- [FACT] No claim is made that this threshold has already been met.

## Day-1 experiment

- [DECISION] Generate baseline and prompt-only outputs for 120 fixed prompts: 20 each in Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi.
- [DECISION] Metric: paired style preference for 40 Hindi/Kannada cases and semantic-preservation checklist across the remaining 80 prompts.
- [DECISION] Decision rule: continue only at >=26/40 Hindi/Kannada preference and <=5% semantic regressions.
- [ASSUMPTION] The first experiment fits within day 1 because it uses a fixed prompt set and no training or new serving model.

## Timeline

- [DECISION] Week 1: implement prompt variant, freeze test set, calibrate rubric, start review.
- [DECISION] Week 2: fix regressions, complete review, apply kill gate.
- [DECISION] Week 3: launch review with rollback-ready prompt.
- [FACT] No external API is assumed.
- [FACT] No production model implementation is created by this decision memo.

## Biggest uncertainty

- [FACT] Native reviewer coverage is limited to Hindi and Kannada.
- [DECISION] Results for Tamil, Telugu, Bengali, and Marathi have lower validation confidence and must not be presented as native-quality evidence.
- [FACT] No measured baseline quality, latency, training speed, or reviewer speed was supplied; all such quantities above are explicitly assumptions or planning arithmetic.
