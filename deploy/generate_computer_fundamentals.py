#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from computer_fundamentals_content_a import CHAPTERS_A
from computer_fundamentals_content_b import CHAPTERS_B
from computer_fundamentals_questions_a import QUESTIONS_A
from computer_fundamentals_questions_b import QUESTIONS_B

BOOK = 'computer-fundamentals'
TITLE = '計算機概論'
SUBTITLE = '資料表示・硬體・作業系統・網路・演算法與資訊科技'
VERSION = '2026.07.29-1'
UPDATED_AT = '2026-07-29'
COVER = '計'
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
<figure class="chapter-figure"><img loading="lazy" src="assets/computer-fundamentals-svg/{fig}" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
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
<title id="title">{safe_title}</title><desc id="desc">{safe_desc}</desc>
<rect width="830" height="390" rx="26" fill="#ffffff"/>
<text x="415" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#1e3a8a">{safe_title}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="415" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先判斷層次與資料流，再做單位、結構或演算法推理。</text>
</svg>\n'''


def appendix_a(chapters):
    rows = []
    for ch in chapters:
        for formula, note in ch['formulas']:
            rows.append(
                f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({html.escape(formula)}\\)</td><td>{html.escape(note)}</td></tr>'
            )
    return '''<h1>附錄 A　數字、資料表示與核心關係速查</h1>
<p class="lead">考前先確認 bit／byte、進位制、整數範圍、資料量與網路速率的單位，再使用公式。計算機概論最常見的錯誤通常是「層次對了、單位卻錯了」。</p>
<h2 id="單位">單位</h2>
<ul><li>1 byte = 8 bits。</li><li>1 kB = 1000 B；1 KiB = 1024 B。</li><li>網路速率常用 bit/s，檔案容量常用 byte。</li></ul>
<h2 id="整數與進位">整數與進位</h2>
<ul><li>n bits 有 2^n 種位元樣式。</li><li>無號 n-bit：0 … 2^n−1。</li><li>二補數 n-bit：−2^(n−1) … 2^(n−1)−1。</li><li>十六進位一位對應四個二進位 bits。</li></ul>
<h2 id="常見資料量">常見資料量</h2>
<p>未壓縮影像可用寬×高×每像素 bits 估算；未壓縮 PCM 類音訊可用取樣率×位元深度×聲道×時間估算。</p>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>關係／公式</th><th>條件與用途</th></tr></thead><tbody>''' + ''.join(rows) + '</tbody></table>\n'


def appendix_b():
    return '''<h1>附錄 B　計算機概論解題路線</h1>
<p class="lead">陌生題先找「它在系統哪一層」，再判斷資料表示、單位與前提。不要看到關鍵字就直接背結論。</p>
<h2 id="進位與容量題">進位與容量題</h2>
<ol><li>先標 base、bit、byte、kB／KiB。</li><li>進位轉換用位值或四位二進位一組。</li><li>資料量題先確認是否未壓縮。</li><li>最後再換成題目要求單位。</li></ol>
<h2 id="硬體與作業系統題">硬體與作業系統題</h2>
<ol><li>先分 CPU、memory、storage、I/O。</li><li>效能題分 clock、instruction count、CPI 與 memory／I/O bottleneck。</li><li>process 與 thread 分清資源邊界。</li><li>virtual memory 題先分 virtual address 與 physical address。</li></ol>
<h2 id="網路題">網路題</h2>
<ol><li>先分 switch／router、MAC／IP。</li><li>再分 DNS、TCP／UDP、TLS、HTTP。</li><li>bandwidth 與 latency 分開。</li><li>傳輸時間先統一 bit 與 byte。</li></ol>
<h2 id="演算法資料題">程式、演算法與資料題</h2>
<ol><li>流程追蹤逐步寫變數。</li><li>Big-O 看輸入規模成長，不當成秒數。</li><li>資料結構依存取／插入／刪除需求選擇。</li><li>資料庫題先找 key、relation 與 transaction。</li></ol>
<h2 id="安全與現代系統題">安全、AI 與現代系統題</h2>
<ol><li>資安先標 CIA、authentication、authorization。</li><li>hash 與 encryption 分開。</li><li>AI 先分 training、inference 與 evaluation。</li><li>cloud／distributed 題記得網路延遲、部分故障與一致性成本。</li></ol>
'''


def appendix_c():
    terms = [
        ('Computer Science','計算機科學'),('Hardware','硬體'),('Software','軟體'),('Algorithm','演算法'),('Bit','位元'),('Byte','位元組'),
        ('Binary','二進位'),('Hexadecimal','十六進位'),("Two’s Complement",'二補數'),('Floating Point','浮點數'),('Unicode','統一碼'),('Sampling','取樣'),
        ('Boolean Logic','布林邏輯'),('Logic Gate','邏輯閘'),('CPU','中央處理器'),('ALU','算術邏輯單元'),('Register','暫存器'),('ISA','指令集架構'),
        ('Cache','快取'),('RAM','主記憶體'),('Locality','區域性'),('Input/Output','輸入輸出'),('Device Driver','裝置驅動程式'),('Interrupt','中斷'),
        ('Operating System','作業系統'),('Kernel','核心'),('Process','程序／行程'),('Thread','執行緒'),('Concurrency','並行'),('Parallelism','平行'),
        ('Virtual Memory','虛擬記憶體'),('Page Fault','缺頁'),('File System','檔案系統'),('Virtual Machine','虛擬機'),('Container','容器'),
        ('Packet','封包'),('Bandwidth','頻寬'),('Latency','延遲'),('Router','路由器'),('DNS','網域名稱系統'),('TCP','傳輸控制協定'),('UDP','使用者資料報協定'),
        ('HTTP','超文字傳輸協定'),('TLS','傳輸層安全性協定'),('Compiler','編譯器'),('Interpreter','直譯器'),('Big-O','漸近成長記號'),
        ('Array','陣列'),('Linked List','鏈結串列'),('Stack','堆疊'),('Queue','佇列'),('Hash Table','雜湊表'),('Database','資料庫'),('Primary Key','主鍵'),('Foreign Key','外鍵'),
        ('Transaction','交易'),('API','應用程式介面'),('Version Control','版本控制'),('Regression Test','回歸測試'),('Authentication','認證'),('Authorization','授權'),
        ('Encryption','加密'),('Hashing','雜湊'),('Machine Learning','機器學習'),('Training','訓練'),('Inference','推論'),('Cloud Computing','雲端運算'),('Edge Computing','邊緣運算'),
        ('IoT','物聯網'),('Privacy','隱私'),('Open Source','開放原始碼'),('Accessibility','可近用性'),
    ]
    rows = ''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en, zh in terms)
    return f'''<h1>附錄 C　中英名詞對照</h1>
<p class="lead">計算機概論英文縮寫很多。考試先把名詞放回正確層次，比死背中文翻譯更可靠。</p>
<h2 id="硬體系統">硬體與系統</h2><p>CPU、ALU、register、cache、RAM、process、thread、virtual memory 分屬不同抽象層，不能互換。</p>
<h2 id="網路資料">網路與資料</h2><p>Bandwidth 與 latency、DNS 與 HTTP、TCP 與 UDP 都是高頻對照。</p>
<h2 id="軟體安全">軟體、安全與 AI</h2><p>Compiler、algorithm、API、hashing、encryption、training 與 inference 要分清功能。</p>
<h2 id="名詞表">名詞表</h2><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>
'''


def search_entries(chapters):
    entries = []
    fields = [
        ('正式定義與核心概念', lambda c: ' '.join(f'{a}：{b}' for a, b in c['definitions'])),
        ('核心公式與成立條件', lambda c: ' '.join(f'{a}；{b}' for a, b in c['formulas'])),
        ('完整標準例題', lambda c: ' '.join(c['example'])),
        ('常見錯誤', lambda c: ' '.join(c['traps'])),
        ('考試判斷方法', lambda c: ' '.join(c['exam'])),
        ('理解檢查', lambda c: ' '.join(c['checks'])),
    ]
    for ch in chapters:
        entries.append({'chapterId': ch['id'], 'chapterTitle': ch['title'], 'page': 0, 'title': ch['title'], 'text': ch['problem'] + ' ' + ' '.join(ch['intuition'])})
        for page, (title, getter) in enumerate(fields, start=1):
            entries.append({'chapterId': ch['id'], 'chapterTitle': ch['title'], 'page': page, 'title': title, 'text': getter(ch)})
    appendix = [
        ('appendix-a','數字、資料表示與核心關係速查','bit／byte、進位制、整數範圍、資料量、CPU、記憶體、網路與資料庫核心關係速查。'),
        ('appendix-b','計算機概論解題路線','進位、硬體、OS、網路、演算法、資料、安全與 AI 的判斷流程。'),
        ('appendix-c','中英名詞對照','計算機概論常見英文縮寫與繁體中文對照。'),
    ]
    for cid, title, text in appendix:
        entries.extend([
            {'chapterId':cid,'chapterTitle':title,'page':0,'title':title,'text':text},
            {'chapterId':cid,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
            {'chapterId':cid,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先定位抽象層，再確認資料格式、單位與前提，最後做計算或結構判斷。'},
        ])
    entries.append({'chapterId':'appendix-b','chapterTitle':'計算機概論解題路線','page':3,'title':'全書快速定位','text':'位元先看格式，硬體先看資料流，OS 先分資源，網路先分層，演算法先看成長，安全先看 CIA，AI 先分訓練與推論。'})
    assert len(entries) == 150
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
    lib_path = site / 'data/library.json'
    if not lib_path.is_file():
        raise SystemExit(f'library not found: {lib_path}')
    library = json.loads(lib_path.read_text(encoding='utf-8'))
    pre_ids = [b['id'] for b in library['books']]
    if BOOK in pre_ids:
        raise AssertionError(f'{BOOK} already exists')
    if not pre_ids:
        raise AssertionError('computer fundamentals generator needs an existing canonical library to clone UI metadata')

    old_id = pre_ids[-1]
    template_entry = deep_replace(copy.deepcopy(library['books'][-1]), old_id, BOOK)
    template_entry.update({'id': BOOK, 'title': TITLE, 'subtitle': SUBTITLE, 'cover': COVER, 'accent': ACCENT, 'status': 'available'})
    if 'version' in template_entry:
        template_entry['version'] = VERSION
    for key in ('description', 'summary'):
        if key in template_entry:
            template_entry[key] = '一般大學計算機概論：資料表示、硬體、作業系統、網路、程式與演算法、資料庫、資安、AI 與現代運算平台。'
    library['books'].append(template_entry)
    lib_path.write_text(jdump(library), encoding='utf-8')

    old_root = site / 'books' / old_id
    old_manifest = json.loads((old_root / 'manifest.json').read_text(encoding='utf-8'))
    old_questions = json.loads((old_root / 'questions.json').read_text(encoding='utf-8'))
    root = site / 'books' / BOOK
    chdir = root / 'chapters'
    figdir = site / 'assets/computer-fundamentals-svg'
    chdir.mkdir(parents=True, exist_ok=False)
    figdir.mkdir(parents=True, exist_ok=False)

    assert len(CHAPTERS) == 20
    assert [c['id'] for c in CHAPTERS] == [f'ch{i:02d}' for i in range(20)]
    assert len(QUESTIONS) == 100

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
        ('appendix-a','A','數字、資料表示與核心關係速查','chapters/appendix-a.html',appendix_a(CHAPTERS)),
        ('appendix-b','B','計算機概論解題路線','chapters/appendix-b.html',appendix_b()),
        ('appendix-c','C','中英名詞對照','chapters/appendix-c.html',appendix_c()),
    ]
    for cid, number, title, rel, body in appendices:
        (root / rel).write_text(body, encoding='utf-8')
        chapter_meta.append({'id':cid,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest = deep_replace(copy.deepcopy(old_manifest), old_id, BOOK)
    manifest.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'version':VERSION,'cover':COVER,'accent':ACCENT,'updatedAt':UPDATED_AT,'chapters':chapter_meta,'features':{'reader':True,'quiz':True,'formula':True}})
    manifest['releaseNotes'] = [{
        'version': VERSION,
        'date': UPDATED_AT,
        'title': '新增一般大學計算機概論教材',
        'changes': ['新增 20 章正文與 3 份附錄','新增 100 題題庫、150 筆搜尋索引與 20 張自製 SVG','進位、二補數、CPU、虛擬記憶體、TCP／UDP、Big-O、密碼雜湊與 AI 採精確條件式敘述'],
        'progressImpact': '新增獨立書籍，不改動既有書籍章節 ID、題目 ID 或閱讀進度。',
    }]
    for key in ('description','summary'):
        if key in manifest:
            manifest[key] = '從近零基礎銜接一般大學計算機概論，建立資料表示、硬體、系統、網路、程式、資料與資訊安全的完整地圖。'
    (root / 'manifest.json').write_text(jdump(manifest), encoding='utf-8')

    qtop = deep_replace(copy.deepcopy(old_questions), old_id, BOOK)
    qtop['bookId'] = BOOK
    qtop['version'] = VERSION
    qitems = []
    for src in QUESTIONS:
        slot = src['id'].rsplit('-', 1)[-1]
        qitems.append({
            'id':src['id'],'bookId':BOOK,'chapterId':src['chapterId'],
            'chapterTitle':chapter_titles[src['chapterId']],
            'topic':next(ch['title'] for ch in CHAPTERS if ch['id'] == src['chapterId']),
            'difficulty':DIFFICULTY_BY_SLOT[slot],
            'question':src['question'],'answer':src['answer'],'explanation':src['explanation'],
            'source':'本書自編標準題型',
        })
    assert len({x['id'] for x in qitems}) == 100
    qtop['count'] = len(qitems)
    qtop['items'] = qitems
    (root / 'questions.json').write_text(jdump(qtop), encoding='utf-8')

    entries = search_entries(CHAPTERS)
    (root / 'search.json').write_text(jdump({'entries':entries}), encoding='utf-8')

    cache = [f'./books/{BOOK}/manifest.json', f'./books/{BOOK}/questions.json', f'./books/{BOOK}/search.json']
    cache += [f'./books/{BOOK}/{x["file"]}' for x in chapter_meta]
    cache += [f'./assets/computer-fundamentals-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    sw_path = site / 'sw.js'
    sw_path.write_text(append_sw_assets(sw_path.read_text(encoding='utf-8'), old_id, cache), encoding='utf-8')

    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':len(qitems),'search':len(entries),'figures':len(CHAPTERS),'pre_books':len(pre_ids),'post_books':len(library['books'])}, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/generate_computer_fundamentals.py SITE_ROOT')
    main(sys.argv[1])
