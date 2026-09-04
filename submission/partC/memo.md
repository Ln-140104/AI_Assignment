# Decision

**Recommend (c) prompt-engineering only for the three-week launch review.** It is the only option that adds no model-training dependency, no second model in the serving path, and is reversible if the style change fails.

## Constraints & assumptions

**Facts:** one A100-80GB is available for two weeks; one reviewer covers Hindi and Kannada for 10 h/week; launch review is in three weeks; no external API budget.

**Assumptions:** use 120 paired test prompts (20 per target language); a reviewer judgment takes 8 minutes; the prompt variant needs one engineer for prompt, regression, and evaluation work during the two-week window; no quality gain is assumed before testing. The six target languages are Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi.

## Cost / feasibility

**Reviewer budget:** 10 h/week x 2 weeks = 20 h. Allocate 4 h to rubric calibration, 5.33 h to 40 native paired judgments (20 Hindi + 20 Kannada; 40 x 8 min = 320 min = 5.33 h), 6.67 h to semantic/regression review and final adjudication, and 4 h contingency. Native evidence covers only Hindi/Kannada; the other four languages remain lower-confidence and are not claimed as natively validated.

**Derived option comparison:** prompt-only requires 0 training GPU-hours and 0 additional model calls per response. SFT would require an assumed 3,000 synthetic pairs (500/language x 6) and an assumed 256 total tokens/pair, or 768,000 training tokens, plus data QA and training/evaluation risk within two weeks. A rewriter would require an additional <=1B model call for every response; its latency and memory impact are not supplied and must be measured before launch. These are planning assumptions, not measurements.

## Evaluation plan

**Success metric:** on 40 Hindi/Kannada native-rated paired judgments, the prompt-only variant must win against the current prompt in at least 26/40 cases (65%), with semantic-preservation regressions <=5% on the same set. The prompt-only path has no added model call; SFT or a rewriter would have to beat this threshold while also justifying their training or serving cost.

**Kill criterion:** abandon prompt-only by the end of week 2 if it wins fewer than 26/40 judgments or semantic regressions exceed 5%. Do not claim native-quality success for Tamil, Telugu, Bengali, or Marathi without qualified review.

## Day-1 experiment

Create baseline and prompt-only outputs for 120 fixed prompts, 20 per target language. Use 40 pairs (20 Hindi + 20 Kannada) for native review and a checklist for the remaining 80 cases. **Decision rule:** continue only if the Hindi/Kannada result reaches at least 26/40 wins (65% preference) with no more than 5% semantic regressions; otherwise investigate a different option before week 2.

## Timeline

Week 1: prompt variant, fixed test set, rubric calibration, and first review. Week 2: regression fixes, second review, and launch gate against the numeric thresholds. Week 3: launch review and rollback-ready prompt decision. No external API or Part C implementation is assumed.
