#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='intermediate-accounting'; BOOK_VERSION='2026.07.29-2'; CANVA_DESIGN_ID='DAHQ41pBkpo'; CANVA_EDIT_URL='https://www.canva.com/d/RwAvCpLNxeqkcjn'; VP_ASSET='assets/intermediate-accounting-svg/ch00.svg'; VP_MARKER='data-vp-asset="intermediate-accounting-recognition-measurement-presentation-map"'
def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'
def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1280" role="img" aria-labelledby="title desc">
<title id="title">中級會計學認列衡量後續處理與表達判斷地圖</title>
<desc id="desc">先辨定義與認列，再固定初始衡量，判後續處理，最後完成分類表達、揭露與準則過渡。</desc>
<rect width="900" height="1280" rx="30" fill="#f0f9ff"/>
<rect x="34" y="34" width="832" height="184" rx="24" fill="#075985"/>
<text x="68" y="88" font-size="28" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">中級會計學｜認列 × 衡量 × 後續處理 × 表達判斷地圖</text>
<text x="68" y="136" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#e0f2fe">先辨定義與認列 → 固定初始衡量 → 判後續處理 → 最後做表達、揭露與過渡</text>
<text x="68" y="178" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bae6fd">定義 ≠ 認列｜分類 ≠ 衡量｜初始 ≠ 後續｜OCI ≠ 必然重分類</text>
<rect x="42" y="246" width="816" height="228" rx="22" fill="#fff" stroke="#0284c7" stroke-width="3"/>
<text x="70" y="292" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">① 認列・分類先固定</text>
<text x="70" y="336" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">先問是否符合資產／負債等定義，再判何時認列；定義本身不等於固定認列門檻。</text>
<text x="70" y="374" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">負債分類看契約條件何時必須遵守：只要求報導日後遵守者，不改變報導日分類，但可能需揭露。</text>
<text x="70" y="412" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">約當現金：為支應短期現金承諾而持有；通常以自取得日起原始到期約三個月內作短期指標。</text>
<text x="70" y="448" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0369a1">準則條件先固定，再寫分錄。</text>
<rect x="42" y="504" width="816" height="228" rx="22" fill="#fff" stroke="#0f766e" stroke-width="3"/>
<text x="70" y="550" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">② 初始衡量・成本歸屬</text>
<text x="70" y="594" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">除役／復原義務先分形成時點：取得／建造資產時形成者與資產成本連動。</text>
<text x="70" y="632" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">日後使用資產生產存貨而形成的義務依 IAS 2 判斷，不能一律加回 PPE。</text>
<text x="70" y="670" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">金融負債交易成本：非 FVTPL 才納入初始衡量；FVTPL 交易成本發生時列損益。</text>
<text x="70" y="706" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#0f766e">同一支出先判準則歸屬，再決定是否資本化。</text>
<rect x="42" y="762" width="816" height="228" rx="22" fill="#fff" stroke="#b45309" stroke-width="3"/>
<text x="70" y="808" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">③ 後續衡量・金融工具・租賃</text>
<text x="70" y="852" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">權益 FVOCI：累積 OCI 不重分類至損益，但可在權益內移轉；股利通常列損益，收回投資成本部分例外。</text>
<text x="70" y="890" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">SPPI 題不能把「現金流會變動」直接等同不符合；2026 修正需依或有事件連動條件判斷。</text>
<text x="70" y="928" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">IFRS 16：短期租賃須不超過 12 個月且不得含購買選擇權；低價值看標的全新時價值。</text>
<text x="70" y="964" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#92400e">先分分類基礎，再判後續衡量與 OCI／損益去向。</text>
<rect x="42" y="1020" width="816" height="190" rx="22" fill="#fff" stroke="#7c3aed" stroke-width="3"/>
<text x="70" y="1066" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6d28d9">④ 所得稅・除列・表達過渡</text>
<text x="70" y="1108" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">IAS 12 單一交易修正後，租賃與除役義務不能再用舊版口訣一概排除遞延所得稅。</text>
<text x="70" y="1140" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">電子支付除列修正只適用特定系統與政策選擇；不可擴張成一般除列捷徑。</text>
<text x="70" y="1172" font-size="14" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">IFRS 18 國際 2027 生效；臺灣證券發行人 2028 過渡；間接法由 IFRS 18 營業損益小計起算。</text>
<rect x="42" y="1228" width="816" height="38" rx="15" fill="#075985"/>
<text x="450" y="1254" text-anchor="middle" font-size="14" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">定義 → 認列 → 初始衡量 → 後續衡量 → 分類／表達 → 揭露／過渡</text>
</svg>\n'''
def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'],expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('intermediate-accounting content version drift')
    changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟中級會計學認列衡量後續處理與表達判斷地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="中級會計學認列衡量後續處理與表達判斷地圖：先辨定義與認列，再固定初始衡量、後續處理、表達與揭露"></a><figcaption>認列 × 衡量 × 後續處理 × 表達判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
    ch0p=root/'chapters/ch00.html'; ch0=ch0p.read_text(encoding='utf-8')
    if VP_MARKER not in ch0:
        old='<figure><img alt="中級會計的解題地圖與準則思維判斷結構圖" loading="lazy" src="assets/intermediate-accounting-svg/ch00.svg"/><figcaption>中級會計的解題地圖與準則思維：先辨認問題，再依準則條件完成衡量與表達</figcaption></figure>'
        if old not in ch0: raise AssertionError('ch00 intermediate-accounting figure not found')
        ch0=ch0.replace(old,figure,1); ch0p.write_text(ch0,encoding='utf-8'); changed=True
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8')
    if VP_MARKER not in text:
        anchor='<h2 id="主題地圖">主題地圖</h2>'
        if anchor not in text: raise AssertionError('appendix-b topic map heading not found')
        text=text.replace(anchor,figure+anchor,1); ap.write_text(text,encoding='utf-8'); changed=True
    sp=site/VP_ASSET; target=svg_text()
    if sp.read_text(encoding='utf-8')!=target: sp.write_text(target,encoding='utf-8'); changed=True
    visual={'status':'passed','date':'2026-07-31','asset':VP_ASSET,'placement':'ch00 and appendix-b','canvaDesignId':CANVA_DESIGN_ID,'canvaEditUrl':CANVA_EDIT_URL,'tabletReadable':True,'zoomable':True,'offlineCachedViaExistingAssetPath':True}
    if m.get('visualPolish')!=visual: m['visualPolish']=visual; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); changed=True
    if changed:
        targetv=next_version(expected_before); lib['version']=targetv; libp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{targetv}';",sw,count=1)
        if n!=1: raise AssertionError('service worker version marker missing')
        swp.write_text(sw,encoding='utf-8'); return targetv
    return expected_before
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: apply_intermediate_accounting_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
