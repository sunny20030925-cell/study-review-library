#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='macroeconomics'
BOOK_VERSION='2026.07.29-2'
CANVA_DESIGN_ID='DAHQ4eP1njs'
CANVA_EDIT_URL='https://www.canva.com/d/1Mr3R5q87YNMNux'
VP_ASSET='assets/macroeconomics-svg/macro-map.svg'
VP_MARKER='data-vp-asset="macroeconomics-policy-model-direction-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">總體經濟學政策模型選擇與方向判斷地圖</title>
<desc id="desc">先判時間尺度、價格調整與開放程度，再依封閉經濟短期政策、Taylor principle 或開放經濟匯率制度追蹤政策方向。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#0c4a6e"/>
<text x="68" y="88" font-size="30" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">總體經濟學｜政策模型選擇 × 方向判斷地圖</text>
<text x="68" y="136" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#e0f2fe">先判時間尺度／價格調整／開放程度 → 寫模型假設 → 再追政策方向</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bae6fd">百分點 ≠ 百分比｜恆等式 ≠ 行為式 ≠ 均衡條件</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#0284c7" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">① 先判分析框架</text>
<text x="70" y="336" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">長期：成長與供給能力；短期：先問價格／工資是否僵固。</text>
<text x="70" y="374" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">再分名目／實質、存量／流量，並標示內生／外生變數。</text>
<text x="70" y="412" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先確認題目是會計恆等式、行為反應，還是均衡比較靜態。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">同一政策在不同時間尺度與模型下，結論可以不同。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 封閉經濟・短期政策</text>
<text x="70" y="594" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">財政擴張通常推升總需求，但效果受擠出與央行反應影響。</text>
<text x="70" y="632" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">貨幣擴張在正常傳導下壓低利率、推升需求；不是無條件結論。</text>
<text x="70" y="670" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先寫短期固定價格／黏性價格假設，再判 IS–LM／AD–AS 的方向。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">政策方向題：先寫衝擊，再逐市場追傳導鏈。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 通膨・Taylor principle</text>
<text x="70" y="852" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">若實際與預期通膨同步上升，名目政策利率需反應超過 1-for-1，</text>
<text x="70" y="890" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">事前實質政策利率才會上升；這是簡化 Taylor principle 的核心。</text>
<text x="70" y="928" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">名目利率上升 ≠ 實質政策一定變緊；必須同時看預期通膨。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#b45309">利率或通膨由 3% 到 5% 是 +2 個百分點，不是 +2%。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">④ 開放經濟・匯率制度</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CA = S − I；只有忽略國外淨要素所得與淨移轉時才用 CA≈NX。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">e=NT$/US$：臺灣通膨較高 → 相對 PPP 下 e 上升 → 新臺幣傾向貶值。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">標準 Mundell–Fleming／完全資本流動：浮動匯率貨幣政策有效、財政被 NX 抵銷；固定匯率相反。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#0c4a6e"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">考前順序：時間尺度 → 模型 → 假設 → 政策方向 → 單位／報價</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root)
    libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('macroeconomics content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟總體經濟學政策模型選擇與方向判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="總體經濟學政策模型選擇與方向判斷地圖：先判時間尺度、模型假設與開放程度，再追政策方向"></a><figcaption>政策模型選擇 × 方向判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        ch0,n=re.subn(r'<figure><img alt="長期、短期、存量、流量與名目實質的分析地圖" loading="lazy" src="assets/macroeconomics-svg/macro-map\.svg"/><figcaption>長期、短期、存量、流量與名目實質的分析地圖</figcaption></figure>',figure,ch0,count=1)
        if n!=1: raise AssertionError('ch00 macro-map figure not found')
        ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p>第一步辨認題目屬長期成長、短期固定價格、物價調整或開放經濟；第二步列出恆等式、行為式與均衡條件；第三步標示外生變數改變；第四步逐市場追蹤方向；第五步檢查模型條件與單位。</p>)',r'\1'+figure,text,count=1)
        if n!=1: raise AssertionError('appendix-b route paragraph not found')
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_macroeconomics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
