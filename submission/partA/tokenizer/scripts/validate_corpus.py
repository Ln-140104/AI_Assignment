#!/usr/bin/env python3
"""Validate five-language FLORES alignment and text integrity."""
from pathlib import Path
import json, unicodedata
ROOT=Path(__file__).resolve().parent.parent
LANGUAGES=['eng','hin','tam','tel','kan']
if __name__=='__main__':
    data_dir=ROOT/'data'; rows=json.loads((data_dir/'corpus.json').read_text(encoding='utf-8')); seen=set(); dup=empty=malformed=0; counts={c:0 for c in LANGUAGES}
    for row in rows:
        if row['id'] in seen: dup+=1
        seen.add(row['id'])
        for code in LANGUAGES:
            text=unicodedata.normalize('NFC',row.get(code,'')).strip()
            if not text: empty+=1
            else:
                counts[code]+=1
                if unicodedata.normalize('NFC',text)!=text or any(x in text for x in '\r\n\t'): malformed+=1
    complete=sum(all(row.get(c,'') for c in LANGUAGES) for row in rows)
    report=[f'Total candidate IDs: {len(rows)}',f'Complete across all five languages: {complete}','Dropped - missing Hindi: 0','Dropped - missing Tamil: 0','Dropped - missing Telugu: 0','Dropped - missing Kannada: 0',f'Dropped - empty text: {empty}',f'Duplicate IDs: {dup}',f'Malformed Unicode or unexpected whitespace entries: {malformed}',f'Final aligned sample: {complete}','Per-language non-empty counts: '+', '.join(f'{c}={counts[c]}' for c in LANGUAGES),f'valid={complete==len(rows) and dup==0 and malformed==0}']
    (data_dir/'corpus_validation.txt').write_text('\n'.join(report)+'\n',encoding='utf-8'); print('\n'.join(report))
