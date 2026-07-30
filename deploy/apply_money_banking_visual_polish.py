#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='money-banking'; BOOK_VERSION='2026.07.29-2'; CANVA_DESIGN_ID='DAHQ45LQcmg'; CANVA_EDIT_URL='https://www.canva.com/d/GPYtOwpOZTmyRuy'; VP_ASSET='assets/money-banking-svg/money-map.svg'; VP_MARKER='data-vp-asset="money-banking-creation-policy-rate-fx-map"'
def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">貨幣銀行學貨幣創造政策傳導與利率匯率方向判斷地圖</title>
<desc id="desc">先辨銀行與中央銀行資產負債表，固定利率、殖利率與匯率報價口徑，再判貨幣創造、債券價格、政策傳導、通膨與匯率方向。</desc>
<rect width="900" height="1280" rx="30" fill="#eff6ff"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#1e3a8a"/>
<text x="68" y="88" font-size="27" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">貨幣銀行學｜貨幣創造 × 政策傳導 × 利率匯率方向判斷地圖</text>
<text x="68" y="136" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">先辨資產負債表與市場 → 固定利率／匯率口徑 → 再判貨幣創造、政策傳導與價格方向</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bfdbfe">1/rr 只是簡單存款乘數｜QE ≠ 財政支出｜E=NT$/US$ 上升＝新臺幣貶值</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#2563eb" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">① 銀行・準備・貨幣創造</text>
<text x="70" y="336" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先分貨幣基數、銀行準備與存款；放款可創造存款，但跨行清算仍需要準備資產。</text>
<text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">1/rr 只在簡化假設下成立；通貨外流、超額準備、資本／流動性與信用需求都會限制擴張。</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">資產＝負債＋權益先守住；擠兌題再分流動性不足與資不抵債。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">存款創造 ≠ 無限制乘數。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 債券・YTM・Duration</text>
<text x="70" y="594" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">票面利率、當期收益率、YTM 與持有期間報酬要分開；債券價格與殖利率反向。</text>
<text x="70" y="632" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">Duration 是小幅殖利率變動的一階近似；變動較大時加入 convexity，並固定 Δy 單位。</text>
<text x="70" y="670" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">殖利率曲線反轉可作資訊訊號，但不是衰退的必然定律。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">先畫 cash flow，再選收益率與價格敏感度工具。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 中央銀行・政策傳導・QE</text>
<text x="70" y="852" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先分準備金制度、貼現窗口、公開市場操作、金融機構轉存款與選擇性信用管理。</text>
<text x="70" y="890" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">QE 是中央銀行資產負債表政策，不等於財政支出；準備金增加也不代表 M2 固定倍增。</text>
<text x="70" y="928" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">最後貸款者核心情境：具償付能力、暫時流動性不足且籌資困難的銀行。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">政策工具 → 金融條件 → 支出／信用／資產價格／匯率 → 總體效果。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">④ Fisher・通膨・開放經濟</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">精確 Fisher：(1+i)=(1+r)(1+πᵉ)；低通膨才用 i≈r+πᵉ，Fisher effect 還需額外假設。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">匯率固定 E=NT$/US$：E↑＝新臺幣貶值；方向題先固定報價，再追利率、資本流動與制度。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">名目 ≠ 實質；匯率升降先看報價；政策方向先寫制度與傳導條件。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#1e3a8a"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">資產負債表 → 利率／殖利率口徑 → 貨幣創造 → 政策工具 → 傳導 → 通膨／匯率方向</text>
</svg>\n'''
def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('money-banking content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟貨幣銀行學貨幣創造政策傳導與利率匯率方向判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="貨幣銀行學貨幣創造政策傳導與利率匯率方向判斷地圖：先辨資產負債表與利率匯率口徑，再判貨幣創造與政策傳導方向"></a><figcaption>貨幣創造 × 政策傳導 × 利率匯率方向判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        old='<figure class="chapter-figure"><img loading="lazy" src="assets/money-banking-svg/money-map.svg" alt="貨幣銀行學四層傳導圖"><figcaption>貨幣銀行學四層傳導圖</figcaption></figure>'
        if old not in ch0: raise AssertionError('ch00 money-map figure not found')
        ch0=ch0.replace(old,figure,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2 id="銀行題">銀行與信用題</h2>'
        if anchor not in text: raise AssertionError('appendix-b banking heading not found')
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_money_banking_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
