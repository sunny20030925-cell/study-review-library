#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='game-theory'
BOOK_VERSION='2026.07.30-2'
CANVA_DESIGN_ID='DAHQ3QeJvMk'
CANVA_EDIT_URL='https://www.canva.com/d/qZaqmF_yGFYibV5'
VP_ASSET='assets/game-theory-svg/game-map.svg'
VP_MARKER='data-vp-asset="game-theory-information-equilibrium-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">賽局理論資訊結構與均衡概念選擇地圖</title>
<desc id="desc">依同時或動態行動、完整或不完全資訊、資訊集合是否單點與是否需要 beliefs，選擇 Nash、mixed Nash、SPNE、BNE 或 PBE。</desc>
<rect width="900" height="1280" rx="30" fill="#f8fafc"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#172554"/>
<text x="68" y="88" font-size="32" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">賽局理論｜資訊結構 × 均衡概念選擇地圖</text>
<text x="68" y="136" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">先問：同時還是動態？資訊完整嗎？資訊集合是否單點？是否需要 beliefs？</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bfdbfe">complete information ≠ perfect information｜BNE ≠ PBE｜mixed Nash 可與 pure Nash 共存</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#2563eb" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">① 同時行動・完整資訊</text>
<text x="70" y="336" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先檢查嚴格支配／反覆刪除，再找純策略 Nash。</text>
<text x="70" y="374" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">需要隨機化時：讓對手在其純策略間無差異 → 解 mixed Nash。</text>
<text x="70" y="418" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">mixed ≠「沒有 pure Nash」；純策略 Nash 與 mixed Nash 可以同時存在。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 動態・perfect information</text>
<text x="70" y="594" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">有限 perfect-information game → backward induction → SPNE。</text>
<text x="70" y="632" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">complete information：payoff／types 等是否共同已知。</text>
<text x="70" y="668" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">perfect information：每個決策資訊集合是否為單點。</text>
<text x="70" y="704" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">普通 backward induction 只直接適用有限 perfect-information game。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ incomplete information・Bayesian</text>
<text x="70" y="852" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">靜態 type game → Bayesian strategy + BNE。</text>
<text x="70" y="890" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">若有動態行動、非單點資訊集合或後續最佳反應：</text>
<text x="70" y="926" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">加入 belief + sequential rationality → 檢查 PBE。</text>
<text x="70" y="962" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#b45309">動態故事不能只算 expected payoff 就結束。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#be123c" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9f1239">④ subgame・belief・off-path</text>
<text x="70" y="1110" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Subgame 起點必須是 singleton information set，且不能切斷任何資訊集合。</text>
<text x="70" y="1144" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">On-path positive-probability beliefs 依 Bayes rule；off-path beliefs 未必唯一，</text>
<text x="70" y="1178" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">但 action 仍須在指定 belief 下 sequentially rational。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#172554"/>
<text x="450" y="1254" text-anchor="middle" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">先辨時序與資訊，再選解概念；均衡之後才談效率、制度與福利。</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root)
    libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'], expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('game-theory content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟賽局理論資訊結構與均衡概念選擇地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="賽局理論資訊結構與均衡概念選擇地圖：依同時或動態行動、資訊結構與 beliefs 選擇 Nash、SPNE、BNE 或 PBE"></a><figcaption>資訊結構 × 均衡概念選擇地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        ch0,n=re.subn(r'<figure class="chapter-figure"><img loading="lazy" src="assets/game-theory-svg/game-map\.svg" alt="賽局分析地圖"><figcaption>賽局分析地圖</figcaption></figure>', figure, ch0, count=1)
        if n!=1: raise AssertionError('ch00 game-map figure not found')
        ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p class="lead">陌生題目先不要猜「答案像哪個經典模型」。按時序、資訊、策略與報酬四步建模，再選解概念。</p>)', r'\1'+figure, text, count=1)
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_game_theory_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
