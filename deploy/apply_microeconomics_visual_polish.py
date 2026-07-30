#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='microeconomics'
BOOK_VERSION='2026.07.29-2'
CANVA_DESIGN_ID='DAHQ3ai5CFo'
CANVA_EDIT_URL='https://www.canva.com/d/dd_p4tygf26PGuC'
VP_ASSET='assets/microeconomics-svg/optimization-map.svg'
VP_MARKER='data-vp-asset="microeconomics-model-assumptions-welfare-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">個體經濟學模型選擇成立條件與福利判斷地圖</title>
<desc id="desc">先寫目標與限制，判斷內點或角點並檢查模型假設，再選擇消費者、生產市場、風險福利或一般均衡公共財的公式與福利結論。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#0c4a6e"/>
<text x="68" y="88" font-size="30" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">個體經濟學｜模型選擇 × 成立條件 × 福利判斷地圖</text>
<text x="68" y="136" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#e0f2fe">先寫目標與限制 → 判斷內點／角點 → 檢查模型假設 → 才套公式與福利結論</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bae6fd">一階條件只是候選解｜條件不符時先回模型，不要硬套公式</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#0284c7" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">① 消費者最佳化</text>
<text x="70" y="336" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先寫 max u(x) 與預算；MRS = pₓ/pᵧ 只適用平滑內點。</text>
<text x="70" y="374" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">角點、不可微或不等式限制 → 檢查 KKT／邊界，不把切線條件當答案。</text>
<text x="70" y="412" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">局部非飽和下才通常用盡預算；Slutsky 的 Hicksian 導數評估於 ū=v(p,m)。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">預算用盡、MRS=價格比都不是無條件定理。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 生產・成本・市場</text>
<text x="70" y="594" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">成本最小／利潤最大先確認產量可行、投入價格、內點／可微與技術條件。</text>
<text x="70" y="632" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">競爭廠商標準內點：p = MC；獨占標準內點：MR = MC。</text>
<text x="70" y="670" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">MRP_L = w 需產品價格與其他投入固定，且廠商是工資接受者。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">市場結構不同，最適條件也不同；不要把 p=MC 到處套。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 風險・福利</text>
<text x="70" y="852" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">vNM expected utility：只有正仿射轉換保留同一風險偏好與期望效用排序。</text>
<text x="70" y="890" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">一般序數效用的任意遞增轉換，不能直接搬進風險模型。</text>
<text x="70" y="928" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CS 面積作精確貨幣福利衡量需準線性／無所得效果；一般情況優先 CV／EV。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#b45309">完全競爭常講 Pareto efficiency，不是無條件 CS + PS 最大化。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">④ 一般均衡・公共財</text>
<text x="70" y="1110" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Walras：p·z(p)=0 需個別預算等式／局部非飽和與利潤分配等前提。</text>
<text x="70" y="1146" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Samuelson：ΣMRS = MRT 限平滑內點最適；角點改用不等式與互補鬆弛。</text>
<text x="70" y="1182" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">先確認均衡／效率定理的偏好、技術與市場前提，再做福利解讀。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#0c4a6e"/>
<text x="450" y="1254" text-anchor="middle" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">考前順序：模型 → 條件 → 解法 → 福利解讀</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root)
    libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('microeconomics content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟個體經濟學模型選擇成立條件與福利判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="個體經濟學模型選擇成立條件與福利判斷地圖：先判目標限制、內點角點與模型假設，再選公式與福利結論"></a><figcaption>模型選擇 × 成立條件 × 福利判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        ch0,n=re.subn(r'<figure><img alt="限制、目標與最適條件的基本結構" loading="lazy" src="assets/microeconomics-svg/optimization-map\.svg"/><figcaption>限制、目標與最適條件的基本結構</figcaption></figure>',figure,ch0,count=1)
        if n!=1: raise AssertionError('ch00 optimization-map figure not found')
        ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p>以下是高頻公式與定理的速查表。它用來複習，不取代正文中的成立條件。</p>)',r'\1'+figure,text,count=1)
        if n!=1: raise AssertionError('appendix-b lead paragraph not found')
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_microeconomics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
