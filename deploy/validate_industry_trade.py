#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from collections import Counter
from pathlib import Path

BOOK='industry-trade'; VERSION='2026.07.29-1'; checks=0

def ck(c,msg):
    global checks; checks+=1
    if not c: raise AssertionError(msg)

def main(site_root:str):
    site=Path(site_root); root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in lib['books']]
    expected=os.environ.get('EXPECTED_LIBRARY_VERSION')
    pre_path=os.environ.get('PRE_LIBRARY_JSON')
    ck(m['id']==BOOK and m['version']==q['version']==VERSION,'book identity/version')
    ck(ids.count(BOOK)==1 and ids[-1]==BOOK,'candidate appended once at tail')
    if expected: ck(lib['version']==expected,'final candidate library version')
    if pre_path:
        pre=json.loads(Path(pre_path).read_text(encoding='utf-8')); pre_ids=[b['id'] for b in pre['books']]
        ck(BOOK not in pre_ids,'book absent from deployed base')
        ck(ids==pre_ids+[BOOK],'all existing book ids/order preserved')
    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20 and len(apps)==3,'20 chapters + 3 appendices')
    ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'chapter ids')
    ck(q['count']==len(q['items'])==100,'100 questions')
    ck(len({x['id'] for x in q['items']})==100,'unique question ids')
    ck(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'5 questions/chapter')
    ck(len(s['entries'])==160,'160 search entries')
    ck(Counter(x['chapterId'] for x in s['entries'])=={f'ch{i:02d}':8 for i in range(20)},'8 search entries/chapter')
    for item in q['items']:
        for field in ['id','bookId','chapterId','chapterTitle','topic','difficulty','question','answer','explanation','source']:
            ck(bool(item.get(field)),f'{item.get("id")} missing {field}')
        ck(item['bookId']==BOOK,f'{item["id"]} bookId')
        ck(item['difficulty'] in {'基礎','標準','綜合','挑戰'},f'{item["id"]} difficulty')
    for ch in m['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>700,f'file {ch["id"]}')
        t=p.read_text(encoding='utf-8'); ck('<script' not in t.lower(),f'inline script {ch["id"]}')
        if ch['kind']=='chapter':
            for token in ['本章要解決的問題','白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']:
                ck(token in t,f'{ch["id"]} missing {token}')
    figs=list((site/'assets/industry-trade-svg').glob('*.svg')); ck(len(figs)==20,'20 SVG')
    for f in figs:
        t=f.read_text(encoding='utf-8'); ck('<title' in t and '<desc' in t and 'viewBox=' in t and 'role="img"' in t,f'accessibility {f.name}')
        ck('href="http' not in t and "href='http" not in t,f'no remote href {f.name}')
    sw=(site/'sw.js').read_text(encoding='utf-8')
    if expected: ck(f"study-library-{expected}" in sw,'service worker version')
    for token in ['./books/industry-trade/manifest.json','./books/industry-trade/questions.json','./books/industry-trade/search.json','./books/industry-trade/chapters/ch19.html','./assets/industry-trade-svg/ch19.svg']:
        ck(token in sw,f'sw path {token}')
    corpus='\n'.join((root/x['file']).read_text(encoding='utf-8') for x in m['chapters'])
    required=['Cournot','Bertrand','Stackelberg','產業內貿易','出口固定成本','策略性貿易政策','外國報復','雙重加價','投入封鎖','全球價值鏈','外國直接投資（FDI）','技術授權','正常價值','重大損害','因果關係','平行貿易','多產品廠商','移轉價格','調整成本','知識外溢','Pigouvian','貿易創造','貿易轉向','競爭政策']
    for token in required: ck(token in corpus,f'missing core/precision token {token}')
    forbidden=['關稅一定提高本國福利','出口補貼一定提高本國福利','垂直整合一定提高福利','FDI 就是所有跨境金融投資','自由貿易讓每個人都受益','貿易轉向一定提高福利']
    for token in forbidden: ck(token not in corpus,f'forbidden overstatement {token}')
    print(f'INDUSTRY_TRADE_QA_ROUND1_OK checks={checks} books={len(ids)} chapters=20 appendices=3 questions=100 search=160 figures=20')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/validate_industry_trade.py SITE_ROOT')
    main(sys.argv[1])
