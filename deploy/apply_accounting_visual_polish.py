#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='accounting'; BOOK_VERSION='2026.07.27-2'; CANVA_DESIGN_ID='DAHQ5G-UZ3g'; CANVA_EDIT_URL='https://www.canva.com/d/__AMHur-jvd7l6c'; VP_ASSET='assets/accounting-svg/accounting-map.svg'; VP_MARKER='data-vp-asset="accounting-transaction-adjustment-statements-cashflow-map"'
def next_version(v:str)->str:
 m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
 if not m: raise AssertionError(f'invalid library version: {v}')
 return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
 return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">會計學交易調整報表與現金流判斷地圖</title><desc id="desc">由交易辨認五大要素與借貸方向，經期末調整連到報表與現金流分類，最後用會計等式檢核。</desc>
<rect width="900" height="1280" rx="30" fill="#eef8f5"/><rect x="34" y="34" width="832" height="184" rx="24" fill="#0f766e"/>
<text x="68" y="88" font-size="30" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">會計學｜交易 → 調整 → 報表 → 現金流判斷地圖</text>
<text x="68" y="136" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#d9faf2">先辨交易影響與期間歸屬，再決定借貸、調整與報表位置；不要從背分錄開始。</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bff4e7">交易 → 五大要素 → 借貸 → 期末調整 → 報表串接 → 現金流 → 等式檢核</text>
<rect x="42" y="246" width="816" height="218" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/><text x="70" y="292" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">① 交易先辨要素</text>
<text x="70" y="336" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">資產＝負債＋權益；每筆交易至少保持會計等式平衡。</text><text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">收入 ≠ 收現；費用 ≠ 付款。權責基礎先看是否已賺得／已耗用。</text><text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">提款／股利不是費用；業主投入不是收入。先辨五大要素再碰借貸。</text><text x="70" y="446" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">先判經濟實質，再記帳。</text>
<rect x="42" y="490" width="816" height="218" rx="22" fill="#fff" stroke="#2563eb" stroke-width="3"/><text x="70" y="536" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">② 借貸與期末調整</text>
<text x="70" y="580" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">資產／費用增加通常記借方；負債／權益／收入增加通常記貸方。</text><text x="70" y="618" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">調整先問：本期應認列多少？期末應留下多少資產或負債？</text><text x="70" y="656" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">應計、遞延、折舊等期末調整通常不直接動現金；完成後借貸必須同額。</text><text x="70" y="690" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">科目類別決定方向，不靠分錄口訣硬背。</text>
<rect x="42" y="734" width="816" height="218" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/><text x="70" y="780" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 存貨與營業資產</text>
<text x="70" y="824" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">存貨先辨可計入成本項目，再比較成本與淨變現價值（NRV）。</text><text x="70" y="862" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">折舊是成本分攤，不等於資產市價下跌；應收款與抵減科目也要分開。</text><text x="70" y="900" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">處分營業資產：先算帳面金額，再與處分價款比較損益。</text><text x="70" y="934" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">衡量題先固定成本與帳面金額口徑。</text>
<rect x="42" y="978" width="816" height="198" rx="22" fill="#fff" stroke="#7b2f67" stroke-width="3"/><text x="70" y="1024" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7b2f67">④ 報表與現金流</text>
<text x="70" y="1068" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">調整後試算表 → 損益表 → 權益變動 → 資產負債表；淨利不等於現金增減。</text><text x="70" y="1106" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">現金流量表另分營業、投資、籌資；分類前先問現金為何改變。</text><text x="70" y="1144" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17343a">IFRS 18 臺灣適用仍有過渡時程，不可誤當 2026 年所有證券發行人已全面適用。</text>
<rect x="42" y="1200" width="816" height="46" rx="16" fill="#17343a"/><text x="450" y="1230" text-anchor="middle" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">交易 → 調整 → 報表 → 現金流；每一步都回到等式與期間歸屬</text></svg>\n'''
def apply(site_root:str, expected_before:str)->str:
 site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
 if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
 root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
 if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('accounting content version drift')
 changed=False
 figure=f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟會計學交易調整報表與現金流判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="會計學交易調整報表與現金流判斷地圖：五大要素、借貸、期末調整、報表與現金流"></a><figcaption>交易 → 調整 → 報表 → 現金流判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>'
 ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
 if VP_MARKER not in ch0:
  old='<figure><img alt="交易經過記錄與分類，最後成為可判斷的財務資訊" loading="lazy" src="assets/accounting-svg/accounting-map.svg"/><figcaption>交易經過記錄與分類，最後成為可判斷的財務資訊</figcaption></figure>'
  if old not in ch0: raise AssertionError('ch00 accounting figure not found')
  ch0p.write_text(ch0.replace(old,figure,1),encoding='utf-8'); changed=True
 ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
 if VP_MARKER not in text:
  anchor='<h2>交易分錄路線</h2>'
  if anchor not in text: raise AssertionError('appendix-b transaction route heading not found')
  ap.write_text(text.replace(anchor,figure+anchor,1),encoding='utf-8'); changed=True
 sp=site/VP_ASSET; target=svg_text()
 if sp.read_text(encoding='utf-8')!=target: sp.write_text(target,encoding='utf-8'); changed=True
 visual={'status':'passed','date':'2026-07-31','asset':VP_ASSET,'placement':'ch00 and appendix-b','canvaDesignId':CANVA_DESIGN_ID,'canvaEditUrl':CANVA_EDIT_URL,'tabletReadable':True,'zoomable':True,'offlineCachedViaExistingAssetPath':True}
 if m.get('visualPolish')!=visual: m['visualPolish']=visual; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed=True
 if changed:
  targetv=next_version(expected_before); lib['version']=targetv; libp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{targetv}';",sw,count=1)
  if n!=1: raise AssertionError('service worker version marker missing')
  swp.write_text(sw,encoding='utf-8'); return targetv
 return expected_before
if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: apply_accounting_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
 print(apply(sys.argv[1],sys.argv[2]))
