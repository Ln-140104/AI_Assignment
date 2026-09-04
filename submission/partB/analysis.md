# Part B - Capacity Reconciliation

## Research Question

Does the supplied model specification explain the long-context benchmark boundary, and what does the benchmark's throughput counter actually measure?

## Evidence Sources and Commands

Source files: `original/starter_kit/bench/model_spec.md`, `original/starter_kit/bench/bench_log.csv`, and `original/starter_kit/REPORT_v0.md`. Reproduction command:

```text
python submission/partB/scripts/reconcile_capacity.py
```

The script writes `submission/partB/evidence/capacity_calculations.json`.

## B1 - KV Cache Reconciliation

### Direct derivation

The model specification gives 28 layers, 8 KV heads, head dimension 128, two tensors (K and V), and FP16 at 2 bytes/value.

```text
KV bytes/token = 28 * 8 * 128 * 2 * 2
                = 114,688 bytes
                = 112.000 KiB

KV bytes for 4,096 tokens = 114,688 * 4,096
                           = 469,762,048 bytes
                           = 448.000 MiB
```

KiB and MiB above are binary units: 1 KiB = 1,024 bytes and 1 MiB = 1,048,576 bytes.

The GPU capacity arithmetic uses decimal GB for the stated 24 GB GPU, 4.2B parameters, and 1.6 GB runtime overhead:

```text
available under utilization = 24,000,000,000 * 0.92
                             = 22.080 decimal GB
model weights = 4,200,000,000 * 2 bytes
              = 8.400 decimal GB
remaining KV budget = 22.080 - 8.400 - 1.600
                    = 12.080 decimal GB
complete 4,096-token sequences = floor(12,080,000,000 / 469,762,048)
                                = floor(25.715147)
                                = 25
```

The simplified calculation uses the model's approximate 4.2B parameter count and treats decimal GB consistently for GPU, weights, overhead, and budget. It does not model allocator fragmentation, framework buffers, or other runtime allocations beyond the stated 1.6 GB.

### Benchmark reconciliation

| Long row | Reported tok/s | KV utilization | Preemptions | Interpretation |
|---|---:|---:|---:|---|
| batch 24 | 1,607.4 | 0.93 | 0 | below the simplified 25-sequence boundary and no observed preemption |
| batch 32 | 1,384.0 | 0.97 | 7 | saturated region with preemption and lower throughput |
| batch 48 | 1,298.5 | 0.97 | 23 | saturated region with more preemptions and lower throughput |

**Observation:** the log is directionally consistent with the simplified capacity: batch 24 is near but below the theoretical 25-sequence limit, while batches 32 and 48 exceed it and show preemption. Exact equality is not expected because the simplified model omits allocator and runtime details.

## B2 - Long-Context Sweep Anomaly

The relevant `prompt_len=3584` rows are:

| Batch | Throughput (`reported_tok_s`) | TTFT p50 ms | ITL p50 ms | p95 E2E ms | Preemptions | KV utilization |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 565.4 | 483.2 | 51.33 | 32,673.3 | 0 | 0.16 |
| 8 | 902.6 | 519.0 | 62.26 | 39,982.9 | 0 | 0.31 |
| 16 | 1,311.4 | 498.3 | 77.20 | 54,602.1 | 0 | 0.62 |
| 24 | 1,607.4 | 500.5 | 96.07 | 69,221.3 | 0 | 0.93 |
| 32 | 1,384.0 | 636.9 | 101.79 | 97,465.7 | 7 | 0.97 |
| 48 | 1,298.5 | 955.4 | 100.00 | 105,427.5 | 23 | 0.97 |

**Measured progression:** reported throughput rises from 565.4 at batch 4 to 1,607.4 at batch 24, then drops to 1,384.0 at batch 32 and 1,298.5 at batch 48. TTFT rises from 500.5 ms at batch 24 to 636.9 ms and 955.4 ms. p95 latency rises from 69,221.3 ms to 97,465.7 ms and 105,427.5 ms. Preemptions change from 0 to 7 to 23, while KV utilization reaches 0.97.

**Inference:** the post-batch-24 degradation is consistent with a KV-constrained scheduler entering a preemption/saturation regime. The evidence is not merely high utilization: the throughput drop co-occurs with increased TTFT, sharply higher p95 latency, and preemptions.

**Primary recommendation:** cap long-context scheduling at batch 24 for this configuration. This is a deployment recommendation, not a new measured result.

**Prediction:** relative to allowing batch 32 or 48 for these prompts, the cap should avoid the observed preemption regime and target the measured batch-24 operating point of 1,607.4 reported total-token tok/s and 200.916 generated-token goodput. The exact production improvement is not measured here.

## B3 - Correcting Report Section 2

The report says long prompts hit 1,311 tok/s at batch 16 versus 883 tok/s for short prompts, which compares the `reported_tok_s` column. It then treats that counter as if it were generated-token throughput and extrapolates batch 48 to approximately 3,200 tok/s.

The benchmark specification says `reported_tok_s` is the harness's built-in throughput counter. The row arithmetic shows it counts prompt/prefill plus generated tokens:

```text
reported total processed tokens = batch * (prompt_len + gen_len)
                                 = 24 * (3584 + 512)
                                 = 98,304 tokens
98,304 / 61.16 seconds = 1,607.325 tokens/s ~= reported 1,607.4
```

### Batch-24 generated-token goodput, two methods

**Method 1: underlying row values**

```text
24 * 512 generated tokens / 61.16 seconds
= 12,288 / 61.16
= 200.916 generated tokens/s
```

**Method 2: convert reported total-token throughput**

```text
1,607.4 * 512 / (3584 + 512)
= 1,607.4 * 512 / 4,096
= 200.925 generated tokens/s
```

The small difference is due to the logged throughput being rounded to one decimal place.

### Batch-48 check

```text
reported total-token rate = 48 * 4096 / 151.41
                          = 1,298.514 ~= 1,298.5 tok/s
honest generated-token goodput = 48 * 512 / 151.41
                               = 162.314 generated tokens/s
```

Therefore the report's approximately 3,200 tok/s claim is wrong: batch 48 actually logs 1,298.5 total processed tokens/s and derives to 162.314 generated tokens/s. The report's 1,600 tok/s figure is also a rounded best observed prefill-plus-generation counter, not generated-token goodput.

### Corrected conclusion

Longer prompts do not by themselves establish better serving throughput. In this log, `reported_tok_s` is prompt/prefill plus generation throughput and rises with batching through batch 24, then degrades at batches 32 and 48 as KV utilization saturates and preemptions appear. Generated-token goodput at batch 24 is approximately 200.9 tokens/s, while batch 48 is approximately 162.3 tokens/s.

## B4 - Production Counter

The single proposed serving metric is **preemption rate**, defined as preempted sequences divided by submitted sequences over a serving interval. It measures how often the scheduler must preempt sequences, using the supplied `preempted_seqs` divided by `num_requests`; it tests B2 because the inferred boundary is a scheduler/KV saturation regime and a rising rate is a direct operational signal. Near batch 24, the benchmark records 0/24 = 0%; batch 32 records 7/32 = 21.875%; and batch 48 records 23/48 = 47.917%. If production showed the same throughput/latency degradation while preemption rate remained zero and KV capacity had substantial headroom, preemption-driven KV saturation would be falsified and another bottleneck would need investigation.

## Evidence Classification

- **Directly measured:** all values copied from the supplied model specification or benchmark log, including throughput, TTFT, ITL, p95 latency, preemptions, KV utilization, wall-clock time, prompt length, and generation length.
- **Derived:** KV arithmetic, 25-sequence theoretical capacity, goodput conversions, ratios, and preemption percentages.
- **Prediction/inference:** the recommendation to cap at batch 24 and the expectation that it avoids the observed preemption regime.

## Caveats

The capacity calculation is simplified and uses approximate model size. The benchmark has identical simultaneous requests and fixed generation with no early stopping. `reported_tok_s` is not a pure decode counter. The benchmark does not establish production behavior, cost, or a universal batch-size rule.
