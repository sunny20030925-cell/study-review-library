#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from public_finance_content_a import CHAPTERS_A
from public_finance_content_b import CHAPTERS_B
from public_finance_questions_a import QUESTIONS_A
from public_finance_questions_b import QUESTIONS_B

BOOK = 'public-finance'
TITLE = '財政學'
SUBTITLE = '公共支出・租稅・分配・地方財政'
VERSION = '2026.07.29-1'
UPDATED_AT = '2026-07-29'
COVER = '財'
ACCENT = '#7c3aed'
CHAPTERS = CHAPTERS_A + CHAPTERS_B
QUESTIONS = QUESTIONS_A + QUESTIONS_B
DIFFICULTY_BY_SLOT = {
    'q01': '基礎',
    'q02': '標準',
    'q03': '標準',
    'q04': '綜合',
    'q05': '陷阱',
}


def jdump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'


def deep_replace(value, old, new):
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [deep_replace(v, old, new) for v in value]
    if isinstance(value, dict):
        return {k: deep_replace(v, old, new) for k, v in value.items()}
    return value


def ul(items):
    return '<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in items) + '</ul>'


def chapter_html(ch):
    defs = ''.join(
        f'<dt>{html.escape(term)}</dt><dd>{html.escape(desc)}</dd>'
        for term, desc in ch['definitions']
    )
    formulas = ''.join(
        f'<div class="formula-card"><p class="math display">\\[{formula}\\]</p><p>{html.escape(note)}</p></div>'
        for formula, note in ch['formulas']
    )
    intuition = ''.join(f'<p>{html.escape(p)}</p>' for p in ch['intuition'])
    example = ''.join(f'<p>{html.escape(p)}</p>' for p in ch['example'])
    checks = ''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    fig = ch['slug'] + '.svg'
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/public-finance-svg/{fig}" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
<h2 id="本章要解決的問題">本章要解決的問題</h2>
<p>{html.escape(ch['problem'])}</p>
<h2 id="白話直覺">白話直覺</h2>
{intuition}
<h2 id="正式定義與核心概念">正式定義與核心概念</h2>
<dl class="term-list">{defs}</dl>
<h2 id="核心公式與成立條件">核心公式與成立條件</h2>
{formulas}
<h2 id="完整標準例題">完整標準例題</h2>
<div class="worked-example">{example}</div>
<h2 id="常見錯誤">常見錯誤</h2>
{ul(ch['traps'])}
<h2 id="考試判斷方法">考試判斷方法</h2>
{ul(ch['exam'])}
<h2 id="理解檢查">理解檢查</h2>
<ol class="quick-check">{checks}</ol>
'''


def render_svg(ch):
    title, labels = ch['figure']
    safe_title = xml_escape(title)
    safe_desc = xml_escape(' → '.join(labels))
    boxes = []
    arrows = []
    xs = [55, 245, 435, 625]
    for i, (x, label) in enumerate(zip(xs, labels)):
        boxes.append(
            f'<rect x="{x}" y="150" width="150" height="92" rx="18" fill="#f5f7ff" stroke="#4f5d95" stroke-width="3"/>'
            f'<text x="{x+75}" y="199" text-anchor="middle" font-size="20" font-family="sans-serif" fill="#1f2947">{xml_escape(label)}</text>'
        )
        if i < 3:
            arrows.append(
                f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#5b647d" stroke-width="4"/>'
                f'<polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#5b647d"/>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 390" role="img" aria-labelledby="title desc">
<title id="title">{safe_title}</title><desc id="desc">{safe_desc}</desc>
<rect width="830" height="390" rx="26" fill="#ffffff"/>
<text x="415" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#18203a">{safe_title}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="415" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#586174">先辨認機制，再套公式與條件，最後回到效率與分配。</text>
</svg>\n'''


def appendix_a(chapters):
    rows = []
    for ch in chapters:
        for formula, note in ch['formulas']:
            rows.append(
                f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({formula}\\)</td><td>{html.escape(note)}</td></tr>'
            )
    return '''<h1>附錄 A　核心公式與圖形速查</h1>
<p class="lead">這份附錄用來考前快速定位公式。公式只有在相應假設成立時才能直接使用，先讀第三欄的條件，再代數字。</p>
<h2 id="福利與公共支出">福利與公共支出</h2>
<p>公共財、外部性與成本效益題的共同原則，是把私人邊際量轉成社會邊際量，並把不同時間點換成同一現值。</p>
<h2 id="租稅與歸宿">租稅與歸宿</h2>
<p>租稅題先找稅基與稅楔，再判斷彈性、數量反應與分配；稅收本身不要誤當成無謂損失。</p>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>公式</th><th>成立條件與用途</th></tr></thead><tbody>''' + ''.join(rows) + '</tbody></table>\n'


def appendix_b():
    return '''<h1>附錄 B　財政學解題路線</h1>
<p class="lead">遇到陌生題目時，不要先背政策結論。先判斷市場／政府機制，再找邊際條件與歸宿，最後才做福利判斷。</p>
<h2 id="市場失靈題">市場失靈題</h2>
<ol><li>辨認公共財、外部性、資訊不對稱或市場力。</li><li>寫出私人與社會邊際量的差。</li><li>找有效率條件。</li><li>比較稅、補貼、數量規制、資訊或公共提供的資訊需求。</li></ol>
<h2 id="租稅題">租稅題</h2>
<ol><li>辨認稅基與法定繳納者。</li><li>畫稅楔，分買方支付與賣方實收。</li><li>用相對彈性判斷經濟歸宿。</li><li>再算稅收、DWL 與分配效果；三者不可混為同一數字。</li></ol>
<h2 id="公共支出與保險題">公共支出與保險題</h2>
<ol><li>把帳面支出改成社會機會成本。</li><li>跨期金額先折現。</li><li>保險題分逆選擇與道德風險。</li><li>移轉題把福利退場一起算進有效邊際稅率。</li></ol>
<h2 id="地方財政與公債題">地方財政與公債題</h2>
<ol><li>地方財政先找跨區外部性、偏好差異與規模經濟。</li><li>補助分一般補助與配合款。</li><li>公債先分赤字 flow 與債務 stock。</li><li>債務動態先定義初級盈餘／赤字正負號，再代入 r、g 與 b。</li></ol>
'''


def appendix_c():
    terms = [
        ('Public Finance / Public Economics','財政學／公共經濟學'),('Positive Analysis','實證分析'),('Normative Analysis','規範分析'),
        ('Pareto Efficiency','Pareto 效率'),('Social Welfare Function','社會福利函數'),('Market Failure','市場失靈'),('Government Failure','政府失靈'),
        ('Public Good','公共財'),('Free Riding','搭便車'),('Samuelson Condition','Samuelson 條件'),('Externality','外部性'),('Pigouvian Tax','Pigouvian 稅'),
        ('Coase Theorem','Coase 定理'),('Tradable Permits','可交易許可'),('Median Voter Theorem','中位數選民定理'),('Rent Seeking','尋租'),
        ('Cost–Benefit Analysis','成本效益分析'),('Net Present Value','淨現值'),('Shadow Price','影子價格'),('Lorenz Curve','Lorenz curve'),('Gini Coefficient','Gini coefficient'),
        ('Adverse Selection','逆選擇'),('Moral Hazard','道德風險'),('Pay-As-You-Go','隨收隨付'),('Fully Funded','完全提存'),('Coinsurance','共同保險'),
        ('Tax Base','稅基'),('Average Tax Rate','平均稅率'),('Marginal Tax Rate','邊際稅率'),('Tax Incidence','租稅歸宿'),('Tax Wedge','稅楔'),
        ('Deadweight Loss','無謂損失'),('Excess Burden','超額負擔'),('Ramsey Rule','Ramsey 規則'),('Tax Credit','稅額抵免'),('Tax Deduction','所得扣除'),
        ('Tax Shield','稅盾'),('Value-Added Tax','加值型營業稅'),('Capitalization','稅負資本化'),('Fiscal Federalism','財政聯邦主義'),('Matching Grant','配合款'),
        ('Primary Balance','初級餘額'),('Debt-to-GDP Ratio','債務比'),('Fiscal Sustainability','財政永續'),
    ]
    rows = ''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en, zh in terms)
    return f'''<h1>附錄 C　中英名詞對照</h1>
<p class="lead">第一次看到英文題幹時，先把名詞對回本書的核心概念，不要因翻譯差異誤判模型。</p>
<h2 id="公共支出與福利">公共支出與福利</h2><p>Public good、externality、social welfare 與 cost–benefit 是公共支出篇的高頻字。</p>
<h2 id="租稅與地方財政">租稅與地方財政</h2><p>Incidence、excess burden、tax base、fiscal federalism 與 primary balance 要特別注意法律名稱和經濟概念的差別。</p>
<h2 id="名詞表">名詞表</h2><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>
'''


def search_entries(chapters, appendix_meta):
    entries = []
    section_fields = [
        ('本章要解決的問題', lambda c: c['problem']),
        ('白話直覺', lambda c: ' '.join(c['intuition'])),
        ('正式定義與核心概念', lambda c: ' '.join(f'{a}：{b}' for a,b in c['definitions'])),
        ('核心公式與成立條件', lambda c: ' '.join(f'{a}；{b}' for a,b in c['formulas'])),
        ('完整標準例題', lambda c: ' '.join(c['example'])),
        ('常見錯誤', lambda c: ' '.join(c['traps'])),
        ('考試判斷方法', lambda c: ' '.join(c['exam'])),
        ('理解檢查', lambda c: ' '.join(c['checks'])),
    ]
    for ch in chapters:
        entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':0,'title':ch['title'],'text':ch['problem']+' '+' '.join(ch['intuition'])})
        for page, (title, getter) in enumerate(section_fields, start=1):
            entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':title,'text':getter(ch)})
    for ch_id, title, text in appendix_meta:
        entries.extend([
            {'chapterId':ch_id,'chapterTitle':title,'page':0,'title':title,'text':text},
            {'chapterId':ch_id,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
            {'chapterId':ch_id,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先辨認條件、再選公式或分析路線，最後檢查效率、分配與單位。'},
        ])
    return entries


def append_sw_assets(sw, old_id, paths):
    if paths[0] in sw:
        return sw
    needle = f'./books/{old_id}/manifest.json'
    idx = sw.find(needle)
    if idx < 0:
        raise AssertionError(f'cannot locate existing book cache entry for {old_id}')
    starts = list(re.finditer(r'const\s+[A-Za-z0-9_$]+\s*=\s*\[', sw[:idx]))
    if not starts:
        raise AssertionError('cannot locate service-worker asset array')
    array_start = starts[-1].end() - 1
    array_end = sw.find('];', idx)
    if array_end < 0:
        raise AssertionError('cannot locate service-worker asset array end')
    body = sw[array_start+1:array_end]
    insertion = ''.join(f"\n  {json.dumps(p, ensure_ascii=False)}," for p in paths)
    if body.rstrip().endswith(','):
        insertion = insertion.lstrip('\n')
    return sw[:array_end] + insertion + '\n' + sw[array_end:]


def main(site_root):
    site = Path(site_root)
    lib_path = site / 'data/library.json'
    if not lib_path.is_file():
        raise SystemExit(f'library not found: {lib_path}')
    library = json.loads(lib_path.read_text(encoding='utf-8'))
    pre_ids = [b['id'] for b in library['books']]
    if BOOK in pre_ids:
        raise AssertionError(f'{BOOK} already exists')
    if not pre_ids:
        raise AssertionError('library has no template book')

    template_entry = copy.deepcopy(library['books'][-1])
    old_id = template_entry['id']
    template_entry = deep_replace(template_entry, old_id, BOOK)
    template_entry['id'] = BOOK
    template_entry['title'] = TITLE
    template_entry['subtitle'] = SUBTITLE
    template_entry['cover'] = COVER
    template_entry['accent'] = ACCENT
    template_entry['status'] = 'available'
    for key in ('description','summary'):
        if key in template_entry:
            template_entry[key] = '一般大學財政學：公共支出、市場失靈、分配、社會保險、租稅、地方財政與公債。'
    library['books'].append(template_entry)
    lib_path.write_text(jdump(library), encoding='utf-8')

    old_root = site / 'books' / old_id
    old_manifest = json.loads((old_root / 'manifest.json').read_text(encoding='utf-8'))
    old_questions = json.loads((old_root / 'questions.json').read_text(encoding='utf-8'))

    root = site / 'books' / BOOK
    chdir = root / 'chapters'
    figdir = site / 'assets/public-finance-svg'
    chdir.mkdir(parents=True, exist_ok=False)
    figdir.mkdir(parents=True, exist_ok=False)

    chapter_meta = []
    chapter_titles = {}
    for ch in CHAPTERS:
        number = str(int(ch['id'][2:]))
        rel = f'chapters/{ch["id"]}.html'
        (root / rel).write_text(chapter_html(ch), encoding='utf-8')
        (figdir / f'{ch["slug"]}.svg').write_text(render_svg(ch), encoding='utf-8')
        chapter_meta.append({'id':ch['id'],'number':number,'title':ch['title'],'file':rel,'kind':'chapter'})
        chapter_titles[ch['id']] = f'第 {number} 章 {ch["title"]}'

    appendices = [
        ('appendix-a','A','核心公式與圖形速查','chapters/appendix-a.html', appendix_a(CHAPTERS)),
        ('appendix-b','B','財政學解題路線','chapters/appendix-b.html', appendix_b()),
        ('appendix-c','C','中英名詞對照','chapters/appendix-c.html', appendix_c()),
    ]
    for ch_id, number, title, rel, body in appendices:
        (root / rel).write_text(body, encoding='utf-8')
        chapter_meta.append({'id':ch_id,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest = deep_replace(copy.deepcopy(old_manifest), old_id, BOOK)
    manifest['id'] = BOOK
    manifest['title'] = TITLE
    manifest['subtitle'] = SUBTITLE
    manifest['version'] = VERSION
    manifest['cover'] = COVER
    manifest['accent'] = ACCENT
    manifest['updatedAt'] = UPDATED_AT
    manifest['chapters'] = chapter_meta
    manifest['releaseNotes'] = [{
        'version': VERSION,
        'date': UPDATED_AT,
        'title': '新增一般大學財政學教材',
        'changes': [
            '新增 20 章正文與 3 份附錄，涵蓋公共支出、分配、租稅、地方財政與公債',
            '新增 100 題題庫，每章 5 題並包含可重新驗算的數值題',
            '新增 20 張自製 SVG 與全文搜尋索引',
            '內容避開會隨年度修法變動的稅率與扣除額，維持財政學理論本位',
        ],
        'progressImpact': '新增獨立書籍，不改動既有書籍章節、題目 ID 或閱讀進度。',
    }]
    for key in ('description','summary'):
        if key in manifest:
            manifest[key] = '從近零基礎銜接一般大學財政學，聚焦公共支出、市場失靈、分配、租稅理論、地方財政與政府債務。'
    (root / 'manifest.json').write_text(jdump(manifest), encoding='utf-8')

    qtop = deep_replace(copy.deepcopy(old_questions), old_id, BOOK)
    qtop['bookId'] = BOOK
    qtop['version'] = VERSION
    qitems = []
    for src in QUESTIONS:
        slot = src['id'].rsplit('-', 1)[-1]
        item = {
            'id': src['id'],
            'bookId': BOOK,
            'chapterId': src['chapterId'],
            'chapterTitle': chapter_titles[src['chapterId']],
            'topic': next(ch['title'] for ch in CHAPTERS if ch['id'] == src['chapterId']),
            'difficulty': DIFFICULTY_BY_SLOT[slot],
            'question': src['question'],
            'answer': src['answer'],
            'explanation': src['explanation'],
            'source': '本書自編標準題型',
        }
        qitems.append(item)
    qtop['count'] = len(qitems)
    qtop['items'] = qitems
    (root / 'questions.json').write_text(jdump(qtop), encoding='utf-8')

    appendix_meta = [
        ('appendix-a','核心公式與圖形速查','公共財、外部性、成本效益、租稅歸宿、超額負擔與債務動態的核心公式。'),
        ('appendix-b','財政學解題路線','市場失靈、租稅、公共支出、地方財政與公債的判斷流程。'),
        ('appendix-c','中英名詞對照','公共經濟學與財政學常見英文術語對照。'),
    ]
    entries = search_entries(CHAPTERS, appendix_meta)
    (root / 'search.json').write_text(jdump({'entries':entries}), encoding='utf-8')

    cache_paths = [
        f'./books/{BOOK}/manifest.json', f'./books/{BOOK}/questions.json', f'./books/{BOOK}/search.json',
    ]
    cache_paths += [f'./books/{BOOK}/{x["file"]}' for x in chapter_meta]
    cache_paths += [f'./assets/public-finance-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw_path.write_text(append_sw_assets(sw, old_id, cache_paths), encoding='utf-8')

    print(json.dumps({
        'book': BOOK, 'version': VERSION, 'chapters': 20, 'appendices': 3,
        'questions': len(qitems), 'search': len(entries), 'figures': len(CHAPTERS),
        'pre_books': len(pre_ids), 'post_books': len(library['books']),
    }, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/generate_public_finance.py SITE_ROOT')
    main(sys.argv[1])
