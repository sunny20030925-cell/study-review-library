#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='investments'
BOOK_VERSION='2026.07.30-1'
CANVA_DESIGN_ID='DAHQ22yayGI'
CANVA_EDIT_URL='https://www.canva.com/d/YcSot4oME9FMJ6w'
VP_ASSET='assets/investments-svg/investment-map.svg'
VP_MARKER='data-vp-asset="investments-exam-model-selection-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">投資學考前模型選擇地圖</title>
<desc id="desc">投資學考前先辨題型與口徑，再依報酬風險與投資組合、資產定價與市場效率、估值債券衍生品與績效三條主線選模型並檢查成立條件。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="178" rx="24" fill="#17324d"/>
<text x="68" y="90" font-size="34" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">投資學｜考前模型選擇地圖</text>
<text x="68" y="137" font-size="20" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">先辨題型 → 固定口徑 → 選模型 → 檢查成立條件</text>
<text x="68" y="178" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bfdbfe">模型成立條件 &gt; 公式背誦；高報酬 ≠ 高 α；高 β ≠ 高總風險。</text>

<rect x="42" y="244" width="816" height="284" rx="22" fill="#ffffff" stroke="#2563eb" stroke-width="3"/>
<text x="70" y="290" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e3a8a">① 報酬・風險・投資組合</text>
<text x="70" y="334" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">HPR：單期報酬；多期報酬要用成長因子相乘。</text>
<text x="70" y="372" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">算術平均 ≠ 幾何平均；實質報酬優先用精確 Fisher 關係。</text>
<text x="70" y="410" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">組合風險：共變異數／相關不可漏；多資產用 wᵀΣw。</text>
<text x="70" y="448" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CAL／Sharpe 用總波動；β 衡量系統性風險，不是總風險。</text>
<text x="70" y="492" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">先固定單期／年化、百分比／小數與風險分母，再代公式。</text>

<rect x="42" y="558" width="816" height="246" rx="22" fill="#ffffff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="604" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#115e59">② 資產定價・市場效率</text>
<text x="70" y="648" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CAPM：E[Rᵢ]=R_f+βᵢ(E[R_M]−R_f)；β 對應 SML。</text>
<text x="70" y="686" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">APT：若截距寫 E[Rᵢ]，factor surprise 應採零均值口徑。</text>
<text x="70" y="724" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">EMH 實證有 joint-hypothesis；事件研究用 AR／CAR 配合識別。</text>
<text x="70" y="766" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">α 是相對指定模型／基準的結果，不是「保證套利」標籤。</text>

<rect x="42" y="834" width="816" height="324" rx="22" fill="#ffffff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="880" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 估值・債券・衍生品・績效</text>
<text x="70" y="924" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Gordon：P₀=D₁/(k−g)，先檢查 k&gt;g。</text>
<text x="70" y="962" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">債券價格與殖利率反向；duration 的 Δy 用小數，convexity 尺度一致。</text>
<text x="70" y="1000" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">免疫：value／duration matching 後仍需再平衡；並非永久鎖定。</text>
<text x="70" y="1038" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Forward／put-call parity：只在各自無套利與 carry 條件下成立。</text>
<text x="70" y="1076" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">ETF 可主動或被動；交易架構 ≠ 被動指數化策略。</text>
<text x="70" y="1114" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Sharpe／Jensen α／IR：先辨基準、風險分母、期間與年化口徑。</text>

<rect x="42" y="1186" width="816" height="60" rx="18" fill="#17324d"/>
<text x="450" y="1224" text-anchor="middle" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">最後檢查：單位一致｜條件成立｜預期 ≠ 保證｜模型結論不可過度外推</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root)
    libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('investments content version drift')
    changed=False
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟投資學考前模型選擇地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="投資學考前模型選擇地圖：先辨題型與口徑，再依報酬風險、資產定價、估值債券衍生品與績效選模型並檢查成立條件"></a><figcaption>投資學考前模型選擇地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    if VP_MARKER not in ch0:
        ch0,n=re.subn(r'<figure class="chapter-figure"><img loading="lazy" src="assets/investments-svg/investment-map\.svg" alt="投資決策地圖"><figcaption>投資決策地圖</figcaption></figure>',figure,ch0,count=1)
        if n!=1: raise AssertionError('ch00 investment map figure not found')
        ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p class="lead">.*?</p>)',r'\1'+figure,text,count=1,flags=re.S)
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_investments_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
