#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='microeconomics'; VERSION='2026.07.29-2'; ASSET='assets/microeconomics-svg/optimization-map.svg'; MARKER='data-vp-asset="microeconomics-model-assumptions-welfare-map"'; CANVA='DAHQ3ai5CFo'; CANVA_URL='https://www.canva.com/d/dd_p4tygf26PGuC'

def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'microeconomics once')
    ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']:
        ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions')
    qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==154,'154 search entries')
    svgdir=site/'assets/microeconomics-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix-b marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset')
    ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom')
    ck('模型選擇 × 成立條件 × 福利判斷地圖' in ch0,'ch00 caption'); ck('模型選擇 × 成立條件 × 福利判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline path')
    for token in ['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','模型選擇','成立條件','福利判斷','消費者最佳化','MRS = pₓ/pᵧ','KKT','局部非飽和','Slutsky','ū=v(p,m)','生產・成本・市場','p = MC','MR = MC','MRP_L = w','風險・福利','vNM expected utility','正仿射轉換','CS 面積','CV／EV','Pareto efficiency','一般均衡・公共財','Walras','p·z(p)=0','Samuelson','ΣMRS = MRT','角點','互補鬆弛','一階條件只是候選解','不要硬套公式','模型 → 條件 → 解法 → 福利解讀']:
        ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version')
    ck('一階條件只是候選解' in ch0,'existing ch00 condition'); ck('速查不是免責條款' in ap,'appendix warning retained'); ck('不取代正文中的成立條件' in ap,'appendix lead retained')
    print(f'MICROECONOMICS_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=154 figures=20 visual_polish=passed')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_microeconomics_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
