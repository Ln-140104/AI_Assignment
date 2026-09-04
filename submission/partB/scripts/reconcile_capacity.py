#!/usr/bin/env python3
"""Reproduce Part B arithmetic from the supplied model specification and bench log."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SPEC=ROOT/'original'/'starter_kit'/'bench'/'model_spec.md'
LOG=ROOT/'original'/'starter_kit'/'bench'/'bench_log.csv'
OUT=Path(__file__).resolve().parents[1]/'evidence'

def read_rows():
    with LOG.open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
def main():
    layers,kv_heads,head_dim,tensors,fp16=28,8,128,2,2
    bytes_token=layers*kv_heads*head_dim*tensors*fp16
    seq_bytes=bytes_token*4096
    gpu_decimal=24e9; usable_decimal=gpu_decimal*.92; weights_decimal=4.2e9*2; overhead_decimal=1.6e9
    kv_budget=usable_decimal-weights_decimal-overhead_decimal; seq_decimal=seq_bytes
    capacity=math.floor(kv_budget/seq_decimal)
    rows=read_rows(); long=[r for r in rows if r['prompt_len']=='3584']
    boundary=[r for r in long if r['batch_size'] in {'24','32','48'}]
    derived=[]
    for r in boundary:
        batch=int(r['batch_size']); prompt=int(r['prompt_len']); gen=int(r['gen_len']); elapsed=float(r['wall_clock_s']); reported=float(r['reported_tok_s'])
        derived.append({'batch':batch,'reported_tok_s':reported,'total_goodput':batch*(prompt+gen)/elapsed,'generated_goodput':batch*gen/elapsed,'converted_generated_goodput':reported*gen/(prompt+gen)})
    result={'kv_bytes_per_token':bytes_token,'kv_kib_per_token':bytes_token/1024,'sequence_bytes_4096':seq_bytes,'sequence_mib_4096':seq_bytes/(1024**2),'gpu_usable_decimal_gb':usable_decimal/1e9,'weights_decimal_gb':weights_decimal/1e9,'overhead_decimal_gb':overhead_decimal/1e9,'kv_budget_decimal_gb':kv_budget/1e9,'theoretical_complete_sequences':capacity,'boundary_rows':boundary,'derived_goodput':derived}
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'capacity_calculations.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('KV bytes/token = 28 * 8 * 128 * 2 * 2 = 114688 bytes')
    print(f'KV KiB/token = {bytes_token/1024:.3f}')
    print(f'4096-token KV = {seq_bytes:,} bytes = {seq_bytes/(1024**2):.3f} MiB')
    print(f'usable GPU memory = 24 GB * .92 = {usable_decimal/1e9:.3f} decimal GB')
    print(f'KV budget = {usable_decimal/1e9:.3f} - {weights_decimal/1e9:.3f} - {overhead_decimal/1e9:.3f} = {kv_budget/1e9:.3f} decimal GB')
    print(f'theoretical complete sequences = floor({kv_budget/seq_decimal:.6f}) = {capacity}')
    for d in derived: print(f"batch {d['batch']}: reported={d['reported_tok_s']:.1f}, total={d['total_goodput']:.3f}, generated={d['generated_goodput']:.3f}, converted={d['converted_generated_goodput']:.3f}")
if __name__=='__main__': main()
