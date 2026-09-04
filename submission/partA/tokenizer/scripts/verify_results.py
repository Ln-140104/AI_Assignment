#!/usr/bin/env python3
"""Independently verify saved sentence measurements against master results."""
import csv, hashlib, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; RESULTS=ROOT/'results'
def q(v,p): return statistics.quantiles(v,n=100,method='inclusive')[int(p*100)-1] if len(v)>1 else v[0]
if __name__=='__main__':
    with (RESULTS/'sentence_level_measurements.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    with (RESULTS/'master_results.csv').open(encoding='utf-8',newline='') as f: master={(r['language'],r['tokenizer']):r for r in csv.DictReader(f)}
    checks=[]
    for key, group in __import__('itertools').groupby(sorted(rows,key=lambda r:(r['language'],r['tokenizer'])),key=lambda r:(r['language'],r['tokenizer'])):
        group=list(group); vals=[int(r['token_count']) for r in group]; expected=master[key]
        checks += [abs(statistics.fmean(vals)-float(expected['mean_tokens_per_sentence']))<1e-9, abs(statistics.median(vals)-float(expected['median_tokens_per_sentence']))<1e-9, abs(q(vals,.95)-float(expected['p95_tokens_per_sentence']))<1e-9]
    digest=hashlib.sha256((RESULTS/'master_results.csv').read_bytes()).hexdigest()
    print(f'sentence_rows={len(rows)}'); print(f'groups={len(master)}'); print(f'independent_checks={sum(checks)}/{len(checks)}'); print(f'master_sha256={digest}'); print(f'deterministic={all(checks)}')
    if not all(checks): raise SystemExit(1)
