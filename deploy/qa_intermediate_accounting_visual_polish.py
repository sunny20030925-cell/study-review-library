#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='intermediate-accounting'; VERSION='2026.07.29-2'; ASSET='assets/intermediate-accounting-svg/ch00.svg'; MARKER='data-vp-asset="intermediate-accounting-recognition-measurement-presentation-map"'; CANVA='DAHQ41pBkpo'; CANVA_URL='https://www.canva.com/d/RwAvCpLNxeqkcjn'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'intermediate-accounting once'); ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==25,'22 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==25,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(22)),'ch00-ch21'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
    for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
    qs=q.get('items',[]); ck(q.get('count')==110 and len(qs)==110,'110 questions'); qids=[x.get('id') for x in qs]; ck(len(qids)==len(set(qids)),'unique question ids'); ck(all(f'ch{c:02d}-q{n:02d}' in qids for c in range(22) for n in range(1,6)),'stable question ids')
    ss=s.get('entries',[]); ck(len(ss)==145,'145 search entries'); svgdir=site/'assets/intermediate-accounting-svg'; svgs=sorted(svgdir.glob('*.svg')); ck(len(svgs)==22,'22 SVGs')
    for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); svg=(site/ASSET).read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker'); ck(ap.count(MARKER)==1,'appendix marker'); ck(ASSET in ch0,'ch00 asset'); ck(ASSET in ap,'appendix asset'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom'); ck('認列 × 衡量 × 後續處理 × 表達判斷地圖' in ch0,'ch00 caption'); ck('認列 × 衡量 × 後續處理 × 表達判斷地圖' in ap,'appendix caption')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline')
    tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','中級會計學｜認列 × 衡量 × 後續處理 × 表達判斷地圖','定義 ≠ 認列','分類 ≠ 衡量','初始 ≠ 後續','OCI ≠ 必然重分類','認列・分類先固定','契約條件何時必須遵守','報導日後遵守者','約當現金','支應短期現金承諾','自取得日起原始到期約三個月','初始衡量・成本歸屬','除役／復原義務','IAS 2','FVTPL','交易成本發生時列損益','後續衡量・金融工具・租賃','權益 FVOCI','權益內移轉','收回投資成本','SPPI','2026 修正','IFRS 16','不超過 12 個月','不得含購買選擇權','低價值看標的全新時價值','所得稅・除列・表達過渡','IAS 12','單一交易修正','遞延所得稅','電子支付除列修正','特定系統與政策選擇','IFRS 18','國際 2027 生效','臺灣證券發行人 2028','營業損益小計起算','定義 → 認列 → 初始衡量 → 後續衡量 → 分類／表達 → 揭露／過渡']
    for token in tokens: ck(token in svg,f'svg token {token}')
    ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href'); ck('javascript:' not in svg.lower(),'no javascript'); sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(sw.count(ASSET)==1,'cached asset once')
    for token in ['四個固定問題','何時認列','原始衡量是多少','後續衡量與表達如何處理','交易日與報導日','分錄是判斷的結果']:
        ck(token in ch0,f'ch00 retained {token}')
    for token in ['主題地圖','Conceptual Framework','IAS 1','IAS 7','IAS 12','IAS 16','IFRS 9','IFRS 15','IFRS 16','2026 現行修正提醒','IFRS 18 過渡']:
        ck(token in ap,f'appendix retained {token}')
    for p in svgs:
        text=p.read_text(encoding='utf-8'); ck('<svg' in text and ('<title' in text or 'aria-label' in text or 'role="img"' in text),f'accessibility {p.name}')
    print(f'INTERMEDIATE_ACCOUNTING_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=22 appendices=3 questions=110 search=145 figures=22 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_intermediate_accounting_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
