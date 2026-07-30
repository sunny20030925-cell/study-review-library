#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='international-economics'; BOOK_VERSION='2026.07.29-2'; CANVA_DESIGN_ID='DAHQ4X_5oYU'; CANVA_EDIT_URL='https://www.canva.com/d/Kn8KqUTKvQn_qh1'; VP_ASSET='assets/international-economics-svg/international-map.svg'; VP_MARKER='data-vp-asset="international-economics-trade-fx-welfare-map"'
def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">國際經濟學貿易模型匯率條件與福利判斷地圖</title>
<desc id="desc">先判貿易或金融、小國或大國、短期或長期，固定模型條件與報價，再依貿易模型、政策福利、國際收支或 CIP PPP 與匯率調整判斷方向。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#0c4a6e"/>
<text x="68" y="88" font-size="29" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">國際經濟學｜貿易模型 × 匯率條件 × 福利判斷地圖</text>
<text x="68" y="136" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#e0f2fe">先判貿易／金融、小國／大國、短期／長期 → 固定模型條件與報價 → 才算福利／方向</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bae6fd">比較利益 ≠ 絕對利益｜模型條件不符時不要硬搬定理</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#0284c7" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">① 貿易模型先判條件</text>
<text x="70" y="336" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Ricardo／特定要素／H–O／規模經濟：先選模型，再判相對價格與分配。</text>
<text x="70" y="374" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Stolper–Samuelson／Rybczynski 不是普遍定律；標準方向依 2×2、多樣化生產等條件。</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">還要檢查充分就業、商品價格固定與無要素密集度反轉等相應前提。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">先問模型、再問條件，最後才判價格、產量與所得分配。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 政策福利逐項算</text>
<text x="70" y="594" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">自由貿易 → 國內價格楔子 → CS／PS → 政府收入或租金 → 生產／消費扭曲。</text>
<text x="70" y="632" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">小國出口補貼：政府支出要入福利帳，但不是兩類扭曲外再加第三塊效率損失。</text>
<text x="70" y="670" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">大國可能另有 terms-of-trade；配額租不必然是政府收入。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">消費者損失 ≠ 社會淨損失；福利一定要逐項合併。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ BOP・報價先固定</text>
<text x="70" y="852" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CA = S − I 是會計連結，不代表單向因果；經常帳也不只等於商品貿易。</text>
<text x="70" y="890" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">BPM7 金融帳方向先看定義；本書 FA_in 與官方金融帳平衡項方向相反。</text>
<text x="70" y="928" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">BOP 是流量；IIP 是存量。匯率先寫單位，再判 S 上升代表誰升／貶。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#b45309">沒有固定正負號與報價，就不要直接判「上升＝升值／貶值」。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">④ CIP・PPP・匯率調整</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CIP 需同到期、可比風險，且無足以阻斷套利的交易成本／資本管制。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">絕對 PPP 不能直接拿不同基期 CPI 指數水準相除；先確認可比價格水準。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Marshall–Lerner「彈性和 &gt;1」是標準特例；J curve 非必然；遠期匯率 ≠ 未來即期保證預測。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#0c4a6e"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">考前順序：模型 → 條件 → 報價／符號 → 均衡方向 → 福利／制度解讀</text>
</svg>\n'''
def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('international-economics content version drift')
    changed=False; figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟國際經濟學貿易模型匯率條件與福利判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="國際經濟學貿易模型匯率條件與福利判斷地圖：先判模型條件與報價，再判均衡方向與福利"></a><figcaption>貿易模型 × 匯率條件 × 福利判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        ch0,n=re.subn(r'<figure><img alt="國際經濟學的分析地圖圖解" loading="lazy" src="assets/international-economics-svg/international-map\.svg"/><figcaption>國際經濟學的分析地圖圖解</figcaption></figure>',figure,ch0,count=1)
        if n!=1: raise AssertionError('ch00 international-map figure not found')
        ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2>五步判題法</h2>'
        if anchor not in text: raise AssertionError('appendix-b route heading not found')
        text=text.replace(anchor,figure+anchor,1); ap.write_text(text,encoding='utf-8'); changed=True
    sp=site/VP_ASSET; target=svg_text()
    if sp.read_text(encoding='utf-8')!=target: sp.write_text(target,encoding='utf-8'); changed=True
    visual={'status':'passed','date':'2026-07-30','asset':VP_ASSET,'placement':'ch00 and appendix-b','canvaDesignId':CANVA_DESIGN_ID,'canvaEditUrl':CANVA_EDIT_URL,'tabletReadable':True,'zoomable':True,'offlineCachedViaExistingAssetPath':True}
    if m.get('visualPolish')!=visual: m['visualPolish']=visual; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed=True
    if changed:
        targetv=next_version(expected_before); lib['version']=targetv; libp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{targetv}';",sw,count=1)
        if n!=1: raise AssertionError('service worker version marker missing')
        swp.write_text(sw,encoding='utf-8'); return targetv
    return expected_before
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: apply_international_economics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
