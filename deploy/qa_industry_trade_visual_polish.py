#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='industry-trade'; VERSION='2026.07.29-1'; ASSET='assets/industry-trade-svg/ch00.svg'; MARKER='data-vp-asset="industry-trade-market-crossborder-policy-map"'; CANVA='DAHQ4qrUfLQ'; CANVA_URL='https://www.canva.com/d/0BA4jmK8k64mjPs'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'industry-trade once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==160,'160 search entries'); svgdir=site/'assets/industry-trade-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('市場結構 × 跨境策略 × 政策福利判斷地圖' in ch0,'ch00 caption'); ck('市場結構 × 跨境策略 × 政策福利判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline')
    tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','市場結構 × 跨境策略 × 政策福利判斷地圖','看到「出口／關稅／FDI」≠ 可以直接套方向','市場・競爭機制先固定','完全競爭','獨占','Cournot','Bertrand','Stackelberg','壟斷性競爭','固定成本','每單位貿易成本','沉沒成本','出口・授權・外包・FDI','異質廠商','生產力','出口固定成本門檻','不是所有廠商都會出口','控制權','契約風險','外包總成本','關稅・補貼・反傾銷','CS／PS','政府收入','1-for-1','策略性補貼','利潤移轉','財政成本','外國反應','重大損害','因果關係','價值鏈・整合・最終福利','垂直整合','內部移轉','真實資源成本','貿易創造','貿易轉向','外部性','創新','調整成本','外國報復','政府失靈','市場 → 競爭方式 → 成本結構 → 跨境策略 → 政策楔子 → 福利／外國反應']
    for token in tokens: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once')
    ck('產業及貿易不是把產業經濟學與國際貿易各講一半' in ch0,'ch00 core retained'); ck('本書固定用三層判斷' in ch0,'ch00 route retained'); ck('第一步：辨認市場' in ap,'appendix step1 retained'); ck('第二步：辨認跨境決策' in ap,'appendix step2 retained'); ck('第三步：做福利帳' in ap,'appendix step3 retained'); ck('第四步：寫條件式結論' in ap,'appendix step4 retained'); ck('固定成本與每單位貿易成本分開' in ap,'appendix cost warning retained'); ck('本國內部移轉與真正資源成本分開' in ap,'appendix transfer warning retained'); ck('外國反應、報復、資訊不足與政府失靈' in ap,'appendix response warning retained')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'INDUSTRY_TRADE_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=160 figures=20 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_industry_trade_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
