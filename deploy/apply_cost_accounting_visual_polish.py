#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='cost-accounting'
BOOK_VERSION='2026.07.29-2'
CANVA_DESIGN_ID='DAHQ5Eq5yIA'
CANVA_EDIT_URL='https://www.canva.com/d/PfgNzm2JtNHRzyX'
VP_ASSET='assets/cost-accounting-svg/cost-map.svg'
VP_MARKER='data-vp-asset="cost-accounting-cost-flow-allocation-eup-variance-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">成本會計學成本流分攤約當產量與差異分析判斷地圖</title>
<desc id="desc">先固定成本流與成本標的，再辨分攤制度與約當產量口徑，最後處理成本數量利潤、差異分析與總額檢核。</desc>
<rect width="900" height="1280" rx="30" fill="#eef6f6"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#0f4c5c"/>
<text x="68" y="88" font-size="29" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">成本會計學｜成本流 × 分攤 × 約當產量 × 差異分析判斷地圖</text>
<text x="68" y="136" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dff5f3">先辨成本如何形成與流動，再固定分攤基礎、數量基準與差異比較點。</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bde9e4">成本標的 → 成本流 → 分攤基礎 → 數量口徑 → 單位成本／差異 → 總額檢核</text>
<rect x="42" y="246" width="816" height="218" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="292" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">① 成本流先固定</text>
<text x="70" y="336" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">直接材料＋直接人工＋製造費用 → 在製品 → 製成品 → 銷貨成本。</text>
<text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">先分成本標的與直接／間接成本，再決定歸集與分攤；分類取決於正在衡量誰。</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">IAS 2 邊界：固定製造費用依正常產能分攤；異常低產量的未分攤部分當期費用化。</text>
<text x="70" y="446" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">先畫流向，再算單位成本。</text>
<rect x="42" y="490" width="816" height="218" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="536" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">② 分攤與成本制度</text>
<text x="70" y="580" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">成本庫 → 分攤基礎 → 分攤率 → 成本標的；分攤率一定先固定分母。</text>
<text x="70" y="618" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">分批成本制看工作單；分步成本制看部門／製程；ABC 先辨作業，再找成本動因。</text>
<text x="70" y="656" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">製造費用多分／少分：比較實際製造費用與已分攤製造費用，再決定期末處理。</text>
<text x="70" y="690" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">制度不同，成本歸集單位就不同。</text>
<rect x="42" y="734" width="816" height="218" rx="22" fill="#fff" stroke="#2563eb" stroke-width="3"/>
<text x="70" y="780" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">③ 分步成本與聯合成本</text>
<text x="70" y="824" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">加權平均法：期初與本期工作合併；FIFO：只計本期完成的工作量。</text>
<text x="70" y="862" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">材料與加工成本完成度可能不同，約當產量與單位成本必須按成本成分分開。</text>
<text x="70" y="900" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">正常／異常損壞分開；聯合成本到分離點為止，分離後可分離成本另算。</text>
<text x="70" y="934" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">先做實體流量，再做 EUP，再做成本分配。</text>
<rect x="42" y="978" width="816" height="198" rx="22" fill="#fff" stroke="#7b2f67" stroke-width="3"/>
<text x="70" y="1024" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7b2f67">④ CVP、差異與損益</text>
<text x="70" y="1068" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">CM＝售價－變動成本；損益兩平量＝固定成本 ÷ 單位 CM，先確認相關範圍與線性假設。</text>
<text x="70" y="1106" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">材料／人工差異先固定 AQ、SQ、AP、SP；標準數量或工時要依實際產出換算。</text>
<text x="70" y="1144" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#17323a">吸收 vs 變動成本法：損益差異來自固定製造費用進出存貨，最後用總額守恆檢核。</text>
<rect x="42" y="1200" width="816" height="46" rx="16" fill="#17323a"/>
<text x="450" y="1230" text-anchor="middle" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">辨題型 → 固定成本流與分母 → 計算 → 判方向 → 回做總額檢核</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('cost-accounting content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟成本會計學成本流分攤約當產量與差異分析判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="成本會計學成本流分攤約當產量與差異分析判斷地圖：成本標的、成本流、分攤、約當產量、差異與總額檢核"></a><figcaption>成本流 × 分攤 × 約當產量 × 差異分析判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        old='<figure><img alt="成本會計的角色與成本語言核心結構圖" loading="lazy" src="assets/cost-accounting-svg/cost-map.svg"/><figcaption>成本會計的角色與成本語言核心結構</figcaption></figure>'
        if old not in ch0: raise AssertionError('ch00 cost-accounting figure not found')
        ch0=ch0.replace(old,figure,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2 id="成本表">成本表題</h2>'
        if anchor not in text: raise AssertionError('appendix-b cost table heading not found')
        text=text.replace(anchor,figure+anchor,1); ap.write_text(text,encoding='utf-8'); changed=True
    sp=site/VP_ASSET; target=svg_text()
    if sp.read_text(encoding='utf-8')!=target: sp.write_text(target,encoding='utf-8'); changed=True
    visual={'status':'passed','date':'2026-07-31','asset':VP_ASSET,'placement':'ch00 and appendix-b','canvaDesignId':CANVA_DESIGN_ID,'canvaEditUrl':CANVA_EDIT_URL,'tabletReadable':True,'zoomable':True,'offlineCachedViaExistingAssetPath':True}
    if m.get('visualPolish')!=visual: m['visualPolish']=visual; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed=True
    if changed:
        targetv=next_version(expected_before); lib['version']=targetv; libp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{targetv}';",sw,count=1)
        if n!=1: raise AssertionError('service worker version marker missing')
        swp.write_text(sw,encoding='utf-8'); return targetv
    return expected_before

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: apply_cost_accounting_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
