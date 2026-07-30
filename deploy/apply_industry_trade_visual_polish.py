#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='industry-trade'; BOOK_VERSION='2026.07.29-1'; CANVA_DESIGN_ID='DAHQ4qrUfLQ'; CANVA_EDIT_URL='https://www.canva.com/d/0BA4jmK8k64mjPs'; VP_ASSET='assets/industry-trade-svg/ch00.svg'; VP_MARKER='data-vp-asset="industry-trade-market-crossborder-policy-map"'
def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">產業及貿易市場結構跨境策略與政策福利判斷地圖</title>
<desc id="desc">先判市場與競爭方式，分固定成本與邊際成本，選出口、授權、外包或 FDI 等跨境策略，再追關稅、補貼、反傾銷與整合的福利效果及外國反應。</desc>
<rect width="900" height="1280" rx="30" fill="#fff7ed"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#7c2d12"/>
<text x="68" y="88" font-size="27" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">產業及貿易｜市場結構 × 跨境策略 × 政策福利判斷地圖</text>
<text x="68" y="136" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ffedd5">先判市場與競爭方式 → 分固定／邊際成本 → 選跨境策略 → 再做政策福利帳</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fed7aa">看到「出口／關稅／FDI」≠ 可以直接套方向；先把市場與策略變數固定</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#c2410c" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">① 市場・競爭機制先固定</text>
<text x="70" y="336" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">完全競爭／獨占／Cournot／Bertrand／Stackelberg／壟斷性競爭：先選競爭方式。</text>
<text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">同質或差異化？是否自由進入、存在容量限制、固定成本或垂直關係？</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Cournot、Bertrand、Stackelberg 的策略變數與時序不同，結論不能直接互換。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">固定成本、每單位貿易成本與沉沒成本要分開。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 出口・授權・外包・FDI</text>
<text x="70" y="594" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">異質廠商：先比較生產力與出口固定成本門檻；不是所有廠商都會出口。</text>
<text x="70" y="632" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">出口／授權／外包／FDI：比較固定成本、邊際成本、控制權、契約風險與市場規模。</text>
<text x="70" y="670" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">外包總成本＝生產＋運輸／貿易＋契約成本；FDI 也不是「市場大就一定做」。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">先找誰在做策略選擇，再問成本與控制權如何改變最佳模式。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 關稅・補貼・反傾銷</text>
<text x="70" y="852" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">關稅：追國內價格、數量、CS／PS 與政府收入；不完全競爭下轉嫁不必 1-for-1。</text>
<text x="70" y="890" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">策略性補貼的利潤移轉只在特定寡占假設下成立；還要扣財政成本與外國反應。</text>
<text x="70" y="928" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">反傾銷：價差／傾銷判定之外，仍需重大損害與因果關係；不能只看價格差。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">政策利潤移轉 ≠ 無條件提升本國福利。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#0369a1" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">④ 價值鏈・整合・最終福利</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">垂直整合：區分內部移轉與真實資源成本；供應鏈／平台再看控制權與跨境契約。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">區域整合：同時有貿易創造與貿易轉向；本國內部移轉不等於全部都是資源損失。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">最後加入外部性、創新、調整成本、外國報復與政府失靈；條件改變，福利方向可反轉。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#7c2d12"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">市場 → 競爭方式 → 成本結構 → 跨境策略 → 政策楔子 → 福利／外國反應</text>
</svg>\n'''
def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('industry-trade content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟產業及貿易市場結構跨境策略與政策福利判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="產業及貿易市場結構跨境策略與政策福利判斷地圖：先判競爭方式與成本結構，再選跨境策略並完成政策福利帳"></a><figcaption>市場結構 × 跨境策略 × 政策福利判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        old='<figure class="chapter-figure"><img loading="lazy" src="assets/industry-trade-svg/ch00.svg" alt="產業與貿易的分析地圖結構圖"><figcaption>產業與貿易的分析地圖：從機制到福利的判斷路線</figcaption></figure>'
        if old not in ch0: raise AssertionError('ch00 figure not found')
        ch0=ch0.replace(old,figure,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2>第一步：辨認市場</h2>'
        if anchor not in text: raise AssertionError('appendix-b first step heading not found')
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_industry_trade_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
