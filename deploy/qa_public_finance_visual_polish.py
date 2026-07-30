#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='public-finance'; VERSION='2026.07.29-2'; ASSET='assets/public-finance-svg/public-finance-map.svg'; MARKER='data-vp-asset="public-finance-mechanism-incidence-welfare-map"'; CANVA='DAHQ4tQIk3M'; CANVA_URL='https://www.canva.com/d/APhMiW3N5hUN-R5'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'public-finance once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==189,'189 search entries'); svgdir=site/'assets/public-finance-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('機制 × 歸宿 × 福利判斷地圖' in ch0,'ch00 caption'); ck('機制 × 歸宿 × 福利判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline')
    tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','財政學｜機制 × 歸宿 × 福利判斷地圖','法定納稅人 ≠ 經濟負擔者','政府支出／稅收 ≠ 社會福利本身','市場失靈・公共財・外部性','Samuelson','MRS','MC','Lindahl','個人化價格','Pigouvian','政府失靈','效率','分配','稅負歸宿・稅收・DWL','法定繳納者不等於經濟歸宿','彈性分攤','小稅／局部近似','完整供需曲線','稅收主要是私人部門到政府的移轉','不是 DWL','DWL 三角形','行政與遵從成本','支出・保險・分配','CBA','social discount rate','PAYG／funded','DB／DC','funded ≠ 個人帳戶','Copayment','coinsurance','教育薪資溢酬','因果生產力效果','最適租稅・地方財政・公債','Ramsey inverse-elasticity rule','own-price elasticity','matching-rate','赤字 flow','債務 stock','(1+g) 分母','Δb≈(r−g)b−ps','stock-flow adjustment','效率 ≠ 公平','移轉 ≠ 資源成本','市場失靈 ≠ 已證明某政策最優']
    for token in tokens: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once')
    retained_ch0=['研究政府如何取得資源','效率與公平','實證分析','規範分析']
    for token in retained_ch0: ck(token in ch0,f'ch00 retained {token}')
    retained_ap=['市場失靈題','租稅題','公共支出與保險題','地方財政與公債題']
    for token in retained_ap: ck(token in ap,f'appendix retained {token}')
    corpus='\n'.join((root/'chapters'/f'ch{i:02d}.html').read_text(encoding='utf-8') for i in range(20))
    corrections=['Lindahl','Social Discount Rate','funded','Copayment','Coinsurance','Signaling','Ramsey','ETI','debt bias','stock-flow adjustment']
    for token in corrections: ck(token.lower() in corpus.lower(),f'correction retained {token}')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'PUBLIC_FINANCE_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=189 figures=20 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_public_finance_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
