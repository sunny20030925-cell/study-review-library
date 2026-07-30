#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK = 'mathematical-economics'
BOOK_VERSION = '2026.07.30-2'
CANVA_DESIGN_ID = 'DAHQ1nDIXJk'
CANVA_EDIT_URL = 'https://www.canva.com/d/4onAJtenfeu_5_k'
VP_ASSET = 'assets/mathematical-economics-svg/kkt-inequality.svg'
VP_MARKER = 'data-vp-asset="mathematical-economics-optimization-dynamics-map"'


def next_version(version: str) -> str:
    match = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not match:
        raise AssertionError(f'invalid library version: {version}')
    return f'{match.group(1)}-{int(match.group(2)) + 1}'


def svg_text() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 835 1140" role="img" aria-labelledby="title desc">
<title id="title">數理經濟學最佳化與動態判斷地圖</title>
<desc id="desc">從最佳化限制類型、KKT 四塊、包絡與比較靜態，到離散與連續動態穩定性的考前判斷流程。</desc>
<rect width="835" height="1140" rx="28" fill="#faf7ff"/>
<rect x="28" y="28" width="779" height="150" rx="24" fill="#4c1d95"/>
<text x="58" y="82" font-size="26" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ede9fe">數理經濟學｜考前速查</text>
<text x="58" y="127" font-size="34" font-weight="800" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ffffff">最佳化與動態判斷地圖</text>
<text x="58" y="158" font-size="16" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ddd6fe">先辨認問題類型，再選條件；最後一定回代可行域與符號慣例。</text>

<rect x="40" y="210" width="755" height="225" rx="22" fill="#f5f3ff" stroke="#7c3aed" stroke-width="3"/>
<circle cx="84" cy="257" r="25" fill="#7c3aed"/><text x="84" y="266" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">1</text>
<text x="126" y="266" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#4c1d95">最佳化：先分限制類型</text>
<text x="70" y="314" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">無限制：FOC → SOC／凹凸性 → 端點</text>
<text x="70" y="350" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">等式限制：Lagrangian + h(x)=0</text>
<text x="70" y="386" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">受限 SOC：沿可行切方向判斷，不只看原 Hessian</text>
<text x="70" y="418" font-size="16" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7c2d12">先寫可行域；候選點不等於已證明最適。</text>

<rect x="40" y="465" width="755" height="230" rx="22" fill="#fff7ed" stroke="#ea580c" stroke-width="3"/>
<circle cx="84" cy="512" r="25" fill="#ea580c"/><text x="84" y="521" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">2</text>
<text x="126" y="521" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">KKT：四塊一起檢查</text>
<text x="70" y="568" font-size="18" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#7c2d12">stationarity ・ primal feasibility ・ dual feasibility ・ complementary slackness</text>
<text x="70" y="616" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">必要性：需適當 constraint qualification（例如適用情況下 LICQ／Slater）。</text>
<text x="70" y="653" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">充分性：還要搭配凹最大化／凸最小化等適當結構，不能只看到 KKT 就宣布全域最適。</text>

<rect x="40" y="725" width="755" height="170" rx="22" fill="#ecfeff" stroke="#0891b2" stroke-width="3"/>
<circle cx="84" cy="772" r="25" fill="#0891b2"/><text x="84" y="781" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">3</text>
<text x="126" y="781" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#155e75">包絡與比較靜態</text>
<text x="70" y="829" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">均衡 F(x,θ)=0：局部比較靜態先看 Jacobian／implicit function。</text>
<text x="70" y="866" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">值函數：dV/dθ = ∂L/∂θ（適當條件）；影子價格符號要跟 Lagrangian 慣例一起判。</text>

<rect x="40" y="925" width="755" height="180" rx="22" fill="#f0fdf4" stroke="#16a34a" stroke-width="3"/>
<circle cx="84" cy="972" r="25" fill="#16a34a"/><text x="84" y="981" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">4</text>
<text x="126" y="981" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#166534">動態：離散 vs 連續</text>
<text x="70" y="1026" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">離散 xₜ₊₁=F(xₜ)：先解 x*=F(x*)；局部穩定看 |F′(x*)|&lt;1。</text>
<text x="70" y="1058" font-size="17" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1f2937">連續 ẋ=G(x)：先令 G(x*)=0；一維常用局部判準 G′(x*)&lt;0。</text>
<text x="70" y="1090" font-size="15" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#166534">邊界 |F′|=1 或線性化導數=0：回到非線性項，線性化本身不下結論。</text>
</svg>
'''


def apply(site_root: str) -> bool:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest_path = root / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('id') != BOOK or manifest.get('version') != BOOK_VERSION:
        raise AssertionError(f'mathematical-economics VP requires {BOOK_VERSION}')

    changed = False
    appendix = root / 'chapters/appendix-b.html'
    text = appendix.read_text(encoding='utf-8')
    figure = (
        '<figure class="chapter-figure" data-vp-asset="mathematical-economics-optimization-dynamics-map">'
        '<a href="assets/mathematical-economics-svg/kkt-inequality.svg" target="_blank" rel="noopener" '
        'aria-label="開啟數理經濟學最佳化與動態判斷地圖大圖">'
        '<img loading="lazy" src="assets/mathematical-economics-svg/kkt-inequality.svg" '
        'alt="數理經濟學最佳化與動態判斷地圖：最佳化、KKT、包絡與比較靜態、動態穩定四區塊"></a>'
        '<figcaption>最佳化與動態判斷地圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>'
    )
    if VP_MARKER not in text:
        text, n = re.subn(r'(<p class="lead">.*?</p>)', r'\1' + figure, text, count=1, flags=re.S)
        if n != 1:
            raise AssertionError('appendix-b lead paragraph not found for VP insertion')
        appendix.write_text(text, encoding='utf-8')
        changed = True

    svg_path = site / VP_ASSET
    target_svg = svg_text()
    if svg_path.read_text(encoding='utf-8') != target_svg:
        svg_path.write_text(target_svg, encoding='utf-8')
        changed = True

    visual = {
        'status': 'passed',
        'date': '2026-07-30',
        'asset': VP_ASSET,
        'placement': 'ch13 and appendix-b',
        'canvaDesignId': CANVA_DESIGN_ID,
        'canvaEditUrl': CANVA_EDIT_URL,
        'tabletReadable': True,
        'zoomable': True,
        'offlineCachedViaExistingAssetPath': True,
    }
    if manifest.get('visualPolish') != visual:
        manifest['visualPolish'] = visual
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changed = True
    return changed


def apply_and_bump(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    lib_path = site / 'data/library.json'
    library = json.loads(lib_path.read_text(encoding='utf-8'))
    if library.get('version') != expected_before:
        raise AssertionError((library.get('version'), expected_before))
    ids = [b['id'] for b in library.get('books', [])]
    if ids.count(BOOK) != 1:
        raise AssertionError(f'{BOOK} must exist exactly once for in-place VP')

    changed = apply(site_root)
    if not changed:
        print(expected_before)
        return expected_before

    target = next_version(expected_before)
    library['version'] = target
    lib_path.write_text(json.dumps(library, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, count = re.subn(r"const VERSION = 'study-library-[^']+';", f"const VERSION = 'study-library-{target}';", sw, count=1)
    if count != 1:
        raise AssertionError('service worker version marker missing')
    sw_path.write_text(sw, encoding='utf-8')
    print(target)
    return target


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/apply_mathematical_economics_visual_polish.py SITE_ROOT EXPECTED_BEFORE')
    apply_and_bump(sys.argv[1], sys.argv[2])
