#!/usr/bin/env python3
"""Independently audit saved sentence observations and aggregate results."""
import csv, hashlib, math, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; RESULTS=ROOT/'results'; LANGS=['eng','hin','tam','tel','kan']; TOKS=['gpt2','xlm-roberta-base']
def q(v,p): return statistics.quantiles(v,n=100,method='inclusive')[int(p*100)-1] if len(v)>1 else v[0]
def close(a,b): return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12)
if __name__=='__main__':
    with (RESULTS/'sentence_level_measurements.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    with (RESULTS/'master_results.csv').open(encoding='utf-8',newline='') as f: master={(r['language'],r['tokenizer']):r for r in csv.DictReader(f)}
    groups={(l,t):[r for r in rows if r['language']==l and r['tokenizer']==t] for l in LANGS for t in TOKS}; checks=[]
    for key,g in groups.items():
        m=master[key]; tokens=[int(r['token_count']) for r in g]; checks += [len(g)==int(m['num_sentences']),close(statistics.fmean(tokens),m['mean_tokens_per_sentence'])]
        for field,denom in [('word_count','aggregate_tokens_per_word'),('grapheme_clusters','aggregate_tokens_per_grapheme'),('utf8_bytes','aggregate_tokens_per_byte')]: checks.append(close(sum(tokens)/sum(int(r[field]) for r in g),m[denom]))
        for field,denom in [('word_count','mean_tokens_per_word'),('grapheme_clusters','mean_tokens_per_grapheme'),('utf8_bytes','mean_tokens_per_byte')]: checks.append(close(statistics.fmean(int(r['token_count'])/int(r[field]) for r in g),m[denom]))
    for tok in TOKS:
        e=groups[('eng',tok)]
        for lang in LANGS: checks.append(close(statistics.fmean(int(r['token_count']) for r in groups[(lang,tok)])/statistics.fmean(int(r['token_count']) for r in e),master[(lang,tok)]['relative_to_english']))
    reductions={}
    for lang in LANGS:
        g=statistics.fmean(int(r['token_count']) for r in groups[(lang,'gpt2')]); x=statistics.fmean(int(r['token_count']) for r in groups[(lang,'xlm-roberta-base')]); reductions[lang]=100*(1-x/g)
    eng_g=sum(int(r['token_count']) for r in groups[('eng','gpt2')]); eng_x=sum(int(r['token_count']) for r in groups[('eng','xlm-roberta-base')]); eng_words=sum(int(r['word_count']) for r in groups[('eng','gpt2')]); eng_bytes=sum(int(r['utf8_bytes']) for r in groups[('eng','gpt2')])
    print(f'sentence_rows={len(rows)} groups={len(groups)}'); print(f'corpus_metric_checks={sum(checks)}/{len(checks)}'); print(f'english_totals=gpt2:{eng_g},xlm_roberta:{eng_x},words:{eng_words},bytes:{eng_bytes},difference_percent:{100*(eng_x/eng_g-1):.6f}'); print('reductions=' + ','.join(f'{k}:{v:.6f}%' for k,v in reductions.items())); print('deterministic=' + str(all(checks)))
    if not all(checks): raise SystemExit(1)
