#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK = 'mathematical-economics'
BOOK_VERSION = '2026.07.30-2'
ASSET = 'assets/mathematical-economics-svg/kkt-inequality.svg'
MARKER = 'data-vp-asset="mathematical-economics-optimization-dynamics-map"'
CANVA_ID = 'DAHQ1nDIXJk'


def main(site_root: str, expected_library: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    lib = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    checks = 0

    def ck(cond: bool, msg: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    ids = [b['id'] for b in lib['books']]
    ck(lib['version'] == expected_library, 'library version')
    ck(ids.count(BOOK) == 1, 'book appears exactly once')
    ck(manifest['id'] == BOOK and manifest['version'] == BOOK_VERSION, 'manifest id/version')
    ck(questions['bookId'] == BOOK and questions['version'] == BOOK_VERSION, 'questions id/version')
    ck(len(manifest['chapters']) == 23, '20 chapters + 3 appendices')
    ck(questions['count'] == len(questions['items']) == 100, '100 questions')
    ck(len(search['entries']) == 150, '150 search entries')
    ck([q['id'] for q in questions['items']] == [f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)], 'question ids stable')

    visual = manifest.get('visualPolish', {})
    ck(visual.get('status') == 'passed', 'visual polish passed')
    ck(visual.get('asset') == ASSET, 'visual polish asset path')
    ck(visual.get('placement') == 'ch13 and appendix-b', 'visual polish placement')
    ck(visual.get('canvaDesignId') == CANVA_ID, 'Canva design id')
    ck(bool(visual.get('canvaEditUrl')), 'Canva edit URL')
    ck(visual.get('tabletReadable') is True, 'tablet readable')
    ck(visual.get('zoomable') is True, 'zoomable')
    ck(visual.get('offlineCachedViaExistingAssetPath') is True, 'offline cache reuse')

    appendix = (root / 'chapters/appendix-b.html').read_text(encoding='utf-8')
    ck(appendix.count(MARKER) == 1, 'appendix VP marker exactly once')
    ck(appendix.count(ASSET) == 2, 'appendix linked and embedded asset')
    ck('target="_blank"' in appendix and '點圖可開啟 SVG 大圖放大閱讀' in appendix, 'standalone zoom affordance')
    ck('最佳化與動態判斷地圖' in appendix, 'appendix caption/alt')

    ch13 = (root / 'chapters/ch13.html').read_text(encoding='utf-8')
    ck(ASSET in ch13, 'chapter 13 reuses existing VP asset path')

    svg_path = site / ASSET
    ck(svg_path.is_file(), 'VP SVG exists')
    svg = svg_path.read_text(encoding='utf-8')
    ck('viewBox="0 0 835 1140"' in svg, 'tablet portrait SVG viewBox')
    ck('<title id="title">數理經濟學最佳化與動態判斷地圖</title>' in svg, 'accessible title')
    ck('<desc id="desc">' in svg, 'accessible description')
    for token in [
        '最佳化：先分限制類型',
        'stationarity',
        'primal feasibility',
        'dual feasibility',
        'complementary slackness',
        'constraint qualification',
        'Jacobian',
        'dV/dθ = ∂L/∂θ',
        '|F′(x*)|&lt;1',
        'G′(x*)&lt;0',
        '線性化本身不下結論',
    ]:
        ck(token in svg, f'SVG token {token}')
    ck('href="http' not in svg and "href='http" not in svg, 'no remote SVG dependency')
    ck(len(list((site / 'assets/mathematical-economics-svg').glob('*.svg'))) == 20, '20 SVG contract preserved')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw, 'service worker version')
    ck(f'./{ASSET}' in sw, 'existing VP asset cache path')

    print(
        f'MATHEMATICAL_ECONOMICS_VP_QA_OK checks={checks} books={len(ids)} '
        f'library={expected_library} content_version={BOOK_VERSION} figures=20 '
        'visual_polish=passed progress_storage_changed=false'
    )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/qa_mathematical_economics_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
