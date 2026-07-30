#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='industrial-economics'; VERSION='2026.07.30-2'; ASSET='assets/industrial-economics-svg/io-map.svg'; MARKER='data-vp-asset="industrial-economics-competition-model-policy-map"'; CANVA='DAHQ4ZchcBY'; CANVA_URL='https://www.canva.com/d/jK7472aaPhvbCbV'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'industrial-economics once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==150,'150 search entries'); svgdir=site/'assets/industrial-economics-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix-b marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('競爭機制 × 模型條件 × 政策判斷地圖' in ch0,'ch00 caption'); ck('競爭機制 × 模型條件 × 政策判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline path')
    tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','競爭機制','模型條件','政策判斷','集中度高 ≠ 已證明市場力','市場界定・成本結構','CRn／HHI','需求替代','進入障礙','自然獨占','次可加性','subadditivity','只有一家','反事實','定價・寡占・市場力','MR=MC','Cournot','qᵢ=(a−c−bQ₋ᵢ)/(2b)','Bertrand','Stackelberg','Lerner=(P−MC)/P=1/|ε|','|ε|&gt;1','進入・合謀・垂直策略','折現現值','F_sunk','低價阻嚇','可信威脅','重複互動 ≠ 無條件更易合謀','RPM','效率理由 ≠ 法律上當然合法','差異化・平台・政策','價格歧視福利不能只看總產量','Hotelling','[0,1]','兩側價格結構','跨邊外部性','平行定價 ≠ 已證明合意','推定合意','市場界定 → 競爭機制 → 模型條件 → 反事實 → 福利／政策']
    for token in tokens: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once')
    for token in ['集中度高','SCP','反向因果','產品替代','進入與競爭方式']: ck(token in ch0,f'existing ch00 token {token}')
    for token in ['陌生題先判斷競爭機制','市場界定與市場結構題','Cournot 找數量最佳反應交點','價格歧視先確認市場力量','合謀比較合作、偏離與懲罰現值','平台畫出兩側與跨邊外部性','公平交易委員會最新公開資料','正確反事實']: ck(token in ap,f'appendix token {token}')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'INDUSTRIAL_ECONOMICS_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_industrial_economics_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
