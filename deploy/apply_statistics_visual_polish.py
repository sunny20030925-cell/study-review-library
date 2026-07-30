#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='statistics'
BOOK_VERSION='2026.07.29-2'
CANVA_DESIGN_ID='DAHQ3VXu1eY'
CANVA_EDIT_URL='https://www.canva.com/d/U6gZwMg-Ro4Z3Lg'
VP_ASSET='assets/statistics-svg/data-process.svg'
VP_MARKER='data-vp-asset="statistics-inference-method-selection-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">統計學推論方法選擇地圖</title>
<desc id="desc">統計學考前先辨目標與資料型態，再依一個母數、兩組比較、多組與關聯、設計條件與推論解讀選擇方法。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="180" rx="24" fill="#312e81"/>
<text x="68" y="90" font-size="34" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">統計學｜推論方法選擇地圖</text>
<text x="68" y="138" font-size="20" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#e0e7ff">先辨目標與資料型態 → 判斷設計 → 檢查條件 → 選方法 → 正確解讀</text>
<text x="68" y="180" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#c7d2fe">統計顯著 ≠ 實質重要｜關聯 ≠ 因果｜未拒絕 H₀ ≠ 證明相等</text>

<rect x="42" y="244" width="816" height="230" rx="22" fill="#fff" stroke="#4f46e5" stroke-width="3"/>
<text x="70" y="290" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#3730a3">① 一個母數</text>
<text x="70" y="334" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">平均數：母體 σ 未知通常用 t；σ 已知等特定條件才用 z。</text>
<text x="70" y="372" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">比例 CI：SE 用 p̂；H₀:p=p₀ 的 z 檢定以 p₀ 建立虛無 SE。</text>
<text x="70" y="414" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#4f46e5">先分「估計」或「檢定」，再決定標準誤與參考分配。</text>

<rect x="42" y="504" width="816" height="230" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#115e59">② 兩組比較</text>
<text x="70" y="594" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先辨獨立組或配對；同一人前後不能當成兩個獨立樣本。</text>
<text x="70" y="632" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">兩獨立平均數常用 Welch t；配對資料改分析每對差值。</text>
<text x="70" y="670" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">兩比例：CI 不合併；H₀:p₁=p₂ 的檢定才以 pooled p 建虛無 SE。</text>

<rect x="42" y="764" width="816" height="230" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="810" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 多組・關聯</text>
<text x="70" y="854" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">三組以上平均數 → ANOVA；類別 × 類別 → χ² 獨立性。</text>
<text x="70" y="892" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">數量 × 數量 → 相關／簡單線性迴歸；先檢查線性與離群。</text>
<text x="70" y="930" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">R²=r² 只適用於含截距的簡單線性迴歸。</text>

<rect x="42" y="1024" width="816" height="184" rx="22" fill="#fff" stroke="#be123c" stroke-width="3"/>
<text x="70" y="1070" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9f1239">④ 設計・條件・解讀</text>
<text x="70" y="1114" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">問：隨機抽樣？隨機分派？觀察值獨立？數量資料再看形狀／離群／樣本量；</text>
<text x="70" y="1148" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">比例與 χ² 檢查近似條件／期望次數。p 值是在 H₀ 下，依 H₁ 方向定義</text>
<text x="70" y="1182" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">「同等或更極端」結果的機率；不能解讀成 H₀ 為真的機率。</text>

<rect x="42" y="1226" width="816" height="38" rx="15" fill="#312e81"/>
<text x="450" y="1252" text-anchor="middle" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">方法選對之前，先把資料型態、研究設計、條件與問題方向寫清楚。</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root)
    libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'], expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('statistics content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟統計學推論方法選擇地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="統計學推論方法選擇地圖：依一個母數、兩組、多組與關聯、設計條件選擇推論方法"></a><figcaption>統計學推論方法選擇地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        ch0,n=re.subn(r'<figure><img alt="統計研究從問題、資料、描述到推論的完整流程" loading="lazy" src="assets/statistics-svg/data-process\.svg"/><figcaption>統計研究從問題、資料、描述到推論的完整流程</figcaption></figure>', figure, ch0, count=1)
        if n!=1: raise AssertionError('ch00 data-process figure not found')
        ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p>遇到題目時，可用下列路線縮小方法。</p>)', r'\1'+figure, text, count=1)
        if n!=1: raise AssertionError('appendix-b intro paragraph not found')
        ap.write_text(text,encoding='utf-8'); changed=True
    sp=site/VP_ASSET; target=svg_text()
    if sp.read_text(encoding='utf-8')!=target:
        sp.write_text(target,encoding='utf-8'); changed=True
    visual={'status':'passed','date':'2026-07-30','asset':VP_ASSET,'placement':'ch00 and appendix-b','canvaDesignId':CANVA_DESIGN_ID,'canvaEditUrl':CANVA_EDIT_URL,'tabletReadable':True,'zoomable':True,'offlineCachedViaExistingAssetPath':True}
    if m.get('visualPolish')!=visual:
        m['visualPolish']=visual; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed=True
    if changed:
        targetv=next_version(expected_before); lib['version']=targetv; libp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{targetv}';",sw,count=1)
        if n!=1: raise AssertionError('service worker version marker missing')
        swp.write_text(sw,encoding='utf-8'); return targetv
    return expected_before

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: apply_statistics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
