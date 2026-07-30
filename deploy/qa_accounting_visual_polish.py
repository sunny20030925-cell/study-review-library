#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='accounting'; VERSION='2026.07.27-2'; ASSET='assets/accounting-svg/accounting-map.svg'; MARKER='data-vp-asset="accounting-transaction-adjustment-statements-cashflow-map"'; CANVA='DAHQ5G-UZ3g'; CANVA_URL='https://www.canva.com/d/__AMHur-jvd7l6c'
def main(site_root:str, expected_library:str)->None:
 site=Path(site_root); root=site/'books'/BOOK; lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'));m=json.loads((root/'manifest.json').read_text(encoding='utf-8'));q=json.loads((root/'questions.json').read_text(encoding='utf-8'));s=json.loads((root/'search.json').read_text(encoding='utf-8'));checks=0
 def ck(c,msg):
  nonlocal checks; checks+=1
  if not c: raise AssertionError(msg)
 ids=[b['id'] for b in lib['books']]; ck(lib['version']==expected_library,'library version');ck(len(ids)==21,'21 books');ck(len(ids)==len(set(ids)),'unique books');ck(ids.count(BOOK)==1,'accounting once');ck(m.get('id')==BOOK,'book id');ck(m.get('version')==VERSION,'content version');ck(len(m.get('chapters',[]))==17,'14 chapters + 3 appendices')
 chapter_ids=[x.get('id') for x in m['chapters']];ck(len(set(chapter_ids))==17,'unique chapter ids');ck(all(f'ch{i:02d}' in chapter_ids for i in range(14)),'ch00-ch13');ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendix ids')
 for item in m['chapters']: ck((root/item['file']).is_file(),f"missing {item['file']}")
 qs=q.get('items',[]);ck(q.get('count')==70 and len(qs)==70,'70 questions');qids=[x.get('id') for x in qs];ck(len(qids)==len(set(qids)),'unique question ids');ck(len(qids)==70,'stable question count');ss=s.get('entries',[]);ck(len(ss)==111,'111 search entries');svgs=sorted((site/'assets/accounting-svg').glob('*.svg'));ck(len(svgs)==13,'13 SVGs')
 for p in svgs: ck(p.is_file() and p.stat().st_size>50,f'bad SVG {p.name}')
 ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8');ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8');svg=(site/ASSET).read_text(encoding='utf-8');ck(ch0.count(MARKER)==1,'ch00 marker');ck(ap.count(MARKER)==1,'appendix marker');ck(ASSET in ch0,'ch00 asset');ck(ASSET in ap,'appendix asset');ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 zoom');ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix zoom');ck('交易 → 調整 → 報表 → 現金流判斷地圖' in ch0,'ch00 caption');ck('交易 → 調整 → 報表 → 現金流判斷地圖' in ap,'appendix caption')
 vp=m.get('visualPolish',{});ck(vp.get('status')=='passed','vp passed');ck(vp.get('asset')==ASSET,'vp asset');ck(vp.get('placement')=='ch00 and appendix-b','placement');ck(vp.get('canvaDesignId')==CANVA,'canva id');ck(vp.get('canvaEditUrl')==CANVA_URL,'canva url');ck(vp.get('tabletReadable') is True,'tablet');ck(vp.get('zoomable') is True,'zoomable');ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline')
 tokens=['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','會計學｜交易 → 調整 → 報表 → 現金流判斷地圖','交易先辨要素','資產＝負債＋權益','收入 ≠ 收現','費用 ≠ 付款','權責基礎','五大要素','借貸與期末調整','資產／費用增加通常記借方','負債／權益／收入增加通常記貸方','本期應認列多少','應計、遞延、折舊','借貸必須同額','存貨與營業資產','淨變現價值（NRV）','折舊是成本分攤','帳面金額','報表與現金流','調整後試算表 → 損益表 → 權益變動 → 資產負債表','營業、投資、籌資','IFRS 18','2026 年所有證券發行人','等式與期間歸屬']
 for t in tokens: ck(t in svg,f'svg token {t}')
 ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'no remote href');ck('javascript:' not in svg.lower(),'no javascript');sw=(site/'sw.js').read_text(encoding='utf-8');ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version');ck(sw.count(ASSET)==1,'cached asset once')
 for t in ['會計在解決什麼問題','權責基礎與現金基礎','五大會計要素','收入與費用','本章理解檢查']: ck(t in ch0,f'ch00 retained {t}')
 for t in ['交易分錄路線','期末調整路線','報表編製路線','考場最後檢查','資產 = 負債 + 權益']: ck(t in ap,f'appendix retained {t}')
 ck('<svg' in svg and '<title' in svg and 'role="img"' in svg,'vp svg accessibility')
 print(f'ACCOUNTING_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=14 appendices=3 questions=70 search=111 figures=13 visual_polish=passed')
if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: qa_accounting_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
 main(sys.argv[1],sys.argv[2])
