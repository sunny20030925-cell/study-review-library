#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='cost-accounting'; VERSION='2026.07.29-2'; ASSET='assets/cost-accounting-svg/cost-map.svg'; MARKER='data-vp-asset="cost-accounting-cost-flow-allocation-eup-variance-map"'; CANVA='DAHQ5Eq5yIA'; CANVA_URL='https://www.canva.com/d/PfgNzm2JtNHRzyX'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'cost-accounting once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==22,'19 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==22,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(19)),'ch00-ch18'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q.get('items',[]); ck(q.get('count')==95 and len(qs)==95,'95 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(len(qids)==95,'stable question count')
    ss=s.get('entries',[]); ck(len(ss)==150,'150 search entries'); svgdir=site/'assets/cost-accounting-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==19,'19 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('成本流 × 分攤 × 約當產量 × 差異分析判斷地圖' in ch0,'ch00 caption'); ck('成本流 × 分攤 × 約當產量 × 差異分析判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline')
    tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','成本會計學｜成本流 × 分攤 × 約當產量 × 差異分析判斷地圖','成本流先固定','直接材料＋直接人工＋製造費用','在製品 → 製成品 → 銷貨成本','成本標的','IAS 2','正常產能','異常低產量','當期費用化','分攤與成本制度','成本庫 → 分攤基礎 → 分攤率 → 成本標的','分批成本制','分步成本制','ABC','成本動因','製造費用多分／少分','分步成本與聯合成本','加權平均法','FIFO','材料與加工成本完成度','約當產量','正常／異常損壞','聯合成本','分離點','EUP','CVP、差異與損益','CM＝售價－變動成本','損益兩平量＝固定成本 ÷ 單位 CM','相關範圍與線性假設','AQ、SQ、AP、SP','實際產出','吸收 vs 變動成本法','固定製造費用進出存貨','總額守恆','辨題型 → 固定成本流與分母 → 計算 → 判方向 → 回做總額檢核']
    for token in tokens: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once')
    for token in ['成本標的','直接成本與間接成本','產品成本與期間成本','主要成本與加工成本','考題方法與常見錯誤']:
        ck(token in ch0,f'ch00 retained {token}')
    for token in ['成本表題','分批題','分步題','差異題','最後 30 秒','總成本守恆']:
        ck(token in ap,f'appendix retained {token}')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'COST_ACCOUNTING_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=19 appendices=3 questions=95 search=150 figures=19 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_cost_accounting_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
