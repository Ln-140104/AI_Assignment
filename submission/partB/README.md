# Part B — Inference Capacity & Throughput Audit

## Objective

Reconcile the model specification with the supplied benchmark
results and determine the practical operating region.

## Questions

1. What is the KV-cache requirement per token?
2. What is the theoretical concurrency limit?
3. Does the benchmark agree with the theoretical estimate?
4. What happens when the system exceeds the safe operating region?
5. What does the reported throughput metric actually measure?

## Experiment IDs

- B1 — KV-cache derivation
- B2 — Theoretical capacity
- B3 — Benchmark reconciliation
- B4 — Throughput definition
- B5 — Preemption analysis

## Status

Executed against the supplied model specification and benchmark log. Part C is not
started.

## Evidence Artifacts

- `analysis.md` contains the B1 KV derivation, B2 long-context sweep, B3 corrected
	throughput interpretation, and B4 operational counter proposal.
- `evidence/capacity_calculations.json` contains the reproducible arithmetic output.
- `DEFENSE_FACTS.md` contains only directly measured or transparently derived facts.

## Reproduction

From the repository root:

```text
python submission/partB/scripts/reconcile_capacity.py
```
