# Part C — Product / Model Decision

## Objective

Select the most appropriate approach for improving conversational
style under the supplied engineering constraints.

## Decision Criteria

The analysis will consider:

- quality improvement;
- inference latency;
- engineering effort;
- GPU availability;
- reviewer bandwidth;
- evaluation cost;
- deployment risk;
- reproducibility;
- time to launch.

## Experiment / Analysis IDs

- C1 — Constraint analysis
- C2 — Option comparison
- C3 — Reviewer-budget calculation
- C4 — Evaluation design
- C5 — Recommendation

## Status

Completed as a decision memo only. The recommendation is prompt-engineering only;
no production model implementation or external API is assumed.

## Deliverables

- `memo.md` — one-page decision memo
- `DEFENSE_FACTS.md` — labeled assumptions, arithmetic, comparison, evaluation plan,
  and caveats for the live defense
