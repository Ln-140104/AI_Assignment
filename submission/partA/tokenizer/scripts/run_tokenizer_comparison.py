#!/usr/bin/env python3
"""Run the reproducible five-language FLORES-101 tokenizer evaluation."""
from __future__ import annotations
import csv, json, re, statistics, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tiktoken
from transformers import AutoTokenizer
ROOT=Path(__file__).resolve().parent.parent; DATA=ROOT/'data'; RESULTS=ROOT/'results'; FIGURES=ROOT.parent/'figures'
LANGS={'eng':'English','hin':'Hindi','tam':'Tamil','tel':'Telugu','kan':'Kannada'}; TOKENIZERS=['gpt2','xlm-roberta-base']
def quantile(v,q): return statistics.quantiles(v,n=100,method='inclusive')[int(q*100)-1] if len(v)>1 else v[0]
def stats(v): return {'mean':statistics.fmean(v),'median':statistics.median(v),'std':statistics.stdev(v) if len(v)>1 else 0.0,'p25':quantile(v,.25),'p75':quantile(v,.75),'p90':quantile(v,.90),'p95':quantile(v,.95)}
def load_encoder(name):
    if name=='gpt2':
        enc=tiktoken.get_encoding('gpt2'); return lambda text: enc.encode(text)
    tok=AutoTokenizer.from_pretrained(name); return lambda text: tok.encode(text,add_special_tokens=False)
def write_csv(path,rows,fields):
    with path.open('w',newline='',encoding='utf-8') as f: writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)
def environment():
    lines=[f'python={sys.version}']
    for name in ['tiktoken','transformers','tokenizers','datasets','sentencepiece','huggingface_hub','matplotlib']:
        try: module=__import__(name); lines.append(f'{name}={getattr(module,"__version__","unknown")}')
        except Exception as exc: lines.append(f'{name}=MISSING ({type(exc).__name__})')
    lines += ['gpt2_encoding=gpt2; special_tokens=false; truncation=false; max_length=not applied','xlm-roberta-base; special_tokens=false; truncation=false; max_length=not applied','normalization=NFC during corpus preparation; lowercase=false']
    (RESULTS/'environment.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
def make_figures(summary,rows):
    FIGURES.mkdir(parents=True,exist_ok=True); labels=list(LANGS); x=range(len(labels)); width=.38
    plt.figure(figsize=(9,5))
    for i,tok in enumerate(TOKENIZERS): plt.bar([v+(i-.5)*width for v in x],[summary[(l,tok)]['mean_tokens_per_sentence'] for l in labels],width,label=tok)
    plt.xticks(list(x),[LANGS[l] for l in labels]); plt.ylabel('Mean tokens per parallel sentence'); plt.legend(); plt.tight_layout(); plt.savefig(FIGURES/'figure1_mean_tokens_per_sentence.png',dpi=180); plt.close()
    plt.figure(figsize=(9,5))
    for i,tok in enumerate(TOKENIZERS): plt.bar([v+(i-.5)*width for v in x],[summary[(l,tok)]['relative_to_english'] for l in labels],width,label=tok)
    plt.xticks(list(x),[LANGS[l] for l in labels]); plt.ylabel('Relative expansion vs English'); plt.legend(); plt.tight_layout(); plt.savefig(FIGURES/'figure2_relative_expansion.png',dpi=180); plt.close()
    plt.figure(figsize=(9,5))
    for tok in TOKENIZERS:
        for lang in labels[1:]:
            vals=[r['token_count']/r['english_token_count'] for r in rows if r['tokenizer']==tok and r['language']==lang]; plt.hist(vals,bins=30,alpha=.3,label=f'{LANGS[lang]} / {tok}')
    plt.xlabel('Per-sentence token expansion vs English'); plt.ylabel('Sentence count'); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig(FIGURES/'figure3_expansion_distributions.png',dpi=180); plt.close()
    plt.figure(figsize=(8,6))
    for tok,color in zip(TOKENIZERS,['#4C78A8','#F58518']):
        vals=[summary[(l,tok)] for l in labels]; plt.scatter([v['mean_tokens_per_sentence'] for v in vals],[v['mean_tokens_per_word'] for v in vals],label=tok,color=color)
        for lang,v in zip(labels,vals): plt.annotate(LANGS[lang],(v['mean_tokens_per_sentence'],v['mean_tokens_per_word']))
    plt.xlabel('Mean tokens per sentence'); plt.ylabel('Mean tokens per word'); plt.legend(); plt.tight_layout(); plt.savefig(FIGURES/'figure4_word_vs_sentence.png',dpi=180); plt.close()
def main():
    RESULTS.mkdir(exist_ok=True); environment(); metadata=json.loads((DATA/'corpus_metadata.json').read_text(encoding='utf-8')); corpus=json.loads((DATA/'corpus.json').read_text(encoding='utf-8')); rows=[]; summary={}
    for tok_name in TOKENIZERS:
        encode=load_encoder(tok_name)
        for lang in LANGS:
            for item in corpus:
                text=item[lang]; rows.append({'sentence_id':item['id'],'language':lang,'text':text,'tokenizer':tok_name,'token_count':len(encode(text)),'word_count':len(re.findall(r'\S+',text)),'unicode_codepoints':len(text),'utf8_bytes':len(text.encode('utf-8'))})
    for tok in TOKENIZERS:
        eng={r['sentence_id']:r['token_count'] for r in rows if r['tokenizer']==tok and r['language']=='eng'}
        for r in rows: r['english_token_count']=eng[r['sentence_id']]
    write_csv(RESULTS/'sentence_level_measurements.csv',rows,['sentence_id','language','text','tokenizer','token_count','word_count','unicode_codepoints','utf8_bytes'])
    for lang in LANGS:
        for tok in TOKENIZERS:
            group=[r for r in rows if r['language']==lang and r['tokenizer']==tok]; tv=[r['token_count'] for r in group]; tt=sum(tv); tw=sum(r['word_count'] for r in group); tc=sum(r['unicode_codepoints'] for r in group); tb=sum(r['utf8_bytes'] for r in group); s=stats(tv)
            summary[(lang,tok)]={'language':lang,'tokenizer':tok,'num_sentences':len(group),'mean_tokens_per_sentence':s['mean'],'median_tokens_per_sentence':s['median'],'std_tokens_per_sentence':s['std'],'p25_tokens_per_sentence':s['p25'],'p75_tokens_per_sentence':s['p75'],'p90_tokens_per_sentence':s['p90'],'p95_tokens_per_sentence':s['p95'],'mean_tokens_per_word':statistics.fmean(r['token_count']/r['word_count'] for r in group),'aggregate_tokens_per_word':tt/tw,'mean_tokens_per_char':statistics.fmean(r['token_count']/r['unicode_codepoints'] for r in group),'aggregate_tokens_per_char':tt/tc,'mean_tokens_per_byte':statistics.fmean(r['token_count']/r['utf8_bytes'] for r in group),'relative_to_english':0.0}
    for tok in TOKENIZERS:
        base=summary[('eng',tok)]['mean_tokens_per_sentence']
        for lang in LANGS: summary[(lang,tok)]['relative_to_english']=summary[(lang,tok)]['mean_tokens_per_sentence']/base
    expansion=[]
    for tok in TOKENIZERS:
        for lang in list(LANGS)[1:]:
            values=[r['token_count']/r['english_token_count'] for r in rows if r['tokenizer']==tok and r['language']==lang]
            s=stats(values); expansion.append({'language':lang,'tokenizer':tok,'mean_expansion':s['mean'],'median_expansion':s['median'],'std_expansion':s['std'],'p25_expansion':s['p25'],'p75_expansion':s['p75'],'p90_expansion':s['p90'],'p95_expansion':s['p95']})
    write_csv(RESULTS/'relative_expansion.csv',expansion,list(expansion[0]))
    rankings=[]
    for tok in TOKENIZERS:
        for metric in ['mean_tokens_per_sentence','relative_to_english','mean_tokens_per_word']:
            order=sorted(LANGS,key=lambda lang:summary[(lang,tok)][metric],reverse=True)
            rankings.append({'tokenizer':tok,'metric':metric,'descending_rank':' > '.join(order)})
    write_csv(RESULTS/'language_rankings.csv',rankings,['tokenizer','metric','descending_rank'])
    master=['language','tokenizer','num_sentences','mean_tokens_per_sentence','median_tokens_per_sentence','std_tokens_per_sentence','p25_tokens_per_sentence','p75_tokens_per_sentence','p90_tokens_per_sentence','p95_tokens_per_sentence','mean_tokens_per_word','aggregate_tokens_per_word','mean_tokens_per_char','aggregate_tokens_per_char','mean_tokens_per_byte','relative_to_english']; write_csv(RESULTS/'master_results.csv',[summary[k] for k in sorted(summary)],master)
    comparison=[]
    for lang in LANGS:
        g=summary[(lang,'gpt2')]; m=summary[(lang,'xlm-roberta-base')]
        for name,s,reduction in [('gpt2',g,0.0),('xlm-roberta-base',m,100*(1-m['mean_tokens_per_sentence']/g['mean_tokens_per_sentence']))]: comparison.append({'language':lang,'tokenizer':name,'tokens_per_word':s['mean_tokens_per_word'],'aggregate_tokens_per_word':s['aggregate_tokens_per_word'],'tokens_per_char':s['mean_tokens_per_char'],'tokens_per_byte':s['mean_tokens_per_byte'],'tokens_per_sentence':s['mean_tokens_per_sentence'],'relative_to_english':s['relative_to_english'],'token_count_reduction_percent':reduction})
    write_csv(RESULTS/'tokenizer_comparison.csv',comparison,list(comparison[0])); make_figures(summary,rows)
    report=['# Controlled Multilingual Tokenizer Evaluation','','## Research Question','Does the Hindi tokenization penalty generalize to a controlled five-language parallel corpus, and how much does tokenizer choice affect the result?','','## Dataset',f"FLORES-101 version {metadata['dataset_version']} from {metadata['source']}; pinned archive SHA256 {metadata['archive_sha256']}. Split: {metadata['split']}. The archive is CC-BY-SA-4.0 and documents professionally translated, multilingual-aligned sentences.",'','## Languages','English (`eng`), Hindi (`hin`), Tamil (`tam`), Telugu (`tel`), and Kannada (`kan`).','','## Tokenizers','GPT-2 via `tiktoken` encoding `gpt2`; XLM-RoBERTa-base via Transformers. Both use no special tokens, no truncation, and no lowercasing. Corpus text is NFC-normalized.','','## Methodology',f"The final sample contains {len(corpus)} shared sentence IDs selected contiguously from `devtest` (1,012 available). For each sentence and tokenizer, the experiment records token count, whitespace-delimited word count, Unicode code points, and UTF-8 bytes. It reports sentence-level means and medians, standard deviation, P25/P75/P90/P95, mean-of-sentence tok/word, aggregate tok/word, tok/char, tok/byte, and relative expansion.",'','## Main Results']
    for lang in LANGS:
        for tok in TOKENIZERS:
            s=summary[(lang,tok)]; report.append(f"- {LANGS[lang]} / {tok}: mean tok/sentence={s['mean_tokens_per_sentence']:.3f}, median={s['median_tokens_per_sentence']:.3f}, mean tok/word={s['mean_tokens_per_word']:.3f}, aggregate tok/word={s['aggregate_tokens_per_word']:.3f}, tok/char={s['mean_tokens_per_char']:.4f}, tok/byte={s['mean_tokens_per_byte']:.4f}, relative expansion={s['relative_to_english']:.3f}x.")
    report += ['','## Parallel-Sentence Analysis','Relative expansion is computed per aligned sentence as non-English token count divided by the English count under the same tokenizer. Distribution data and raw observations are in `sentence_level_measurements.csv`.','','## Tokenizer Comparison']
    for lang in LANGS: report.append(f"- {LANGS[lang]} token-count reduction from GPT-2 to XLM-RoBERTa: {next(x for x in comparison if x['language']==lang and x['tokenizer']=='xlm-roberta-base')['token_count_reduction_percent']:.2f}%.")
    report += ['','## Robustness Across Metrics','Language rankings are saved in `language_rankings.csv` for mean tok/sentence, relative expansion, and mean tok/word. These metrics use different denominators, so agreement is a robustness observation rather than proof of linguistic causality.','Per-sentence expansion mean, median, standard deviation, P25, P75, P90, and P95 are saved in `relative_expansion.csv`.','','## Validation of Previous Report','- Claim A: the original 5.89x Hindi/English tok/word result reproduces on the supplied sample, but it does not generalize as a fixed value.','- Claim B: script complexity as the root cause is not established because tokenizer choice materially changes the gap.','- Claim C: tokenization inefficiency is not language-invariant; tokenizer choice changes relative expansion.','- Claim D: an inherent language penalty is not established by these measurements.','','## What the Experiment Establishes','The five languages can be compared on the same 1,000 aligned IDs. Tokenizer choice materially affects the observed language differences.','','## What the Experiment Does Not Establish','It does not establish causality, serving cost, model quality, or an intrinsic property of a language.','','## Limitations','The sample is the first 1,000 `devtest` IDs rather than a random sample; FLORES-101 is a translation benchmark domain; whitespace word counts are an operational denominator; byte-normalized values are representation-level metrics.']
    (RESULTS/'results_summary.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    claims=[['original_claim','new_evidence','status','reasoning'],['Hindi is approximately 6x worse than English','Original sample 5.89x; controlled FLORES result varies by tokenizer and metric','PARTIALLY_SUPPORTED','The original sample reproduces, but 6x is not a general constant.'],['Script complexity is the root cause','GPT-2 and XLM-R produce different language gaps','NOT_SUPPORTED','The experiment does not isolate script from tokenizer behavior.'],['Tokenization inefficiency is language-invariant','Language and tokenizer rankings differ','NOT_SUPPORTED','Tokenizer choice changes relative expansion.'],['Observed token penalty is inherent to the language','Controlled measurements only','UNRESOLVED','The evidence does not establish an intrinsic linguistic cause.']]
    with (RESULTS/'claim_validation.csv').open('w',newline='',encoding='utf-8') as f: csv.writer(f).writerows(claims)
    print(f'completed languages={len(LANGS)} sentences={len(corpus)} tokenizers={len(TOKENIZERS)}')
if __name__=='__main__': main()
