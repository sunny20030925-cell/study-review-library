#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='commercial-law'
BOOK_VERSION='2026.07.29-2'
CANVA_DESIGN_ID='DAHQ2c1bRXE'
CANVA_EDIT_URL='https://www.canva.com/d/tW8J87KlNJIiXkN'
VP_ASSET='assets/commercial-law-svg/law-map.svg'
VP_MARKER='data-vp-asset="commercial-law-dual-track-case-map"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1220" role="img" aria-labelledby="title desc">
<title id="title">商事法案例題雙軌判斷地圖</title>
<desc id="desc">先辨主體與行為，再沿公司法或證券交易法雙軌分析；特別比較公司法第194條與第214條，以及證券交易法第157條與第157條之1。</desc>
<rect width="900" height="1220" rx="30" fill="#fff7ed"/>
<rect x="34" y="34" width="832" height="176" rx="24" fill="#7c2d12"/>
<text x="68" y="91" font-size="35" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">商事法案例題雙軌判斷地圖</text>
<text x="68" y="136" font-size="20" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ffedd5">公司法 × 證券交易法｜先辨主體與行為，再拆要件與法律效果</text>
<text x="68" y="177" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fed7aa">主體／公司型態 → 行為分類 → 身分・比例・期間・程序／消息 → 法律效果</text>

<rect x="42" y="244" width="816" height="386" rx="22" fill="#ffffff" stroke="#b45309" stroke-width="3"/>
<rect x="42" y="244" width="816" height="62" rx="22" fill="#ffedd5"/>
<text x="70" y="286" font-size="26" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7c2d12">① 公司法｜組織・權限・董事責任・股東救濟</text>
<text x="70" y="347" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#431407">權限機關 → 召集／表決 → 利益衝突 → 義務違反 → 救濟</text>
<text x="70" y="394" font-size="21" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">別混：公司法 §194 vs §214</text>
<text x="82" y="439" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">§194：董事會決議違反法令或章程；繼續持股 1 年以上 → 得請求董事會停止其行為。</text>
<text x="82" y="484" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">§214：繼續 6 個月＋持股 1% → 先書面請監察人為公司起訴。</text>
<text x="82" y="525" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">30 日不提起 → 股東得為公司起訴。</text>
<text x="82" y="570" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7c2d12">代表訴訟是替公司主張，不是股東替自己求償。</text>

<rect x="42" y="660" width="816" height="370" rx="22" fill="#ffffff" stroke="#c2410c" stroke-width="3"/>
<rect x="42" y="660" width="816" height="62" rx="22" fill="#fff1e6"/>
<text x="70" y="702" font-size="26" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">② 證交法｜募集發行・揭露・公司治理・市場交易</text>
<text x="70" y="762" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#431407">證券／公開發行身分 → 行為類型 → 主體 → 期間／消息／意圖 → 法律效果</text>
<text x="70" y="809" font-size="21" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">別混：證交法 §157 vs §157-1</text>
<text x="82" y="855" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">§157 短線交易：法定內部人＋6 個月反向交易＋有利益 → 利益歸公司。</text>
<text x="82" y="896" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">不以「實際知悉重大消息」為構成要件。</text>
<text x="82" y="941" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">§157-1 內線交易：法定主體實際知悉重大消息；消息明確後，</text>
<text x="82" y="982" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">未公開前或公開後 18 小時內交易受規範證券 → 禁止。</text>

<rect x="42" y="1062" width="816" height="116" rx="20" fill="#ffedd5" stroke="#b45309" stroke-width="2"/>
<text x="68" y="1103" font-size="21" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7c2d12">③ 考試作答順序</text>
<text x="68" y="1142" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#431407">定性主體／制度 → 列條文與要件 → 涵攝事實 → 畫時間軸／比例門檻 → 分開寫法律效果</text>
<text x="68" y="1170" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">公開發行 ≠ 上市；同一事實可能同時觸發公司法與證交法，需分層分析。</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'], expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('commercial-law content version drift')
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8'); changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟商事法案例題雙軌判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="商事法案例題雙軌判斷地圖：公司法與證券交易法雙軌，並比較公司法194與214、證交法157與157-1"></a><figcaption>商事法案例題雙軌判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    if VP_MARKER not in text:
        text,n=re.subn(r'(<p>案例題解題路線.*?</p>)',r'\1'+figure,text,count=1,flags=re.S)
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_commercial_law_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
