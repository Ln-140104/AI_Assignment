#!/usr/bin/env python3
"""Write aligned five-language text files from corpus.json."""
from pathlib import Path
import json
import unicodedata
ROOT=Path(__file__).resolve().parent.parent
if __name__=='__main__':
    data_dir=ROOT/'data'; rows=json.loads((data_dir/'corpus.json').read_text(encoding='utf-8'))
    for code in ['eng','hin','tam','tel','kan']:
        lines = [unicodedata.normalize('NFC', row[code]).strip() for row in rows]
        (data_dir/f'{code}.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'prepared_languages=5\naligned_sentences={len(rows)}')
