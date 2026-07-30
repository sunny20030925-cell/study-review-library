#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='commercial-law'; VERSION='2026.07.29-2'; ASSET='assets/commercial-law-svg/law-map.svg'; MARKER='data-vp-asset="commercial-law-dual-track-case-map"'; CANVA='DAHQ2c1bRXE'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'commercial law once')
    ck(m['id']==q['bookId']==BOOK,'book id'); ck(m['version']==q['version']==VERSION,'content version'); ck(len([x for x in m['chapters'] if x['kind']=='chapter'])==18,'18 chapters'); ck(len([x for x in m['chapters'] if x['kind']=='appendix'])==3,'3 appendices')
    ck(q['count']==len(q['items'])==90,'90 questions'); ck(len({x['id'] for x in q['items']})==90,'unique q ids'); ck(len(s['entries'])==111,'111 search')
    ck([x['id'] for x in q['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(18) for j in range(1,6)],'question ids stable')
    figs=sorted((site/'assets/commercial-law-svg').glob('*.svg')); ck(len(figs)==18,'18 figures')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoom'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline metadata')
    ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); ck(MARKER in ap,'appendix marker'); ck(ap.count(MARKER)==1,'marker once'); ck(ap.count(ASSET)>=2,'appendix link and image'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'zoom link')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ck(ASSET in ch0,'ch00 existing placement')
    svg=(site/ASSET).read_text(encoding='utf-8');
    for tok in ['商事法案例題雙軌判斷地圖','公司法 §194 vs §214','繼續持股 1 年以上','繼續 6 個月＋持股 1%','30 日不提起','證交法 §157 vs §157-1','6 個月反向交易','實際知悉重大消息','公開後 18 小時','公開發行 ≠ 上市','viewBox="0 0 900 1220"','<title','<desc']:
        ck(tok in svg,f'svg token {tok}')
    ck('href="http' not in svg and "href='http" not in svg,'no remote svg')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f'study-library-{expected_library}' in sw,'sw version'); ck(f'./{ASSET}' in sw,'asset cached'); ck(sw.count(f'./{ASSET}')==1,'cache once')
    for f in figs:
        t=f.read_text(encoding='utf-8'); ck('<title' in t and '<desc' in t and 'viewBox=' in t,f'accessibility {f.name}')
    print(f'COMMERCIAL_LAW_VP_QA_OK checks={checks} books={len(ids)} library={expected_library} chapters=18 appendices=3 questions=90 search=111 figures=18 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_commercial_law_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
