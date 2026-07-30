#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='international-economics'; VERSION='2026.07.29-2'; ASSET='assets/international-economics-svg/international-map.svg'; MARKER='data-vp-asset="international-economics-trade-fx-welfare-map"'; CANVA='DAHQ4X_5oYU'; CANVA_URL='https://www.canva.com/d/Kn8KqUTKvQn_qh1'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'international-economics once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==144,'144 search entries'); svgdir=site/'assets/international-economics-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix-b marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('貿易模型 × 匯率條件 × 福利判斷地圖' in ch0,'ch00 caption'); ck('貿易模型 × 匯率條件 × 福利判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline path')
    for token in ['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','貿易模型','匯率條件','福利判斷','比較利益 ≠ 絕對利益','Ricardo','特定要素','H–O','Stolper–Samuelson','Rybczynski','2×2','充分就業','要素密集度反轉','政策福利逐項算','CS／PS','政府收入或租金','terms-of-trade','消費者損失 ≠ 社會淨損失','BOP・報價先固定','CA = S − I','BPM7','FA_in','BOP 是流量','IIP 是存量','CIP・PPP・匯率調整','CIP','資本管制','絕對 PPP','CPI 指數','Marshall–Lerner','J curve','遠期匯率 ≠ 未來即期保證預測','模型 → 條件 → 報價／符號 → 均衡方向 → 福利／制度解讀']: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once'); ck('貿易還是金融？' in ch0,'existing ch00 route retained'); ck('五步判題法' in ap,'appendix route retained'); ck('最常見的失分點' in ap,'appendix warning retained'); ck('CPI 指數水準相除求絕對 PPP' in ap,'appendix PPP warning retained')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'INTERNATIONAL_ECONOMICS_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=144 figures=20 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_international_economics_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
