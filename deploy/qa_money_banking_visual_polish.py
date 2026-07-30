#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='money-banking'; VERSION='2026.07.29-2'; ASSET='assets/money-banking-svg/money-map.svg'; MARKER='data-vp-asset="money-banking-creation-policy-rate-fx-map"'; CANVA='DAHQ45LQcmg'; CANVA_URL='https://www.canva.com/d/GPYtOwpOZTmyRuy'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'money-banking once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q if isinstance(q,list) else q.get('items',q.get('questions',[])); ck(len(qs)==100,'100 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(20) for n in range(1,6)),'stable question ids')
    ss=s if isinstance(s,list) else s.get('entries',s.get('items',s.get('search',[]))); ck(len(ss)==150,'150 search entries'); svgdir=site/'assets/money-banking-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==20,'20 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('貨幣創造 × 政策傳導 × 利率匯率方向判斷地圖' in ch0,'ch00 caption'); ck('貨幣創造 × 政策傳導 × 利率匯率方向判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline')
    tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','貨幣銀行學｜貨幣創造 × 政策傳導 × 利率匯率方向判斷地圖','1/rr 只是簡單存款乘數','QE ≠ 財政支出','E=NT$/US$','新臺幣貶值','銀行・準備・貨幣創造','貨幣基數','銀行準備','放款可創造存款','跨行清算','通貨外流','超額準備','資本／流動性','信用需求','資產＝負債＋權益','流動性不足','資不抵債','存款創造 ≠ 無限制乘數','債券・YTM・Duration','票面利率','當期收益率','YTM','持有期間報酬','債券價格與殖利率反向','Duration','convexity','Δy','殖利率曲線反轉','不是衰退的必然定律','中央銀行・政策傳導・QE','準備金制度','貼現窗口','公開市場操作','金融機構轉存款','選擇性信用管理','中央銀行資產負債表政策','M2 固定倍增','最後貸款者','具償付能力','政策工具 → 金融條件','Fisher・通膨・開放經濟','(1+i)=(1+r)(1+πᵉ)','i≈r+πᵉ','Fisher effect','E↑＝新臺幣貶值','名目 ≠ 實質','資產負債表 → 利率／殖利率口徑 → 貨幣創造 → 政策工具 → 傳導 → 通膨／匯率方向']
    for token in tokens: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once')
    for token in ['資金如何移轉、信用如何形成','誰的資產負債表改變','資產＝負債＋權益']:
        ck(token in ch0,f'ch00 retained {token}')
    for token in ['銀行與信用題','放款入帳時分清放款資產與存款負債','債券與利率題','分票面利率、當期收益率、YTM 與持有期間報酬','中央銀行與政策題','QE 分會計效果、金融市場效果與最終支出效果','通膨與開放經濟題','E=NT$/US$；E 上升＝新臺幣貶值','不可能三角']:
        ck(token in ap,f'appendix retained {token}')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'MONEY_BANKING_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_money_banking_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
