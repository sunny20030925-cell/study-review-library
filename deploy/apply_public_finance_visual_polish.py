#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='public-finance'; BOOK_VERSION='2026.07.29-2'; CANVA_DESIGN_ID='DAHQ4tQIk3M'; CANVA_EDIT_URL='https://www.canva.com/d/APhMiW3N5hUN-R5'; VP_ASSET='assets/public-finance-svg/public-finance-map.svg'; VP_MARKER='data-vp-asset="public-finance-mechanism-incidence-welfare-map"'
def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">財政學機制歸宿與福利判斷地圖</title>
<desc id="desc">先辨市場與政府機制，固定邊際條件與制度定義，找經濟歸宿，再分別判斷稅收、資源成本、效率、分配與跨期效果。</desc>
<rect width="900" height="1280" rx="30" fill="#f5f3ff"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#5b21b6"/>
<text x="68" y="88" font-size="30" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">財政學｜機制 × 歸宿 × 福利判斷地圖</text>
<text x="68" y="136" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ede9fe">先辨市場／政府機制 → 固定邊際條件與制度定義 → 找經濟歸宿 → 再算效率、分配與跨期成本</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ddd6fe">法定納稅人 ≠ 經濟負擔者｜政府支出／稅收 ≠ 社會福利本身</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">① 市場失靈・公共財・外部性</text>
<text x="70" y="336" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">公共財：Samuelson 條件看各人 MRS 加總與 MC；Lindahl 是個人化價格／稅負份額。</text>
<text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">外部性：比較私人與社會邊際量，再判 Pigouvian 稅、補貼、規制或公共提供。</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">市場失靈只是介入理由之一；還要比較資訊需求、行政成本與政府失靈。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">先做實證分析，再把效率、分配與價值判斷分開。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 稅負歸宿・稅收・DWL</text>
<text x="70" y="594" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">法定繳納者不等於經濟歸宿；彈性分攤只適用標準競爭市場、小稅／局部近似。</text>
<text x="70" y="632" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">大稅楔或彈性沿曲線改變時，要回完整供需曲線找新均衡。</text>
<text x="70" y="670" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">稅收主要是私人部門到政府的移轉，不是 DWL；DWL 來自被扭曲的邊際交易。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">DWL 三角形需有效率基準與線性／局部近似；行政與遵從成本另算。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 支出・保險・分配</text>
<text x="70" y="852" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">CBA 用社會機會成本與合適 social discount rate，不機械等同政府借款利率。</text>
<text x="70" y="890" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">PAYG／funded 是融資方式；DB／DC 是給付／提撥規則；funded ≠ 個人帳戶。</text>
<text x="70" y="928" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Copayment 是固定額；coinsurance 是比例；教育薪資溢酬 ≠ 全是因果生產力效果。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">制度名詞先固定，觀察到的相關也不能直接當政策因果效果。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#0369a1" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">④ 最適租稅・地方財政・公債</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Ramsey inverse-elasticity rule 是特殊情況；一般問題不能只看 own-price elasticity。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">地方配合款先固定 matching-rate 定義；公債先分赤字 flow 與債務 stock。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">精確債務動態含 (1+g) 分母；最後才用 Δb≈(r−g)b−ps，並留意 stock-flow adjustment。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#5b21b6"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">效率 ≠ 公平｜移轉 ≠ 資源成本｜市場失靈 ≠ 已證明某政策最優</text>
</svg>\n'''
def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('public-finance content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟財政學機制歸宿與福利判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="財政學機制歸宿與福利判斷地圖：先辨機制與制度定義，再找經濟歸宿並判斷效率、分配與跨期效果"></a><figcaption>機制 × 歸宿 × 福利判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        old='<figure class="chapter-figure"><img loading="lazy" src="assets/public-finance-svg/public-finance-map.svg" alt="政策分析三層"><figcaption>政策分析三層</figcaption></figure>'
        if old not in ch0: raise AssertionError('ch00 public-finance-map figure not found')
        ch0=ch0.replace(old,figure,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2 id="市場失靈題">市場失靈題</h2>'
        if anchor not in text: raise AssertionError('appendix-b market failure heading not found')
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_public_finance_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
