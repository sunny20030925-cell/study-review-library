#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='macroeconomics'; VERSION='2026.07.29-2'; ASSET='assets/macroeconomics-svg/macro-map.svg'; MARKER='data-vp-asset="macroeconomics-policy-model-direction-map"'; CANVA='DAHQ4eP1njs'; CANVA_URL='https://www.canva.com/d/1Mr3R5q87YNMNux'

def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'macroeconomics once')
    ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions')
    qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==143,'143 search entries')
    svgdir=site/'assets/macroeconomics-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix-b marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset')
    ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom')
    ck('政策模型選擇 × 方向判斷地圖' in ch0,'ch00 caption'); ck('政策模型選擇 × 方向判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline path')
    for token in ['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','政策模型選擇','方向判斷','時間尺度','價格調整','開放程度','恆等式','行為式','均衡條件','封閉經濟・短期政策','財政擴張','擠出','央行反應','貨幣擴張','IS–LM','AD–AS','通膨・Taylor principle','1-for-1','實質政策利率','百分點','CA = S − I','CA≈NX','e=NT$/US$','相對 PPP','新臺幣傾向貶值','Mundell–Fleming','浮動匯率','固定匯率','完全資本流動','政策方向','單位／報價']:
        ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version')
    for token in ['長期與短期','恆等式、行為式與均衡條件','百分點、百分比與近似成長率']:
        ck(token in ch0,f'ch00 retained {token}')
    for token in ['第一步辨認題目屬長期成長','百分比、百分點、年化、名目與實質','最後做反例檢查']:
        ck(token in ap,f'appendix retained {token}')
    print(f'MACROECONOMICS_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=143 figures=20 visual_polish=passed')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_macroeconomics_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
