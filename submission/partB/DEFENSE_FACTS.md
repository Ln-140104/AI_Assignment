# Part B Defense Facts

## B1 KV Cache

- Formula: `28 layers * 8 KV heads * 128 head_dim * 2 K/V tensors * 2 FP16 bytes = 114,688 bytes/token`.
- KV size: `112.000 KiB/token`.
- One 4,096-token sequence: `469,762,048 bytes = 448.000 MiB`.
- GPU budget: `24 GB * 0.92 = 22.080 decimal GB`.
- Approximate FP16 weights: `4.2B * 2 bytes = 8.400 decimal GB`.
- Remaining KV budget after weights and stated 1.6 GB overhead: `22.080 - 8.400 - 1.600 = 12.080 decimal GB`.
- Simplified theoretical capacity: `floor(12,080,000,000 / 469,762,048) = 25` complete 4,096-token sequences.
- KiB/MiB are binary units. GPU, weights, overhead, and budget are expressed in decimal GB.

## Benchmark Boundary

- Long batch 24: `reported_tok_s=1607.4`, `KV=0.93`, `preempted=0`.
- Long batch 32: `reported_tok_s=1384.0`, `KV=0.97`, `preempted=7`.
- Long batch 48: `reported_tok_s=1298.5`, `KV=0.97`, `preempted=23`.
- The simplified capacity predicts a boundary near 25 sequences; the log is directionally consistent, not exactly equal because allocator/runtime details are omitted.

## B2 Finding

- Long throughput rises from `565.4` at batch 4 to `1607.4` at batch 24, then falls to `1384.0` and `1298.5` at batches 32 and 48.
- TTFT rises from `500.5 ms` at batch 24 to `636.9 ms` and `955.4 ms`; p95 latency rises from `69,221.3 ms` to `97,465.7 ms` and `105,427.5 ms`; preemptions rise from `0` to `7` and `23`.
- Evidence-backed inference: the post-24 decline is consistent with KV-constrained scheduler saturation and preemption.
- Primary recommendation: cap long-context batch size at 24. The exact production effect is a prediction, not measured.

## B3 Goodput

- Batch 24 total-token counter: `24 * (3584 + 512) / 61.16 = 1607.325 ~= 1607.4`.
- Batch 24 generated goodput, method 1: `24 * 512 / 61.16 = 200.916 tokens/s`.
- Batch 24 generated goodput, method 2: `1607.4 * 512 / 4096 = 200.925 tokens/s`.
- Batch 48 generated goodput: `48 * 512 / 151.41 = 162.314 tokens/s`.
- The original report misread total prompt-plus-generation throughput as generated-token throughput and incorrectly extrapolated batch 48 to approximately 3,200 tok/s.

## B4 Counter

- Proposed operational metric: preemption rate = preempted sequences / submitted sequences.
- Measured benchmark reference: batch 24 `0/24=0%`; batch 32 `7/32=21.875%`; batch 48 `23/48=47.917%`.
- A production observation of degradation with zero preemptions and substantial KV headroom would falsify the proposed mechanism.

## Commands

```text
python submission/partB/scripts/reconcile_capacity.py
```

The command was run twice. The output is deterministic. No production values are claimed.

## Caveats

The KV calculation is simplified, model size is approximate, and `reported_tok_s` is not pure decode throughput. The benchmark uses simultaneous identical requests with fixed generation and does not prove universal production behavior.
