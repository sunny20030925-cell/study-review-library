#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='econometrics'
BOOK_VERSION='2026.07.30-1'
CANVA_DESIGN_ID='DAHQ2ztIet0'
CANVA_EDIT_URL='https://www.canva.com/d/qDaRkhTIyinoAfS'
VP_ASSET='assets/econometrics-svg/econometrics-map.svg'
VP_MARKER='data-vp-asset="econometrics-causal-identification-roadmap"'


def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'


def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1260" role="img" aria-labelledby="title desc">
<title id="title">計量經濟學因果識別方法選擇地圖</title>
<desc id="desc">先分描述預測與因果問題；因果題依研究設計檢查 RCT、FE 或 FD、IV 或 2SLS、DiD、RDD 的核心識別條件與外推限制。</desc>
<rect width="900" height="1260" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="170" rx="24" fill="#0f3d5e"/>
<text x="68" y="88" font-size="34" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">計量經濟學｜因果識別方法選擇地圖</text>
<text x="68" y="132" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">先問目標 → 再找識別來源 → 最後才談估計、推論與外推</text>
<text x="68" y="172" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bfdbfe">估計 ≠ 識別；顯著、高 R²、robust SE 都不能自動把相關變成因果。</text>

<rect x="42" y="236" width="816" height="160" rx="22" fill="#ffffff" stroke="#2563eb" stroke-width="3"/>
<text x="70" y="280" font-size="24" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e3a8a">① 先問目標｜描述／預測，還是因果？</text>
<text x="70" y="324" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">描述／預測：重點是樣本外表現與預測誤差；預測準確不等於因果成立。</text>
<text x="70" y="365" font-size="18" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">因果：先寫 estimand，再說明哪個研究設計與假設能識別它。</text>

<rect x="42" y="426" width="390" height="228" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="68" y="470" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">② RCT｜隨機分派</text>
<text x="68" y="512" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Random assignment 支持樣本內部因果比較。</text>
<text x="68" y="548" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">有 noncompliance：先分 ITT 與實際 treatment。</text>
<text x="68" y="592" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">SATE → PATE 仍需代表性、外部效度或 transportability 條件。</text>

<rect x="468" y="426" width="390" height="228" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="494" y="470" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">③ FE／FD｜Panel</text>
<text x="494" y="512" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">消除 time-invariant αᵢ，不等於自動消除內生性。</text>
<text x="494" y="548" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">標準靜態模型仍需適當 strict exogeneity。</text>
<text x="494" y="592" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">time-varying confounding／lagged outcome 仍可能破壞因果解讀。</text>

<rect x="42" y="686" width="390" height="228" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="68" y="730" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">④ IV／2SLS｜工具變數</text>
<text x="68" y="772" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Relevance：Z 必須能推動 X。</text>
<text x="68" y="808" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Exclusion／exogeneity：Z 不可另一路徑影響 Y。</text>
<text x="68" y="854" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">強 first stage ≠ 工具有效；另檢查 weak instrument 風險。</text>

<rect x="468" y="686" width="390" height="228" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="494" y="730" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">⑤ DiD｜差異中的差異</text>
<text x="494" y="772" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先算兩組 post − pre，再相減。</text>
<text x="494" y="808" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">核心識別條件：parallel trends。</text>
<text x="494" y="854" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">處置前係數不顯著 ≠ 已證明平行趨勢。</text>

<rect x="42" y="946" width="816" height="174" rx="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
<text x="70" y="990" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0c4a6e">⑥ RDD｜Cutoff 附近的局部因果效果</text>
<text x="70" y="1032" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">靠 running variable 在 cutoff 周圍的連續性與局部比較識別跳躍效果。</text>
<text x="70" y="1073" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">估計是 local effect；不能無條件外推到遠離 cutoff 的所有樣本。</text>

<rect x="42" y="1150" width="816" height="72" rx="20" fill="#0f3d5e"/>
<text x="68" y="1180" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">最後檢查：robust SE 修正異質變異下的推論，不修正內生性。</text>
<text x="68" y="1208" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">顯著 ≠ 因果；高 R² ≠ 因果；預測較準 ≠ 因果；先識別，再估計。</text>
</svg>\n'''


def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'], expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('econometrics content version drift')
    changed=False

    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    old='<figure class="chapter-figure"><img loading="lazy" src="assets/econometrics-svg/econometrics-map.svg" alt="計量經濟學工作地圖"><figcaption>計量經濟學工作地圖</figcaption></figure>'
    new='<figure class="chapter-figure"><a href="assets/econometrics-svg/econometrics-map.svg" target="_blank" rel="noopener" aria-label="開啟計量經濟學因果識別方法選擇地圖大圖"><img loading="lazy" src="assets/econometrics-svg/econometrics-map.svg" alt="計量經濟學因果識別方法選擇地圖：先分描述預測與因果，再檢查 RCT、FE 或 FD、IV 或 2SLS、DiD、RDD 的識別條件"></a><figcaption>計量經濟學因果識別方法選擇地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>'
    if old in ch0:
        ch0=ch0.replace(old,new,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    elif '計量經濟學因果識別方法選擇地圖｜點圖可開啟 SVG 大圖放大閱讀。' not in ch0:
        raise AssertionError('ch00 econometrics map figure not found')

    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟計量經濟學因果識別方法選擇地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="計量經濟學因果識別方法選擇地圖：先分描述預測與因果，再依 RCT、FE 或 FD、IV 或 2SLS、DiD、RDD 檢查識別條件"></a><figcaption>因果識別方法選擇地圖｜陌生題先定 estimand 與識別來源；點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p class="lead">.*?</p>)',r'\1'+figure,text,count=1,flags=re.S)
        if n!=1: raise AssertionError('appendix-b lead paragraph not found')
        ap.write_text(text,encoding='utf-8'); changed=True

    sp=site/VP_ASSET; target=svg_text()
    if sp.read_text(encoding='utf-8')!=target: sp.write_text(target,encoding='utf-8'); changed=True
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_econometrics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
