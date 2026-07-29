#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
from collections import Counter

BOOK='civil-law-overview'; VERSION='2026.07.29-1'
checks=0

def ck(cond,msg):
    global checks; checks+=1
    if not cond: raise AssertionError(msg)

def main(site_root, expected_library='2026.07.29-18'):
    site=Path(site_root); root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ck(m['id']==q['bookId']==BOOK,'book id')
    ck(m['version']==q['version']==VERSION,'version')
    ck(lib['version']==expected_library,'library version')
    ids=[x['id'] for x in lib['books']]
    ck(len(ids)==13 and ids[-3:]==['public-finance','money-banking',BOOK],'canonical civil tail')
    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'chapter count'); ck(len(apps)==3,'appendix count')
    ck(q['count']==len(q['items'])==100,'question count')
    ck(len(s['entries'])==150,'search count')
    ck(len({x['id'] for x in q['items']})==100,'unique qids')
    ck(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions each')
    ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'chapter ids')
    for ch in m['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>500,f'chapter file {ch["id"]}')
        text=p.read_text(encoding='utf-8'); ck('<script' not in text.lower(),f'no inline script {ch["id"]}')
    figs=sorted((site/'assets/civil-law-overview-svg').glob('*.svg')); ck(len(figs)==20,'figure count')
    for p in figs:
        x=p.read_text(encoding='utf-8'); ck('<title' in x and '<desc' in x and 'viewBox=' in x,f'figure a11y {p.name}'); ck('href="http' not in x and "href='http" not in x,f'no remote figure {p.name}')
    corpus='\n'.join((root/x['file']).read_text(encoding='utf-8') for x in m['chapters'])
    required=[
      '滿 18 歲為成年','未滿 7 歲','純獲法律上利益','效力未定','通謀虛偽意思表示','發現詐欺','逾十年不得撤銷',
      '15 年','定期給付','無因管理','不當得利','給付遲延','不完全給付','所失利益','定型化契約','顯失公平',
      '危險移轉','通知後 6 個月','交付後 5 年','週年利率超過 16%','民法第 184 條','2 年','10 年',
      '非經登記不生效力','民法第 166-1 條','施行日期尚未另定','共有人過半數','逾三分之二','抵押權','善意受讓',
      '租用基地建築房屋','未滿 18 歲不得結婚','二人以上證人','戶政機關','司法院釋字第七四八號解釋施行法','婚生推定','非婚生子女經生父認領',
      '直系血親卑親屬','兄弟姊妹','三個月內','以書面向法院','未滿 16 歲不得為遺囑','特留分'
    ]
    compact=' '.join(corpus.split())
    for token in required: ck(token in compact,f'missing legal token {token}')
    forbidden=[
      '滿二十歲為成年','男未滿十八歲，女未滿十六歲','未成年人已結婚者，有行為能力','禁治產人，無行為能力',
      '第 166-1 條已施行','不動產負擔契約一律必須公證才有效','拋棄繼承就由子女代位','配偶一律先拿二分之一'
    ]
    for token in forbidden: ck(token not in compact,f'forbidden stale law {token}')
    sw=(site/'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw,'sw version')
    for token in ['./books/civil-law-overview/manifest.json','./books/civil-law-overview/questions.json','./books/civil-law-overview/search.json','./books/civil-law-overview/chapters/ch19.html','./assets/civil-law-overview-svg/inheritance-will.svg']:
        ck(token in sw,f'sw path {token}')
    ck(m['releaseNotes'][0]['version']==VERSION,'release version')
    ck('新增一般大學民法概要教材'==m['releaseNotes'][0]['title'],'release title')
    print(f'CIVIL_LAW_OVERVIEW_QA1_OK checks={checks} books={len(ids)} library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20')

if __name__=='__main__':
    if len(sys.argv) not in (2,3): raise SystemExit('usage: python deploy/validate_civil_law_overview.py SITE_ROOT [EXPECTED_LIBRARY]')
    main(sys.argv[1],sys.argv[2] if len(sys.argv)==3 else '2026.07.29-18')
