#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
BOOK='civil-law-overview'; VERSION='2026.07.30-2'; ASSET='assets/civil-law-overview-svg/civil-map.svg'; MARKER='data-vp-asset="civil-law-claim-basis-roadmap"'; CANVA='DAHQ2mt-Yds'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'civil law once')
    ck(m['id']==q['bookId']==BOOK,'book id'); ck(m['version']==q['version']==VERSION,'content version'); ck(len([x for x in m['chapters'] if x['kind']=='chapter'])==20,'20 chapters'); ck(len([x for x in m['chapters'] if x['kind']=='appendix'])==3,'3 appendices')
    ck([x['id'] for x in m['chapters']]==[f'ch{i:02d}' for i in range(20)]+['appendix-a','appendix-b','appendix-c'],'chapter ids stable')
    ck(q['count']==len(q['items'])==100,'100 questions'); ck(len({x['id'] for x in q['items']})==100,'unique q ids'); ck(len(s['entries'])==150,'150 search')
    ck([x['id'] for x in q['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)],'question ids stable')
    figs=sorted((site/'assets/civil-law-overview-svg').glob('*.svg')); ck(len(figs)==20,'20 figures')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoom'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline metadata')
    ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); ck(MARKER in ap,'appendix marker'); ck(ap.count(MARKER)==1,'marker once'); ck(ap.count(ASSET)>=2,'appendix link and image'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'zoom link')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ck(ASSET in ch0,'ch00 existing placement')
    svg=(site/ASSET).read_text(encoding='utf-8')
    for tok in ['民法案例題請求權基礎地圖','A 對 B 要什麼','已有契約','不當得利｜§179','無法律上原因受利益','侵權｜§184 常見入口','故意或過失＋不法侵害他人權利','物權｜§767','無權占有／侵奪','請求返還','請求除去','請求防止','親屬／繼承｜特別規則','發生：要件齊嗎','一般請求權原則 15 年','法律另定較短期間者','債權 ≠ 物權','法規時點','viewBox="0 0 900 1220"','<title','<desc']:
        ck(tok in svg,f'svg token {tok}')
    ck('href="http' not in svg and "href='http" not in svg,'no remote svg')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f'study-library-{expected_library}' in sw,'sw version'); ck(f'./{ASSET}' in sw,'asset cached'); ck(sw.count(f'./{ASSET}')==1,'cache once')
    for f in figs:
        t=f.read_text(encoding='utf-8'); ck('<title' in t and '<desc' in t and 'viewBox=' in t,f'accessibility {f.name}')
    print(f'CIVIL_LAW_OVERVIEW_VP_QA_OK checks={checks} books={len(ids)} library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_civil_law_overview_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
