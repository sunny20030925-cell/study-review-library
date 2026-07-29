from __future__ import annotations

import re
from pathlib import Path

# Keep the chapter source human-readable while protecting LaTeX control words from
# Python string-escape parsing. The raw file is data, not an importable module.
raw_path=Path(__file__).with_name('money_banking_content.raw')
source=raw_path.read_text(encoding='utf-8')
source=re.sub(r'\\([A-Za-z]+)',r'\\\\\1',source)
source=source.replace(r'\ ',r'\\ ').replace(r'\$',r'\\$')
namespace={}
exec(compile(source,str(raw_path),'exec'),namespace)
CHAPTERS=namespace['CHAPTERS']

# Validators intentionally reject full incorrect propositions anywhere in the book.
# Phrase traps as diagnoses of the mistake rather than reproducing the bad claim verbatim.
REPHRASE={
    '銀行可以無限制憑空放款。':'把銀行放款誤解成不受任何約束的「憑空放款」。',
    '貨幣乘數在現實中永遠等於 1/rr。':'把 1/rr 誤當成現實世界永遠固定的貨幣乘數。',
    'QE 必然使 M2 等比例增加。':'把 QE 誤解成會讓 M2 無條件等比例增加。',
    '升息必然增加每一家銀行獲利。':'把升息誤解成一定提高所有銀行獲利。',
    '任何匯率上升都代表本幣升值。':'未先固定報價，就把「匯率上升」直接判成升值。',
    '流動性陷阱使所有貨幣政策永久無效。':'把流動性陷阱誤解成所有貨幣政策都永久失效。',
    'Taylor rule 是所有央行依法必須遵守的公式。':'把 Taylor 型規則誤當成所有央行的法定公式。',
    '存款保險可以消除所有銀行風險。':'把存款保險誤解成能消除全部銀行風險。',
}

def rewrite(value):
    if isinstance(value,str):
        for old,new in REPHRASE.items(): value=value.replace(old,new)
        return value
    if isinstance(value,list): return [rewrite(v) for v in value]
    if isinstance(value[0] if isinstance(value,tuple) and value else None,str) and isinstance(value,tuple): return tuple(rewrite(v) for v in value)
    if isinstance(value,tuple): return tuple(rewrite(v) for v in value)
    if isinstance(value,dict): return {k:rewrite(v) for k,v in value.items()}
    return value

CHAPTERS=rewrite(CHAPTERS)
if len(CHAPTERS)!=20 or [c['id'] for c in CHAPTERS] != [f'ch{i:02d}' for i in range(20)]:
    raise AssertionError('money banking chapter source integrity check failed')
