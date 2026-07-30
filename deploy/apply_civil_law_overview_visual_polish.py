#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path

BOOK='civil-law-overview'
BOOK_VERSION='2026.07.30-2'
CANVA_DESIGN_ID='DAHQ2mt-Yds'
CANVA_EDIT_URL='https://www.canva.com/d/3hxkdRsJsAWGQB-'
VP_ASSET='assets/civil-law-overview-svg/civil-map.svg'
VP_MARKER='data-vp-asset="civil-law-claim-basis-roadmap"'

def next_version(v:str)->str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def svg_text()->str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1220" role="img" aria-labelledby="title desc">
<title id="title">民法案例題請求權基礎地圖</title>
<desc id="desc">民法案例題先確定誰對誰主張什麼，再依契約、不當得利、侵權、物權或親屬繼承尋找請求權基礎，最後檢查發生、變動、受阻與法律效果。</desc>
<rect width="900" height="1220" rx="30" fill="#eff6ff"/>
<rect x="34" y="34" width="832" height="172" rx="24" fill="#1e3a8a"/>
<text x="68" y="91" font-size="35" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">民法案例題請求權基礎地圖</text>
<text x="68" y="136" font-size="20" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">誰對誰 → 要什麼 → 找請求權基礎 → 發生／變動／受阻／效果</text>
<text x="68" y="176" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bfdbfe">先定目標，再選法律關係；不要看到損害就直接跳侵權。</text>

<rect x="42" y="238" width="816" height="168" rx="22" fill="#ffffff" stroke="#2563eb" stroke-width="3"/>
<text x="70" y="284" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e3a8a">① 先定目標｜A 對 B 要什麼？</text>
<text x="70" y="328" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">交付／返還／賠償／停止妨害／解除或撤銷／身分與繼承效果</text>
<text x="70" y="370" font-size="18" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1d4ed8">已有契約 → 先查契約履行與債務不履行，再看其他請求權是否並存。</text>

<rect x="42" y="438" width="390" height="218" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="68" y="482" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">② 不當得利｜§179</text>
<text x="68" y="525" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">無法律上原因受利益，</text>
<text x="68" y="559" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">致他人受損害 → 應返還其利益。</text>
<text x="68" y="607" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">原因其後不存在，也要再檢查 §179 後段。</text>

<rect x="468" y="438" width="390" height="218" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="494" y="482" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">③ 侵權｜§184 常見入口</text>
<text x="494" y="525" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">故意或過失＋不法侵害他人權利</text>
<text x="494" y="559" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">→ 原則上負損害賠償責任。</text>
<text x="494" y="607" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">考題另可能涉及善良風俗或保護他人法律等型態。</text>

<rect x="42" y="688" width="390" height="218" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="68" y="732" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">④ 物權｜§767</text>
<text x="68" y="775" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">無權占有／侵奪 → 請求返還</text>
<text x="68" y="809" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">妨害所有權 → 請求除去</text>
<text x="68" y="843" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">有妨害之虞 → 請求防止</text>
<text x="68" y="879" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">先確認所有權與占有權源；債權 ≠ 物權。</text>

<rect x="468" y="688" width="390" height="218" rx="22" fill="#ffffff" stroke="#3b82f6" stroke-width="3"/>
<text x="494" y="732" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e40af">⑤ 親屬／繼承｜特別規則</text>
<text x="494" y="775" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">婚姻、親子、扶養、繼承、遺囑</text>
<text x="494" y="809" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">→ 先走身分法與繼承法的特別要件。</text>
<text x="494" y="855" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#2563eb">不要把身分效果硬套成一般契約問題。</text>

<rect x="42" y="938" width="816" height="136" rx="22" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
<text x="68" y="980" font-size="22" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e3a8a">⑥ 四格檢查｜每一個請求權都跑一次</text>
<text x="68" y="1022" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">發生：要件齊嗎？　變動：撤銷／解除／讓與／抵銷？　受阻：時效／抗辯／第三人？</text>
<text x="68" y="1055" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">效果：最後可以交付、返還、賠償、除去妨害，或發生其他何種法律效果？</text>

<rect x="42" y="1100" width="816" height="82" rx="20" fill="#1e3a8a"/>
<text x="68" y="1135" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#fff">§125：一般請求權原則 15 年；法律另定較短期間者，依其規定。</text>
<text x="68" y="1165" font-size="15" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">最後檢查：無效／得撤銷／效力未定不要混用；年齡、期間、方式與身分規則要確認法規時點。</text>
</svg>\n'''

def apply(site_root:str, expected_before:str)->str:
    site=Path(site_root); libp=site/'data/library.json'; lib=json.loads(libp.read_text(encoding='utf-8'))
    if lib['version']!=expected_before: raise AssertionError((lib['version'], expected_before))
    root=site/'books'/BOOK; mp=root/'manifest.json'; m=json.loads(mp.read_text(encoding='utf-8'))
    if m.get('id')!=BOOK or m.get('version')!=BOOK_VERSION: raise AssertionError('civil-law-overview content version drift')
    ap=root/'chapters/appendix-b.html'; text=ap.read_text(encoding='utf-8'); changed=False
    figure=(f'<figure class="chapter-figure" {VP_MARKER}><a href="{VP_ASSET}" target="_blank" rel="noopener" aria-label="開啟民法案例題請求權基礎地圖大圖"><img loading="lazy" src="{VP_ASSET}" alt="民法案例題請求權基礎地圖：先定當事人與目標，再依契約、不當得利、侵權、物權、親屬繼承尋找基礎並做四格檢查"></a><figcaption>民法案例題請求權基礎地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>')
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
    if len(sys.argv)!=3: raise SystemExit('usage: apply_civil_law_overview_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    print(apply(sys.argv[1],sys.argv[2]))
