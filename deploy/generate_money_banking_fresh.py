#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from money_banking_content import CHAPTERS
from money_banking_questions import build_questions

BOOK='money-banking'
TITLE='貨幣銀行學'
SUBTITLE='貨幣・金融市場・銀行・中央銀行與貨幣政策'
VERSION='2026.07.29-1'
UPDATED_AT='2026-07-29'
COVER='貨'
ACCENT='#0f766e'
DIFFICULTY_BY_SLOT={'q01':'基礎','q02':'標準','q03':'標準','q04':'進階','q05':'進階'}


def jdump(obj):
    return json.dumps(obj,ensure_ascii=False,indent=2)+'\n'


def deep_replace(value,old,new):
    if isinstance(value,str): return value.replace(old,new)
    if isinstance(value,list): return [deep_replace(v,old,new) for v in value]
    if isinstance(value,dict): return {k:deep_replace(v,old,new) for k,v in value.items()}
    return value


def clean_math(s):
    # The content source intentionally stays readable Python; repair the few control
    # escapes that Python string literals interpret before rendering LaTeX.
    return s.replace('\t',r'\times').replace('\a',r'\approx').replace('\f',r'\frac').replace('\x0b',r'\vphantom')


def ul(items):
    return '<ul>'+''.join(f'<li>{html.escape(x)}</li>' for x in items)+'</ul>'


def chapter_html(ch):
    defs=''.join(f'<dt>{html.escape(term)}</dt><dd>{html.escape(desc)}</dd>' for term,desc in ch['definitions'])
    formulas=''.join(
        f'<div class="formula-card"><p class="math display">\\[{html.escape(clean_math(formula))}\\]</p><p>{html.escape(note)}</p></div>'
        for formula,note in ch['formulas']
    )
    intuition=''.join(f'<p>{html.escape(p)}</p>' for p in ch['intuition'])
    example=''.join(f'<p>{html.escape(p)}</p>' for p in ch['example'])
    checks=''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    identity = '<p><strong>資產負債表速記：</strong>銀行最基本的恆等式可寫成「資產＝負債＋權益」。</p>' if ch['id'] in {'ch00','ch06'} else ''
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/money-banking-svg/{ch['slug']}.svg" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
<h2 id="本章要解決的問題">本章要解決的問題</h2>
<p>{html.escape(ch['problem'])}</p>
<h2 id="白話直覺">白話直覺</h2>
{intuition}
{identity}
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
    title,labels=ch['figure']
    xs=[50,245,440,635]
    boxes=[]; arrows=[]
    for i,(x,label) in enumerate(zip(xs,labels)):
        boxes.append(f'<rect x="{x}" y="150" width="150" height="92" rx="18" fill="#ecfdf5" stroke="#0f766e" stroke-width="3"/><text x="{x+75}" y="199" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#134e4a">{xml_escape(label)}</text>')
        if i<3:
            arrows.append(f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#64748b" stroke-width="4"/><polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#64748b"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 835 390" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(' → '.join(labels))}</desc>
<rect width="835" height="390" rx="26" fill="#ffffff"/>
<text x="417" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#134e4a">{xml_escape(title)}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="417" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先看資產負債表與機制，再判斷利率、風險與政策傳遞。</text>
</svg>\n'''


def appendix_a(chapters):
    rows=[]
    for ch in chapters:
        for formula,note in ch['formulas']:
            rows.append(f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({html.escape(clean_math(formula))}\\)</td><td>{html.escape(note)}</td></tr>')
    return '''<h1>附錄 A　核心公式與銀行報表速查</h1>
<p class="lead">考前先用這份附錄確認符號與條件。貨幣銀行學最常見的失分，不是算術，而是把不同層級的資產負債表、利率口徑或模型條件混在一起。</p>
<h2 id="資產負債表">資產負債表</h2>
<p>銀行速記：<strong>資產＝負債＋權益</strong>。中央銀行也遵守資產負債表恆等，但銀行準備對商業銀行是資產、對中央銀行則是負債。準備貨幣可用 B=C+R 的簡化式理解；銀行準備 R 只是準備貨幣的組成之一。</p>
<h2 id="貨幣與乘數">貨幣與乘數</h2>
<p>M1A、M1B、M2 是由窄到廣的貨幣總計數。1/rr 只稱簡單存款乘數；一般示意式 m=(1+c)/(rr+e+c) 仍會隨通貨持有、超額準備與銀行行為改變，不能當成現實世界固定常數。</p>
<h2 id="利率與匯率">利率與匯率</h2>
<p>Fisher 精確式為 (1+i)=(1+r)(1+π^e)，低通膨才常用 i≈r+π^e。本書匯率固定 E=NT$/US$；E 上升表示新臺幣貶值。</p>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>公式／關係</th><th>成立條件與用途</th></tr></thead><tbody>'''+''.join(rows)+'</tbody></table>\n'


def appendix_b():
    return '''<h1>附錄 B　貨幣銀行學解題路線</h1>
<p class="lead">陌生題不要先猜政策方向。先確定是哪一層資產負債表，再確認價格／利率定義，最後才做行為與政策判斷。</p>
<h2 id="銀行題">銀行與信用題</h2>
<ol><li>列銀行資產、負債、權益，先維持資產＝負債＋權益。</li><li>放款入帳時分清放款資產與存款負債；跨行支付再追準備清算。</li><li>把資本限制、流動性、信用風險、資金成本與信用需求一起檢查。</li><li>若出現擠兌，先分流動性不足與資不抵債；最後貸款者不是無條件救助。</li></ol>
<h2 id="債券利率題">債券與利率題</h2>
<ol><li>先畫現金流時間軸。</li><li>分票面利率、當期收益率、YTM 與持有期間報酬。</li><li>價格敏感度用修正存續期間時，只把它當小幅殖利率變動的一階近似。</li><li>殖利率曲線分成未來短率預期與期限溢酬，不把反轉寫成必然衰退。</li></ol>
<h2 id="貨幣政策題">中央銀行與政策題</h2>
<ol><li>先寫央行工具：公開市場操作、準備制度、貼現／融通與其他制度工具。</li><li>再看銀行準備與隔夜利率，分走廊或準備充裕的地板型直覺。</li><li>政策利率之後至少追一條利率／信用／資產價格／匯率／預期傳遞。</li><li>QE 分會計效果、金融市場效果與最終支出效果；準備增加不等於固定乘數 M2。</li></ol>
<h2 id="通膨開放經濟題">通膨與開放經濟題</h2>
<ol><li>Fisher 題先辨認精確式或近似式，再分 equation 與 effect。</li><li>Phillips 題先寫預期、產出缺口與供給衝擊。</li><li>匯率第一行固定 E=NT$/US$；E 上升＝新臺幣貶值。</li><li>外匯干預再問是否沖銷；不可能三角則逐一標出固定匯率、資本流動與政策自主。</li></ol>
<p>最後檢查：單位是否一致、百分點是否轉成小數、存量與流量是否混用、結論是否漏掉制度與成立條件。</p>
'''


def appendix_c():
    terms=[
      ('Money','貨幣'),('Medium of Exchange','交易媒介'),('Unit of Account','計價單位'),('Store of Value','價值儲藏'),('Liquidity','流動性'),
      ('Monetary Aggregates','貨幣總計數'),('Present Value','現值'),('Yield to Maturity','到期殖利率'),('Holding-Period Return','持有期間報酬率'),('Duration','存續期間'),('Term Premium','期限溢酬'),
      ('Direct Finance','直接金融'),('Indirect Finance','間接金融'),('Adverse Selection','逆選擇'),('Moral Hazard','道德危險'),('Financial Intermediary','金融中介'),
      ('Bank Reserves','銀行準備'),('Reserve Money / Base Money','準備貨幣／貨幣基數'),('Deposit Creation','存款創造'),('Simple Deposit Multiplier','簡單存款乘數'),('Currency–Deposit Ratio','通貨—存款比率'),
      ('Return on Assets','資產報酬率 ROA'),('Return on Equity','權益報酬率 ROE'),('Repricing Gap','重新訂價缺口'),('Deposit Insurance','存款保險'),('Lender of Last Resort','最後貸款者'),
      ('Microprudential Supervision','個體審慎監理'),('Macroprudential Policy','總體審慎政策'),('Central Bank','中央銀行'),('Open Market Operations','公開市場操作'),('Discount Window','貼現窗口'),
      ('Interest-Rate Corridor','利率走廊'),('Floor System','地板型制度'),('Monetary Policy Transmission','貨幣政策傳遞'),('Fisher Equation','Fisher 關係式'),('Fisher Effect','Fisher effect'),
      ('Phillips Curve','Phillips curve'),('Taylor Principle','Taylor principle'),('Time Inconsistency','時間不一致'),('Effective Lower Bound','有效下限'),('Quantitative Easing','量化寬鬆'),('Forward Guidance','前瞻指引'),
      ('Exchange Rate','匯率'),('Sterilization','沖銷'),('Impossible Trinity','不可能三角'),('Capital Flow','資本流動'),('Foreign-Exchange Intervention','外匯干預')
    ]
    rows=''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en,zh in terms)
    return f'''<h1>附錄 C　中英名詞對照</h1>
<p class="lead">英文題幹最容易在相近名詞上失分。先確認本書固定用語，再進公式與政策方向。</p>
<h2 id="貨幣金融市場">貨幣與金融市場</h2><p>Money、liquidity、yield、duration 與 term premium 要分層理解；yield 不等於所有形式的實際報酬。</p>
<h2 id="銀行央行政策">銀行、中央銀行與政策</h2><p>Bank reserves、base money、deposit creation、open market operations 與 lender of last resort 分屬不同層級，不能互換。</p>
<h2 id="開放經濟">開放經濟</h2><p>Exchange rate 必須先固定報價。本書固定 E=NT$/US$；sterilization 是沖銷外匯干預對國內準備的影響。</p>
<h2 id="名詞表">名詞表</h2><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>
'''


def search_entries(chapters):
    entries=[]
    fields=[
      ('正式定義與核心概念',lambda c:' '.join(f'{a}：{b}' for a,b in c['definitions'])),
      ('核心公式與成立條件',lambda c:' '.join(f'{clean_math(a)}；{b}' for a,b in c['formulas'])),
      ('完整標準例題',lambda c:' '.join(c['example'])),
      ('常見錯誤',lambda c:' '.join(c['traps'])),
      ('考試判斷方法',lambda c:' '.join(c['exam'])),
      ('理解檢查',lambda c:' '.join(c['checks'])),
    ]
    for ch in chapters:
        entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':0,'title':ch['title'],'text':ch['problem']+' '+' '.join(ch['intuition'])})
        for page,(title,getter) in enumerate(fields,start=1):
            entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':title,'text':getter(ch)})
    appendix=[
      ('appendix-a','核心公式與銀行報表速查','資產＝負債＋權益、M1A／M1B／M2、Fisher、簡單存款乘數、一般貨幣乘數與 E=NT$/US$ 的公式速查。'),
      ('appendix-b','貨幣銀行學解題路線','銀行、債券、貨幣政策、通膨與開放經濟題的判斷流程。'),
      ('appendix-c','中英名詞對照','Money and Banking 常見英文術語與繁體中文對照。'),
    ]
    for cid,title,text in appendix:
        entries.extend([
          {'chapterId':cid,'chapterTitle':title,'page':0,'title':title,'text':text},
          {'chapterId':cid,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
          {'chapterId':cid,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先固定符號與資產負債表層級，再選公式，最後檢查制度條件、方向與單位。'},
        ])
    entries.append({'chapterId':'appendix-b','chapterTitle':'貨幣銀行學解題路線','page':3,'title':'全書快速定位','text':'債券先折現，銀行先畫資產負債表，貨幣乘數先看假設，政策先追傳遞，匯率先固定 E=NT$/US$。'})
    assert len(entries)==150
    return entries


def append_sw_assets(sw,old_id,paths):
    if paths[0] in sw: return sw
    needle=f'./books/{old_id}/manifest.json'; idx=sw.find(needle)
    if idx<0: raise AssertionError(f'cannot locate existing book cache entry for {old_id}')
    starts=list(re.finditer(r'const\s+[A-Za-z0-9_$]+\s*=\s*\[',sw[:idx]))
    if not starts: raise AssertionError('cannot locate service-worker asset array')
    array_start=starts[-1].end()-1; array_end=sw.find('];',idx)
    if array_end<0: raise AssertionError('cannot locate service-worker asset array end')
    body=sw[array_start+1:array_end]
    insertion=''.join(f'\n  {json.dumps(p,ensure_ascii=False)},' for p in paths)
    if body.rstrip().endswith(','): insertion=insertion.lstrip('\n')
    return sw[:array_end]+insertion+'\n'+sw[array_end:]


def main(site_root):
    site=Path(site_root); lib_path=site/'data/library.json'
    if not lib_path.is_file(): raise SystemExit(f'library not found: {lib_path}')
    library=json.loads(lib_path.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in library['books']]
    if BOOK in pre_ids: raise AssertionError(f'{BOOK} already exists')
    if len(pre_ids)!=11 or pre_ids[-1]!='public-finance': raise AssertionError(f'fresh money generator expects current eleven-book public-finance tail: {pre_ids}')

    template_entry=copy.deepcopy(library['books'][-1]); old_id=template_entry['id']; template_entry=deep_replace(template_entry,old_id,BOOK)
    template_entry.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'cover':COVER,'accent':ACCENT,'status':'available'})
    if 'version' in template_entry: template_entry['version']=VERSION
    for key in ('description','summary'):
        if key in template_entry: template_entry[key]='一般大學貨幣銀行學：貨幣、利率、金融市場、銀行、中央銀行、貨幣政策、通膨與開放經濟。'
    library['books'].append(template_entry); lib_path.write_text(jdump(library),encoding='utf-8')

    old_root=site/'books'/old_id
    old_manifest=json.loads((old_root/'manifest.json').read_text(encoding='utf-8'))
    old_questions=json.loads((old_root/'questions.json').read_text(encoding='utf-8'))
    root=site/'books'/BOOK; chdir=root/'chapters'; figdir=site/'assets/money-banking-svg'
    chdir.mkdir(parents=True,exist_ok=False); figdir.mkdir(parents=True,exist_ok=False)

    chapter_meta=[]; chapter_titles={}
    for ch in CHAPTERS:
        number=str(int(ch['id'][2:])); rel=f'chapters/{ch["id"]}.html'
        (root/rel).write_text(chapter_html(ch),encoding='utf-8')
        (figdir/f'{ch["slug"]}.svg').write_text(render_svg(ch),encoding='utf-8')
        chapter_meta.append({'id':ch['id'],'number':number,'title':ch['title'],'file':rel,'kind':'chapter'})
        chapter_titles[ch['id']]=f'第 {number} 章 {ch["title"]}'

    appendices=[
      ('appendix-a','A','核心公式與銀行報表速查','chapters/appendix-a.html',appendix_a(CHAPTERS)),
      ('appendix-b','B','貨幣銀行學解題路線','chapters/appendix-b.html',appendix_b()),
      ('appendix-c','C','中英名詞對照','chapters/appendix-c.html',appendix_c()),
    ]
    for cid,number,title,rel,body in appendices:
        (root/rel).write_text(body,encoding='utf-8'); chapter_meta.append({'id':cid,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest=deep_replace(copy.deepcopy(old_manifest),old_id,BOOK)
    manifest.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'version':VERSION,'cover':COVER,'accent':ACCENT,'updatedAt':UPDATED_AT,'chapters':chapter_meta,'features':{'reader':True,'quiz':True,'formula':True}})
    manifest['releaseNotes']=[{'version':VERSION,'date':UPDATED_AT,'title':'新增一般大學貨幣銀行學教材','changes':['新增 20 章正文與 3 份附錄','新增 100 題題庫、150 筆搜尋索引與 20 張自製 SVG','貨幣乘數、放款創造存款、央行工具、Fisher、QE 與匯率方向採精確條件式敘述'],'progressImpact':'新增獨立書籍，不改動既有書籍章節 ID、題目 ID 或閱讀進度。'}]
    for key in ('description','summary'):
        if key in manifest: manifest[key]='從近零基礎銜接一般大學貨幣銀行學，涵蓋貨幣、債券利率、金融中介、銀行風險、中央銀行與貨幣政策。'
    (root/'manifest.json').write_text(jdump(manifest),encoding='utf-8')

    raw_questions=build_questions(); qtop=deep_replace(copy.deepcopy(old_questions),old_id,BOOK); qtop['bookId']=BOOK; qtop['version']=VERSION
    qitems=[]
    for src in raw_questions:
        slot=src['id'].rsplit('-',1)[-1]
        qitems.append({'id':src['id'],'bookId':BOOK,'chapterId':src['chapterId'],'chapterTitle':chapter_titles[src['chapterId']],'topic':next(ch['title'] for ch in CHAPTERS if ch['id']==src['chapterId']),'difficulty':DIFFICULTY_BY_SLOT[slot],'question':src['question'],'answer':src['answer'],'explanation':src['explanation'],'source':'本書自編標準題型'})
    qtop['count']=len(qitems); qtop['items']=qitems; (root/'questions.json').write_text(jdump(qtop),encoding='utf-8')

    entries=search_entries(CHAPTERS); (root/'search.json').write_text(jdump({'entries':entries}),encoding='utf-8')
    cache=[f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json']
    cache += [f'./books/{BOOK}/{x["file"]}' for x in chapter_meta]
    cache += [f'./assets/money-banking-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    sw_path=site/'sw.js'; sw_path.write_text(append_sw_assets(sw_path.read_text(encoding='utf-8'),old_id,cache),encoding='utf-8')
    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':len(qitems),'search':len(entries),'figures':len(CHAPTERS),'pre_books':len(pre_ids),'post_books':len(library['books'])},ensure_ascii=False))

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/generate_money_banking_fresh.py SITE_ROOT')
    main(sys.argv[1])
