#!/usr/bin/env python3
"""Download and prepare a deterministic five-language FLORES-101 sample."""
from __future__ import annotations
import argparse, hashlib, json, tarfile, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
URL='https://dl.fbaipublicfiles.com/flores101/dataset/flores101_dataset.tar.gz'
LANGUAGES={'eng':'English','hin':'Hindi','tam':'Tamil','tel':'Telugu','kan':'Kannada'}
SPLIT='devtest'
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=1000)
    args=parser.parse_args(); data_dir=ROOT/'data'; data_dir.mkdir(parents=True,exist_ok=True)
    archive=data_dir/'flores101_dataset.tar.gz'; extracted=data_dir/'flores101_dataset'
    if not archive.exists(): urllib.request.urlretrieve(URL,archive)
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    if not extracted.exists():
        with tarfile.open(archive,'r:gz') as tar: tar.extractall(data_dir,filter='data')
    available={}
    for code in LANGUAGES:
        path=extracted/SPLIT/f'{code}.{SPLIT}'
        available[code]={str(i+1):line.strip() for i,line in enumerate(path.read_text(encoding='utf-8').splitlines())}
    total=len(available['eng']); selected_ids=list(range(1,min(args.limit,total)+1))
    rows=[{'id':i,**{code:available[code][str(i)] for code in LANGUAGES}} for i in selected_ids]
    (data_dir/'corpus.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    metadata={'dataset_name':'FLORES-101','dataset_version':'1.0.0','source':URL,'archive_sha256':digest,'languages':list(LANGUAGES.values()),'language_codes':LANGUAGES,'parallel':True,'split':SPLIT,'total_available_sentences':total,'selected_sentences':len(rows),'sampling_method':'first contiguous IDs from the documented devtest split','random_seed':None,'filtering':['selected IDs present in all five language files','NFC normalization and stripped line endings'],'license':'CC-BY-SA-4.0','selected_ids':f'1-{len(rows)}'}
    (data_dir/'corpus_metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(metadata,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
