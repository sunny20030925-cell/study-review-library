#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

BOOK = 'advanced-statistics'
BOOK_VERSION = '2026.07.30-1'
CANVA_DESIGN_ID = 'DAHQ1ZXj2QA'
CANVA_EDIT_URL = 'https://www.canva.com/d/JJGioLQiGpjgePs'
VP_ASSET = 'assets/advanced-statistics-svg/math-bridge.svg'
VP_MARKER = 'data-vp-asset="advanced-statistics-inference-roadmap"'


def svg_text() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 1100" role="img" aria-labelledby="title desc">
<title id="title">高等統計推論路線圖</title>
<desc id="desc">從模型與抽樣、點估計與估計量品質、檢定理論到線性模型的高等統計考前判斷路線，並提醒精確與漸近條件。</desc>
<rect width="830" height="1100" rx="28" fill="#f8fafc"/>
<rect x="28" y="28" width="774" height="150" rx="24" fill="#1e3a8a"/>
<text x="58" y="85" font-size="34" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#ffffff">高等統計推論路線圖</text>
<text x="58" y="132" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#dbeafe">模型 → 抽樣 → 估計 → 信賴區間 → 檢定 → 線性模型</text>
<text x="58" y="162" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#bfdbfe">第一個判斷：Exact（有限樣本精確）還是 Asymptotic（大樣本漸近）？</text>

<rect x="40" y="210" width="750" height="205" rx="22" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>
<circle cx="86" cy="256" r="25" fill="#2563eb"/><text x="86" y="265" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">1</text>
<text x="128" y="264" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e3a8a">建模與抽樣</text>
<text x="72" y="310" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e293b">PMF / PDF・support・joint / marginal / conditional・Jacobian</text>
<text x="72" y="347" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e293b">LLN ≠ CLT；Slutsky / Delta method 是漸近工具</text>
<text x="72" y="384" font-size="18" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#b45309">χ²、t、F 要當「精確」結果使用，先檢查常態與獨立條件。</text>

<rect x="40" y="445" width="750" height="220" rx="22" fill="#f0fdf4" stroke="#16a34a" stroke-width="3"/>
<circle cx="86" cy="492" r="25" fill="#16a34a"/><text x="86" y="501" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">2</text>
<text x="128" y="500" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#166534">點估計與估計量品質</text>
<text x="72" y="547" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e293b">MoM・MLE・bias / variance / MSE・consistency・asymptotic normality</text>
<text x="72" y="590" font-size="21" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#14532d">MLE：θ̂ = argmax ℓ(θ)</text>
<text x="72" y="628" font-size="21" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#14532d">CRLB：Var(T) ≥ 1 / I(θ)　〔需正則條件〕</text>

<rect x="40" y="695" width="750" height="195" rx="22" fill="#fff7ed" stroke="#ea580c" stroke-width="3"/>
<circle cx="86" cy="741" r="25" fill="#ea580c"/><text x="86" y="750" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">3</text>
<text x="128" y="749" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">檢定理論</text>
<text x="72" y="795" font-size="19" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e293b">size α・power 1−β・Neyman–Pearson・UMP / MLR・LRT</text>
<text x="72" y="835" font-size="19" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#9a3412">p-value ≠ P(H₀ | data)</text>
<text x="72" y="870" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e293b">Wilks：正則條件下，大樣本 likelihood-ratio statistic → χ²。</text>

<rect x="40" y="920" width="750" height="145" rx="22" fill="#faf5ff" stroke="#9333ea" stroke-width="3"/>
<circle cx="86" cy="966" r="25" fill="#9333ea"/><text x="86" y="975" text-anchor="middle" font-size="24" font-weight="700" font-family="sans-serif" fill="#fff">4</text>
<text x="128" y="974" font-size="25" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6b21a8">線性模型與最後檢查</text>
<text x="72" y="1015" font-size="18" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#1e293b">Gauss–Markov：OLS 是 BLUE 不需要常態；精確小樣本 t / F 才另需常態。</text>
<text x="72" y="1048" font-size="17" font-weight="700" font-family="system-ui,-apple-system,'Noto Sans TC','Microsoft JhengHei',sans-serif" fill="#6b21a8">作答順序：目標參數 → 統計量 / 估計量 → Exact / Asymptotic → 成立條件 → 公式</text>
</svg>
'''


def apply(site_root: str) -> bool:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest_path = root / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('id') != BOOK or manifest.get('version') != BOOK_VERSION:
        raise AssertionError(f'advanced-statistics VP requires {BOOK_VERSION}')

    appendix = root / 'chapters/appendix-b.html'
    text = appendix.read_text(encoding='utf-8')
    changed = False
    figure = (
        '<figure class="chapter-figure" data-vp-asset="advanced-statistics-inference-roadmap">'
        '<a href="assets/advanced-statistics-svg/math-bridge.svg" target="_blank" rel="noopener" '
        'aria-label="開啟高等統計推論路線圖大圖">'
        '<img loading="lazy" src="assets/advanced-statistics-svg/math-bridge.svg" '
        'alt="高等統計推論路線圖：建模與抽樣、點估計與品質、檢定理論、線性模型四區塊"></a>'
        '<figcaption>高等統計推論路線圖｜點圖可開啟 SVG 大圖放大閱讀。</figcaption></figure>'
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
        'placement': 'appendix-b and ch00',
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
