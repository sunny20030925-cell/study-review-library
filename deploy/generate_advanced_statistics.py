#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from advanced_statistics_content_a import CHAPTERS_A
from advanced_statistics_content_b import CHAPTERS_B
from advanced_statistics_questions_a import QUESTIONS_A
from advanced_statistics_questions_b import QUESTIONS_B

BOOK = 'advanced-statistics'
TITLE = '高等統計學'
SUBTITLE = '機率模型・抽樣分配・估計與檢定理論'
VERSION = '2026.07.29-1'
UPDATED_AT = '2026-07-29'
COVER = '高'
ACCENT = '#2563eb'
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
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/advanced-statistics-svg/{ch['slug']}.svg" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
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
    xs = [55, 245, 435, 625]
    boxes = []
    arrows = []
    for i, (x, label) in enumerate(zip(xs, labels)):
        boxes.append(
            f'<rect x="{x}" y="150" width="150" height="92" rx="18" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>'
            f'<text x="{x+75}" y="199" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#1e3a8a">{xml_escape(label)}</text>'
        )
        if i < 3:
            arrows.append(
                f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#64748b" stroke-width="4"/>'
                f'<polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#64748b"/>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 390" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(' → '.join(labels))}</desc>
<rect width="830" height="390" rx="26" fill="#ffffff"/>
<text x="415" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#1e3a8a">{xml_escape(title)}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="415" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先寫模型與條件，再推抽樣分布，最後判斷估計或檢定。</text>
</svg>
'''

def appendix_a(chapters):
    rows = []
    for ch in chapters:
        for formula, note in ch['formulas']:
            rows.append(
                f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({formula}\\)</td><td>{html.escape(note)}</td></tr>'
            )
    return '''<h1>附錄 A　核心分配、定理與公式速查</h1>
<p class="lead">高等統計最危險的不是少背一條公式，而是忘記公式成立的模型條件。這份表把公式和條件放在同一列。</p>
<h2 id="機率與分配">機率與分配</h2>
<p>先辨認支撐、參數化與獨立性；Gamma 本書固定使用 rate 參數，常態精確抽樣分配要另外確認母體常態。</p>
<h2 id="估計與檢定">估計與檢定</h2>
<p>MLE、Fisher information、CRLB、Wilks、t 與 F 都有各自條件。考試先寫條件，再代公式。</p>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>公式／定理</th><th>成立條件與用途</th></tr></thead><tbody>''' + ''.join(rows) + '</tbody></table>\n'

def appendix_b():
    return '''<h1>附錄 B　高等統計解題路線</h1>
<p class="lead">陌生題先判斷「模型 → 隨機量 → 抽樣分布 → 目標參數 → 推論方法」，不要從公式表猜答案。</p>
<h2 id="分配題">機率與分配題</h2>
<ol><li>先寫隨機變數與支撐。</li><li>確認離散／連續、多元與獨立結構。</li><li>邊際化、條件化或變數轉換時先畫支撐。</li><li>最後檢查密度正規化與機率範圍。</li></ol>
<h2 id="抽樣分配題">抽樣分配與極限定理題</h2>
<ol><li>辨認是有限樣本精確結果還是大樣本近似。</li><li>常態母體下再使用 χ²、t、F 的精確結構。</li><li>LLN、CLT、Slutsky、Delta method 要分清各自處理的收斂問題。</li></ol>
<h2 id="估計題">估計題</h2>
<ol><li>先寫 likelihood 或理論動差。</li><li>MLE 檢查支撐、邊界與參數空間。</li><li>比較估計量時分 bias、variance、MSE、一致性與效率。</li><li>充分、完備、Rao–Blackwell、Lehmann–Scheffé 不混用。</li></ol>
<h2 id="檢定題">檢定與線性模型題</h2>
<ol><li>先寫 H0/H1 與方向。</li><li>標出 size、power、p-value 或 likelihood ratio 的角色。</li><li>NP、UMP、LRT 先確認適用假設型態。</li><li>線性模型分清 Gauss–Markov 的 BLUE 條件與常態下精確 t/F 條件。</li></ol>
'''

def appendix_c():
    terms = [
        ('Random Variable','隨機變數'),('CDF','累積分配函數'),('PMF','機率質量函數'),('PDF','機率密度函數'),
        ('Joint Distribution','聯合分配'),('Marginal Distribution','邊際分配'),('Conditional Distribution','條件分配'),
        ('Covariance','共變異數'),('Conditional Expectation','條件期望'),('Multivariate Normal','多元常態'),
        ('Jacobian','Jacobian／雅可比行列式'),('Moment Generating Function','動差母函數'),('Characteristic Function','特徵函數'),
        ('Order Statistic','次序統計量'),('Law of Large Numbers','大數法則'),('Central Limit Theorem','中央極限定理'),
        ('Slutsky Theorem','Slutsky 定理'),('Delta Method','Delta method'),('Sampling Distribution','抽樣分配'),
        ('Likelihood','概似'),('Method of Moments','動差法'),('Maximum Likelihood Estimator','最大概似估計量'),
        ('Sufficient Statistic','充分統計量'),('Completeness','完備性'),('Exponential Family','指數族'),
        ('Bias','偏誤'),('Mean Squared Error','均方誤差'),('Fisher Information','Fisher information'),
        ('Cramér–Rao Lower Bound','Cramér–Rao 下界'),('Rao–Blackwell Theorem','Rao–Blackwell 定理'),
        ('Lehmann–Scheffé Theorem','Lehmann–Scheffé 定理'),('Pivotal Quantity','樞紐量'),('Coverage Probability','覆蓋率'),
        ('Size','檢定大小'),('Power','檢定力'),('Neyman–Pearson Lemma','Neyman–Pearson 引理'),
        ('Uniformly Most Powerful','一致最強力'),('Likelihood-Ratio Test','概似比檢定'),('Wilks Theorem','Wilks 定理'),
        ('Ordinary Least Squares','普通最小平方法'),('Gauss–Markov Theorem','Gauss–Markov 定理'),('BLUE','最佳線性無偏估計量'),
    ]
    rows = ''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en, zh in terms)
    return f'''<h1>附錄 C　中英名詞與符號對照</h1>
<p class="lead">英文題幹常用縮寫與定理名稱。先把名詞對回機率模型、估計或檢定角色，再判斷公式。</p>
<h2 id="機率論">機率論</h2><p>CDF、joint、marginal、conditional、Jacobian 與 convergence 是前半部高頻詞。</p>
<h2 id="數理統計">數理統計</h2><p>Likelihood、sufficiency、information、coverage、power、UMP 與 LRT 是後半部推論主線。</p>
<h2 id="名詞表">名詞表</h2><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>
'''

def search_entries(chapters, appendix_meta):
    entries = []
    fields = [
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
        for page, (title, getter) in enumerate(fields, start=1):
            entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':title,'text':getter(ch)})
    for ch_id,title,text in appendix_meta:
        entries.extend([
            {'chapterId':ch_id,'chapterTitle':title,'page':0,'title':title,'text':text},
            {'chapterId':ch_id,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
            {'chapterId':ch_id,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先辨認模型、支撐與成立條件，再選分配、估計量或檢定，最後檢查有限樣本與漸近結論是否混用。'},
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
    array_end = sw.find('];', idx)
    if array_end < 0:
        raise AssertionError('cannot locate service-worker asset array end')
    insertion = ''.join(f'\n  {json.dumps(p, ensure_ascii=False)},' for p in paths)
    return sw[:array_end] + insertion + '\n' + sw[array_end:]

def main(site_root):
    site = Path(site_root)
    lib_path = site/'data/library.json'
    library = json.loads(lib_path.read_text(encoding='utf-8'))
    pre_ids = [b['id'] for b in library['books']]
    if BOOK in pre_ids:
        raise AssertionError(f'{BOOK} already exists')
    if not pre_ids or pre_ids[-1] != 'money-banking':
        raise AssertionError(f'advanced statistics generator requires money-banking tail, got {pre_ids[-3:]}')

    template_entry = copy.deepcopy(library['books'][-1])
    old_id = template_entry['id']
    template_entry = deep_replace(template_entry, old_id, BOOK)
    template_entry.update({
        'id': BOOK, 'title': TITLE, 'subtitle': SUBTITLE, 'cover': COVER,
        'accent': ACCENT, 'status': 'available',
    })
    for key in ('description','summary'):
        if key in template_entry:
            template_entry[key] = '一般大學高等統計／數理統計核心：機率模型、多元分配、極限定理、抽樣分配、估計與檢定理論。'
    library['books'].append(template_entry)
    lib_path.write_text(jdump(library), encoding='utf-8')

    old_root = site/'books'/old_id
    old_manifest = json.loads((old_root/'manifest.json').read_text(encoding='utf-8'))
    old_questions = json.loads((old_root/'questions.json').read_text(encoding='utf-8'))

    root = site/'books'/BOOK
    chdir = root/'chapters'
    figdir = site/'assets/advanced-statistics-svg'
    chdir.mkdir(parents=True, exist_ok=False)
    figdir.mkdir(parents=True, exist_ok=False)

    chapter_meta = []
    chapter_titles = {}
    for c in CHAPTERS:
        number = str(int(c['id'][2:]))
        rel = f'chapters/{c["id"]}.html'
        (root/rel).write_text(chapter_html(c), encoding='utf-8')
        (figdir/f'{c["slug"]}.svg').write_text(render_svg(c), encoding='utf-8')
        chapter_meta.append({'id':c['id'],'number':number,'title':c['title'],'file':rel,'kind':'chapter'})
        chapter_titles[c['id']] = f'第 {number} 章 {c["title"]}'

    appendices = [
        ('appendix-a','A','核心分配、定理與公式速查','chapters/appendix-a.html',appendix_a(CHAPTERS)),
        ('appendix-b','B','高等統計解題路線','chapters/appendix-b.html',appendix_b()),
        ('appendix-c','C','中英名詞與符號對照','chapters/appendix-c.html',appendix_c()),
    ]
    for cid,number,title,rel,body in appendices:
        (root/rel).write_text(body, encoding='utf-8')
        chapter_meta.append({'id':cid,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest = deep_replace(copy.deepcopy(old_manifest), old_id, BOOK)
    manifest.update({
        'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'version':VERSION,'cover':COVER,
        'accent':ACCENT,'updatedAt':UPDATED_AT,'chapters':chapter_meta,
        'releaseNotes':[{
            'version':VERSION,'date':UPDATED_AT,'title':'新增一般大學高等統計學教材',
            'changes':[
                '新增 20 章正文與 3 份附錄，從必要數學工具、機率模型與多元分配延伸到估計與檢定理論',
                '新增 100 題題庫，每章 5 題，涵蓋標準計算、定理條件、推導辨識與常見陷阱',
                '新增 189 筆搜尋索引與 20 張自製 SVG 結構圖',
                '與既有《統計學》分工：本書聚焦數理統計核心，不重做描述統計與入門推論',
            ],
            'progressImpact':'新增獨立書籍，不改動既有書籍章節、題目 ID、閱讀進度或錯題紀錄。',
        }],
    })
    for key in ('description','summary'):
        if key in manifest:
            manifest[key] = '銜接基礎統計與微積分，建立一般大學高等統計／數理統計的機率、抽樣分配、估計與檢定理論。'
    (root/'manifest.json').write_text(jdump(manifest), encoding='utf-8')

    qtop = deep_replace(copy.deepcopy(old_questions), old_id, BOOK)
    qtop['bookId']=BOOK
    qtop['version']=VERSION
    items=[]
    for src in QUESTIONS:
        slot=src['id'].rsplit('-',1)[-1]
        items.append({
            'id':src['id'],'bookId':BOOK,'chapterId':src['chapterId'],
            'chapterTitle':chapter_titles[src['chapterId']],
            'topic':next(c['title'] for c in CHAPTERS if c['id']==src['chapterId']),
            'difficulty':DIFFICULTY_BY_SLOT[slot],
            'question':src['question'],'answer':src['answer'],'explanation':src['explanation'],
            'source':'本書自編標準題型',
        })
    qtop['count']=len(items); qtop['items']=items
    (root/'questions.json').write_text(jdump(qtop),encoding='utf-8')

    appendix_meta=[
        ('appendix-a','核心分配、定理與公式速查','常用分配、抽樣分配、估計與檢定公式及其成立條件。'),
        ('appendix-b','高等統計解題路線','從模型與支撐到抽樣分配、估計量與檢定的判斷流程。'),
        ('appendix-c','中英名詞與符號對照','高等統計與數理統計常見英文術語、定理名稱與縮寫。'),
    ]
    entries=search_entries(CHAPTERS,appendix_meta)
    (root/'search.json').write_text(jdump({'entries':entries}),encoding='utf-8')

    cache=[
        f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',
        *[f'./books/{BOOK}/{m["file"]}' for m in chapter_meta],
        *[f'./assets/advanced-statistics-svg/{c["slug"]}.svg' for c in CHAPTERS],
    ]
    swp=site/'sw.js'
    swp.write_text(append_sw_assets(swp.read_text(encoding='utf-8'),old_id,cache),encoding='utf-8')
    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':100,'search':len(entries),'figures':20,'pre_books':len(pre_ids),'post_books':len(library['books'])},ensure_ascii=False))

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/generate_advanced_statistics.py SITE_ROOT')
    main(sys.argv[1])
