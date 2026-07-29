#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from game_theory_content_a import CHAPTERS_A
from game_theory_content_b import CHAPTERS_B
from game_theory_questions_a import QUESTIONS_A
from game_theory_questions_b import QUESTIONS_B

BOOK = 'game-theory'
TITLE = '賽局理論及應用'
SUBTITLE = '策略互動・Nash 均衡・動態賽局・資訊不完全與制度設計'
VERSION = '2026.07.29-1'
UPDATED_AT = '2026-07-29'
COVER = '局'
ACCENT = '#b45309'
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
        f'<div class="formula-card"><p class="math display">\\[{html.escape(formula)}\\]</p><p>{html.escape(note)}</p></div>'
        for formula, note in ch['formulas']
    )
    intuition = ''.join(f'<p>{html.escape(p)}</p>' for p in ch['intuition'])
    example = ''.join(f'<p>{html.escape(p)}</p>' for p in ch['example'])
    checks = ''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    fig = ch['slug'] + '.svg'
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/game-theory-svg/{fig}" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
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
    xs = [52, 247, 442, 637]
    boxes = []
    arrows = []
    for i, (x, label) in enumerate(zip(xs, labels)):
        boxes.append(
            f'<rect x="{x}" y="148" width="150" height="94" rx="18" fill="#fff7ed" stroke="#b45309" stroke-width="3"/>'
            f'<text x="{x+75}" y="199" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#7c2d12">{xml_escape(label)}</text>'
        )
        if i < 3:
            arrows.append(
                f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#64748b" stroke-width="4"/>'
                f'<polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#64748b"/>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 390" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(' → '.join(labels))}</desc>
<rect width="840" height="390" rx="26" fill="#ffffff"/>
<text x="420" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#7c2d12">{xml_escape(title)}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="420" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先辨認時序與資訊，再選解概念；均衡之後才談效率與制度。</text>
</svg>\n'''


def appendix_a(chapters):
    rows = []
    for ch in chapters:
        for formula, note in ch['formulas']:
            rows.append(
                f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({html.escape(formula)}\\)</td><td>{html.escape(note)}</td></tr>'
            )
    return '''<h1>附錄 A　核心符號與解概念速查</h1>
<p class="lead">賽局理論最容易失分的地方不是算術，而是把不同資訊結構與解概念混在一起。先確認模型，再用相對應的均衡條件。</p>
<h2 id="四個核心解概念">四個核心解概念</h2>
<table><thead><tr><th>模型</th><th>常用解概念</th><th>額外檢查</th></tr></thead><tbody>
<tr><td>靜態＋完整資訊</td><td>Nash equilibrium</td><td>互為最佳回應、單方面偏離</td></tr>
<tr><td>動態＋完整資訊</td><td>SPNE</td><td>每個真正子賽局都要是 Nash</td></tr>
<tr><td>靜態＋不完全資訊</td><td>Bayesian Nash equilibrium</td><td>策略為 type→action，使用條件期望報酬</td></tr>
<tr><td>動態＋不完全資訊</td><td>Perfect Bayesian equilibrium</td><td>策略＋belief、Bayes consistency、sequential rationality</td></tr>
</tbody></table>
<h2 id="高頻符號">高頻符號</h2>
<p><strong>s_i</strong> 表玩家 i 的策略，<strong>s_-i</strong> 表其他玩家策略；<strong>u_i</strong> 是報酬；<strong>BR_i</strong> 是最佳回應；<strong>δ</strong> 常表示跨期折現因子；<strong>μ</strong> 常表示資訊集合上的信念。</p>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>公式／條件</th><th>使用時機</th></tr></thead><tbody>''' + ''.join(rows) + '</tbody></table>\n'


def appendix_b():
    return '''<h1>附錄 B　賽局理論標準解題路線</h1>
<p class="lead">陌生題目先不要猜「答案像哪個經典模型」。按時序、資訊、策略與報酬四步建模，再選解概念。</p>
<h2 id="第一步建模">第一步：建模</h2>
<ol><li>列玩家與每位玩家真正可控制的行動。</li><li>判斷同時還是先後行動；必要時畫賽局樹。</li><li>判斷誰知道什麼：完整資訊、私人 type、可觀察訊號或資訊集合。</li><li>把所有結果轉成 payoff；金錢只是可能的報酬代理。</li></ol>
<h2 id="第二步選解概念">第二步：選解概念</h2>
<ol><li>靜態完整資訊：最佳回應、優勢、純／混合 Nash。</li><li>動態完整資訊：向後歸納與 SPNE，檢查可信威脅。</li><li>靜態不完全資訊：Bayesian strategy 與 BNE。</li><li>動態不完全資訊：完整策略、belief、Bayes 更新與 PBE。</li></ol>
<h2 id="第三步數值工具">第三步：數值工具</h2>
<ol><li>混合策略：用「自己的機率使對手無差異」求解。</li><li>連續策略：固定對手策略最大化自己的 payoff，得到 reaction function 再聯立。</li><li>重複賽局：比較遵守策略與一次偏離的折現現值。</li><li>合作賽局：先寫效率，再逐 coalition 檢查 blocking；Shapley 另算平均邊際貢獻。</li></ol>
<h2 id="第四步最後檢查">第四步：最後檢查</h2>
<p>均衡不是效率、優勢不是 Nash 的同義詞、BNE 不是 PBE 的縮寫、Nash bargaining solution 不是 Nash equilibrium。題目若問制度或政策，再另外比較福利、資訊需求與誘因。</p>
'''


def appendix_c():
    terms = [
        ('Game Theory','賽局理論'),('Player','玩家'),('Action','行動'),('Strategy','策略'),('Payoff','報酬'),('Normal Form','策略式／正規式'),
        ('Best Response','最佳回應'),('Strict Dominance','嚴格優勢'),('Weak Dominance','弱優勢'),('Rationalizability','合理化'),('Nash Equilibrium','Nash 均衡'),
        ('Mixed Strategy','混合策略'),('Support','支撐集'),('Zero-Sum Game','零和賽局'),('Maximin','最大最小'),('Minimax Theorem','極小極大定理'),
        ('Reaction Function','反應函數'),('Cournot Competition','Cournot 數量競爭'),('Bertrand Competition','Bertrand 價格競爭'),('Extensive Form','展開式賽局'),
        ('Backward Induction','向後歸納'),('Subgame','子賽局'),('Subgame Perfect Nash Equilibrium','子賽局完美 Nash 均衡'),('Credible Threat','可信威脅'),
        ('Commitment','承諾'),('Ultimatum Game','最後通牒賽局'),('Alternating Offers','交替出價'),('Nash Bargaining Solution','Nash 議價解'),
        ('Repeated Game','重複賽局'),('Trigger Strategy','觸發策略'),('Folk Theorem','民間定理／Folk theorem'),('Type','型態'),('Common Prior','共同先驗'),
        ('Bayesian Nash Equilibrium','Bayesian Nash 均衡'),('Private Value','私人價值'),('Common Value','共同價值'),('Winner\'s Curse','贏家詛咒'),
        ('Perfect Bayesian Equilibrium','Perfect Bayesian 均衡'),('Belief','信念'),('Sequential Rationality','序列理性'),('Signaling','訊號傳遞'),
        ('Separating Equilibrium','分離均衡'),('Pooling Equilibrium','混同均衡'),('Screening','篩選'),('Incentive Compatibility','誘因相容'),('Individual Rationality','個別理性'),
        ('Cheap Talk','無成本訊息／cheap talk'),('Mechanism Design','機制設計'),('Revelation Principle','揭示原理'),('VCG Mechanism','VCG 機制'),
        ('Coalition','聯盟'),('Core','核心／core'),('Shapley Value','Shapley value'),('Congestion Game','擁擠賽局'),('Price of Anarchy','無政府代價／Price of Anarchy'),
    ]
    rows = ''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en, zh in terms)
    return f'''<h1>附錄 C　中英名詞對照</h1>
<p class="lead">英文題幹的難點常是同一概念有不同中文譯名。先認英文核心詞，再回到定義與解題條件。</p>
<h2 id="策略與均衡">策略與均衡</h2><p>Best response、dominance、Nash、mixed strategy 與 subgame perfection 是前半部高頻詞。</p>
<h2 id="資訊與制度">資訊與制度</h2><p>Type、belief、Bayesian、PBE、signaling、screening、IC、IR 與 mechanism design 要特別分清楚。</p>
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
            {'chapterId':ch_id,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先辨認玩家、時序與資訊，再選解概念，最後檢查偏離、信念與成立條件。'},
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
    insertion = ''.join(f'\n  {json.dumps(p, ensure_ascii=False)},' for p in paths)
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
            template_entry[key] = '一般大學賽局理論：策略式與動態賽局、Nash、重複賽局、資訊不完全、拍賣、訊號、機制與合作賽局。'
    library['books'].append(template_entry)
    lib_path.write_text(jdump(library), encoding='utf-8')

    old_root = site / 'books' / old_id
    old_manifest = json.loads((old_root / 'manifest.json').read_text(encoding='utf-8'))
    old_questions = json.loads((old_root / 'questions.json').read_text(encoding='utf-8'))

    root = site / 'books' / BOOK
    chdir = root / 'chapters'
    figdir = site / 'assets/game-theory-svg'
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
        ('appendix-a','A','核心符號與解概念速查','chapters/appendix-a.html', appendix_a(CHAPTERS)),
        ('appendix-b','B','賽局理論標準解題路線','chapters/appendix-b.html', appendix_b()),
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
        'title': '新增一般大學賽局理論及應用教材',
        'changes': [
            '新增 20 章正文與 3 份附錄，從策略式賽局延伸到動態、不完全資訊、機制與合作賽局',
            '新增 100 題題庫，每章 5 題並包含可獨立重算的均衡與機率題',
            '新增 20 張自製 SVG 與 189 筆全文搜尋索引',
            '明確區分 NE、SPNE、BNE、PBE，以及 Nash bargaining、core、Shapley 等不同解概念',
        ],
        'progressImpact': '新增獨立書籍，不改動既有書籍章節、題目 ID 或閱讀進度。',
    }]
    for key in ('description','summary'):
        if key in manifest:
            manifest[key] = '從近零基礎銜接一般大學賽局理論，聚焦策略互動、均衡、動態可信性、不完全資訊、拍賣、訊號與制度設計。'
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
        ('appendix-a','核心符號與解概念速查','NE、SPNE、BNE、PBE、最佳回應、混合策略、折現、信念與常用公式的快速定位。'),
        ('appendix-b','賽局理論標準解題路線','從玩家、時序、資訊與報酬建模，再選解概念並檢查偏離與信念。'),
        ('appendix-c','中英名詞對照','賽局理論、拍賣、訊號、機制設計與合作賽局的常用英文術語。'),
    ]
    entries = search_entries(CHAPTERS, appendix_meta)
    (root / 'search.json').write_text(jdump({'entries':entries}), encoding='utf-8')

    cache_paths = [
        f'./books/{BOOK}/manifest.json', f'./books/{BOOK}/questions.json', f'./books/{BOOK}/search.json',
    ]
    cache_paths += [f'./books/{BOOK}/{x["file"]}' for x in chapter_meta]
    cache_paths += [f'./assets/game-theory-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
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
        raise SystemExit('usage: python deploy/generate_game_theory.py SITE_ROOT')
    main(sys.argv[1])
