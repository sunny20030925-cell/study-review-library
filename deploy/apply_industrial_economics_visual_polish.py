#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='industrial-economics'; BOOK_VERSION='2026.07.30-2'; CANVA_DESIGN_ID='DAHQ4ZchcBY'; CANVA_EDIT_URL='https://www.canva.com/d/jK7472aaPhvbCbV'; VP_ASSET='assets/industrial-economics-svg/io-map.svg'; VP_MARKER='data-vp-asset="industrial-economics-competition-model-policy-map"'
def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">產業經濟學競爭機制模型條件與政策判斷地圖</title>
<desc id="desc">先界定市場與競爭機制，固定模型條件，再用反事實判斷價格、進入、福利與競爭政策。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#4c1d95"/>
<text x="68" y="88" font-size="28" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">產業經濟學｜競爭機制 × 模型條件 × 政策判斷地圖</text>
<text x="68" y="136" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ede9fe">先界定市場與競爭機制 → 固定模型條件 → 再判價格、進入、福利與政策</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ddd6fe">集中度高 ≠ 已證明市場力｜市場定義錯，後面指標全會跟著錯</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">① 市場界定・成本結構</text>
<text x="70" y="336" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先界定產品／地理市場，再看 CRn／HHI、需求替代、進入障礙與容量。</text>
<text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">自然獨占正式判準：相關需求範圍內成本具有次可加性（subadditivity）。</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">「只有一家」是市場結果，不是自然獨占的定義；集中度也只是市場力證據的一部分。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">先問反事實：若價格、品質或進入改變，誰會替代誰？</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 定價・寡占・市場力</text>
<text x="70" y="594" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">獨占先 MR=MC。Cournot：P=a−bQ 時，qᵢ=(a−c−bQ₋ᵢ)/(2b)。</text>
<text x="70" y="632" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Bertrand 先檢查同質、成本與容量；Stackelberg 從跟隨者最佳反應向後歸納。</text>
<text x="70" y="670" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Lerner=(P−MC)/P=1/|ε| 只適用單產品、可微需求、內點利潤最大化。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">正加價內點解位於 |ε|&gt;1；多產品、容量限制或不可微需求不可機械套用。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 進入・合謀・垂直策略</text>
<text x="70" y="852" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">進入要比較未來增量經濟利潤折現現值與不可回收進入成本 F_sunk。</text>
<text x="70" y="890" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">低價阻嚇若不能傳遞資訊、建立承諾或改變進入後報酬，未必是可信威脅。</text>
<text x="70" y="928" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">重複互動 ≠ 無條件更易合謀；要比較合作、偏離與懲罰的現值。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#b45309">RPM 可能有服務效率理由，但效率理由 ≠ 法律上當然合法。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#0369a1" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">④ 差異化・平台・政策</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">價格歧視福利不能只看總產量；銷售配置也會改變總剩餘。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Hotelling 算完 x* 要檢查 [0,1] 與市場覆蓋；平台看兩側價格結構與跨邊外部性。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">聯合行為：平行定價 ≠ 已證明合意；無直接協議也不代表不能依相當依據推定合意。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#4c1d95"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">考前順序：市場界定 → 競爭機制 → 模型條件 → 反事實 → 福利／政策</text>
</svg>\n'''
def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('industrial-economics content version drift')
    changed=False; figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟產業經濟學競爭機制模型條件與政策判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="產業經濟學競爭機制模型條件與政策判斷地圖：先界定市場與模型條件，再判反事實、福利與政策"></a><figcaption>競爭機制 × 模型條件 × 政策判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        old='<figure class="chapter-figure"><img loading="lazy" src="assets/industrial-economics-svg/io-map.svg" alt="產業組織分析地圖"><figcaption>產業組織分析地圖</figcaption></figure>'
        if old not in ch0: raise AssertionError('ch00 io-map figure not found')
        ch0=ch0.replace(old,figure,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2 id="市場結構題">市場界定與市場結構題</h2>'
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_industrial_economics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
