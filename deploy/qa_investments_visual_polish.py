#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
BOOK='investments'; VERSION='2026.07.30-1'; ASSET='assets/investments-svg/investment-map.svg'; MARKER='data-vp-asset="investments-exam-model-selection-map"'; CANVA='DAHQ22yayGI'
def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'investments once')
    ck(m['id']==q['bookId']==BOOK,'book id'); ck(m['version']==q['version']==VERSION,'content version'); ck(len([x for x in m['chapters'] if x['kind']=='chapter'])==22,'22 chapters'); ck(len([x for x in m['chapters'] if x['kind']=='appendix'])==3,'3 appendices')
    ck([x['id'] for x in m['chapters']]==[f'ch{i:02d}' for i in range(22)]+['appendix-a','appendix-b','appendix-c'],'chapter ids stable')
    ck(q['count']==len(q['items'])==110,'110 questions'); ck(len({x['id'] for x in q['items']})==110,'unique q ids'); ck(len(s['entries'])==165,'165 search')
    ck([x['id'] for x in q['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(22) for j in range(1,6)],'question ids stable')
    figs=sorted((site/'assets/investments-svg').glob('*.svg')); ck(len(figs)==22,'22 figures')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('canvaEditUrl')=='https://www.canva.com/d/YcSot4oME9FMJ6w','canva url'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoom'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline metadata')
    ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8'); ck(MARKER in ap,'appendix marker'); ck(ap.count(MARKER)==1,'appendix marker once'); ck(ap.count(ASSET)>=2,'appendix link and image'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom link')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ck(MARKER in ch0,'ch00 marker'); ck(ch0.count(MARKER)==1,'ch00 marker once'); ck(ch0.count(ASSET)>=2,'ch00 link and image'); ck('投資學考前模型選擇地圖｜點圖可開啟 SVG 大圖放大閱讀。' in ch0,'ch00 caption'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom link')
    svg=(site/ASSET).read_text(encoding='utf-8')
    for tok in ['投資學｜考前模型選擇地圖','先辨題型 → 固定口徑 → 選模型 → 檢查成立條件','高報酬 ≠ 高 α','高 β ≠ 高總風險','報酬・風險・投資組合','HPR','算術平均 ≠ 幾何平均','Fisher','wᵀΣw','CAL／Sharpe','β 衡量系統性風險','資產定價・市場效率','CAPM','SML','APT','零均值口徑','joint-hypothesis','AR／CAR','估值・債券・衍生品・績效','Gordon','k&gt;g','duration 的 Δy 用小數','convexity','value／duration matching','仍需再平衡','Forward／put-call parity','ETF 可主動或被動','交易架構 ≠ 被動指數化策略','Sharpe／Jensen α／IR','預期 ≠ 保證','viewBox="0 0 900 1280"','<title','<desc']:
        ck(tok in svg,f'svg token {tok}')
    ck('href="http' not in svg and "href='http" not in svg,'no remote svg')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f'study-library-{expected_library}' in sw,'sw version'); ck(f'./{ASSET}' in sw,'asset cached'); ck(sw.count(f'./{ASSET}')==1,'cache once')
    for f in figs:
        t=f.read_text(encoding='utf-8'); ck('<title' in t and '<desc' in t and 'viewBox=' in t,f'accessibility {f.name}')
    print(f'INVESTMENTS_VP_QA_OK checks={checks} books={len(ids)} library={expected_library} chapters=22 appendices=3 questions=110 search=165 figures=22 visual_polish=passed')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_investments_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
