#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from industrial_economics_content import CHAPTERS
from industrial_economics_questions import build_questions

BOOK='industrial-economics'
TITLE='產業經濟學'
SUBTITLE='市場結構・策略競爭・廠商行為與競爭政策'
VERSION='2026.07.29-1'
UPDATED_AT='2026-07-29'
COVER='產'
ACCENT='#7c3aed'
DIFFICULTY_BY_SLOT={'q01':'基礎','q02':'標準','q03':'標準','q04':'進階','q05':'進階'}


def jdump(obj):
    return json.dumps(obj,ensure_ascii=False,indent=2)+'\n'


def deep_replace(value,old,new):
    if isinstance(value,str): return value.replace(old,new)
    if isinstance(value,list): return [deep_replace(v,old,new) for v in value]
    if isinstance(value,dict): return {k:deep_replace(v,old,new) for k,v in value.items()}
    return value


def ul(items):
    return '<ul>'+''.join(f'<li>{html.escape(x)}</li>' for x in items)+'</ul>'


def chapter_html(ch):
    defs=''.join(f'<dt>{html.escape(term)}</dt><dd>{html.escape(desc)}</dd>' for term,desc in ch['definitions'])
    formulas=''.join(
        f'<div class="formula-card"><p class="math display">\\[{html.escape(formula)}\\]</p><p>{html.escape(note)}</p></div>'
        for formula,note in ch['formulas']
    )
    intuition=''.join(f'<p>{html.escape(p)}</p>' for p in ch['intuition'])
    example=''.join(f'<p>{html.escape(p)}</p>' for p in ch['example'])
    checks=''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/industrial-economics-svg/{ch['slug']}.svg" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
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
    title,labels=ch['figure']
    xs=[50,245,440,635]
    boxes=[]; arrows=[]
    for i,(x,label) in enumerate(zip(xs,labels)):
        boxes.append(f'<rect x="{x}" y="150" width="150" height="92" rx="18" fill="#f5f3ff" stroke="#7c3aed" stroke-width="3"/><text x="{x+75}" y="199" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#5b21b6">{xml_escape(label)}</text>')
        if i<3:
            arrows.append(f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#64748b" stroke-width="4"/><polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#64748b"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 835 390" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(' → '.join(labels))}</desc>
<rect width="835" height="390" rx="26" fill="#ffffff"/>
<text x="417" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#5b21b6">{xml_escape(title)}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="417" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先固定市場與模型假設，再追廠商誘因、策略互動與市場結果。</text>
</svg>\n'''


def appendix_a(chapters):
    rows=[]
    for ch in chapters:
        for formula,note in ch['formulas']:
            rows.append(f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({html.escape(formula)}\\)</td><td>{html.escape(note)}</td></tr>')
    return '''<h1>附錄 A　核心公式與模型速查</h1>
<p class="lead">產業經濟學最容易失分的地方不是公式太多，而是把不同模型的決策變數、時序與市場假設混在一起。考前先用本表固定「什麼模型在什麼條件下能用」。</p>
<h2 id="模型先決條件">模型先決條件</h2>
<ul><li>市場力量題：先界定相關市場，再看需求替代、進入與成本。</li><li>獨占：內點最適先用 MR=MC 求量，再回需求求價格。</li><li>Cournot：同時選數量；Bertrand：同時選價格；Stackelberg：有先後時序且先期行動需具承諾效果。</li><li>合謀：比較合作、單次偏離與未來懲罰；平台：至少同時看兩側與跨邊外部性。</li></ul>
<h2 id="指標尺度">指標尺度</h2>
<p>HHI 若以百分比市占率計算，範圍 0–10,000；若以 0–1 比例計算，範圍 0–1。兩種口徑不可混算。Delta HHI=2s_As_B 的捷徑同樣要固定市占尺度。</p>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>公式／關係</th><th>成立條件與用途</th></tr></thead><tbody>'''+''.join(rows)+'</tbody></table>\n'


def appendix_b():
    return '''<h1>附錄 B　產業經濟學解題路線</h1>
<p class="lead">陌生題先判斷競爭機制，不要先猜「這是獨占還是寡占」。同一個少數廠商市場，在數量競爭、價格競爭、差異化與序列決策下會得到不同答案。</p>
<h2 id="市場結構題">市場界定與市場結構題</h2>
<ol><li>先界定產品、地理與交易範圍。</li><li>確認市占率是銷量還是銷售額，再算 CRn／HHI。</li><li>補需求替代、進入障礙、買方力量與容量；集中度只是一部分證據。</li></ol>
<h2 id="定價寡占題">定價與寡占題</h2>
<ol><li>獨占先 MR=MC，再回需求找 P。</li><li>Cournot 找數量最佳反應交點；Bertrand 先檢查同質、成本與容量假設；Stackelberg 從跟隨者反應向後歸納。</li><li>價格歧視先確認市場力量、分群／自我選擇與防套利條件。</li></ol>
<h2 id="進入策略題">進入、合謀、垂直與併購題</h2>
<ol><li>進入先分固定成本與沉沒成本，再檢查威脅是否可信。</li><li>合謀比較合作、偏離與懲罰現值。</li><li>垂直安排同時寫效率與排除機制；併購依序看市場界定、單邊／協調效果、進入與效率。</li></ol>
<h2 id="平台實證政策題">平台、實證與政策題</h2>
<ol><li>平台畫出兩側與跨邊外部性，不能只看單邊價格。</li><li>資料題先分描述相關與因果識別。</li><li>競爭政策最後才把經濟機制放回現行法規；易變申報門檻以公平交易委員會最新公開資料為準。</li></ol>
<p>最後檢查：市場定義是否一致、模型假設是否符合、百分比尺度是否混用、比較的是觀察值還是正確反事實。</p>
'''


def appendix_c():
    terms=[
      ('Industrial Organization','產業組織／產業經濟學'),('Market Structure','市場結構'),('Conduct','廠商行為'),('Performance','市場績效'),('Relevant Market','相關市場'),('Market Share','市場占有率'),('Concentration Ratio','集中率'),('HHI','赫芬達爾—赫希曼指數'),('Market Power','市場力量'),('Lerner Index','勒納指數'),
      ('Economies of Scale','規模經濟'),('Minimum Efficient Scale','最低效率規模'),('Economies of Scope','範疇經濟'),('Sunk Cost','沉沒成本'),('Natural Monopoly','自然獨占'),('Price Discrimination','價格歧視'),('Two-Part Tariff','兩部定價'),('Best Response','最佳反應'),('Nash Equilibrium','Nash 均衡'),('Strategic Substitute','策略替代'),
      ('Cournot Competition','Cournot 數量競爭'),('Bertrand Competition','Bertrand 價格競爭'),('Stackelberg Competition','Stackelberg 序列競爭'),('Credible Commitment','可信承諾'),('Product Differentiation','產品差異化'),('Horizontal Differentiation','水平差異化'),('Vertical Differentiation','垂直差異化'),('Hotelling Model','Hotelling 空間模型'),('Monopolistic Competition','獨占性競爭'),('Business Stealing','商業攫取'),
      ('Entry Barrier','進入障礙'),('Limit Pricing','極限定價'),('Predatory Pricing','掠奪性定價'),('Recoupment','可回收性'),('Cartel','卡特爾'),('Tacit Coordination','默契協調'),('Repeated Game','重複賽局'),('Discount Factor','折現因子'),('Vertical Integration','垂直整合'),('Double Marginalization','雙重加價'),
      ('Resale Price Maintenance','轉售價格維持'),('Exclusive Dealing','獨家交易'),('Unilateral Effects','單邊效果'),('Coordinated Effects','協調效果'),('Advertising','廣告'),('Search Cost','搜尋成本'),('Signaling','信號'),('R&D','研究發展'),('Knowledge Spillover','知識外溢'),('Network Effect','網路效果'),
      ('Two-Sided Market','兩邊市場'),('Multi-homing','多歸屬'),('Competition Policy','競爭政策'),('Concerted Action','聯合行為'),('Identification','因果辨識'),('Reduced Form','簡化式'),('Structural Model','結構式模型'),('Counterfactual','反事實')
    ]
    rows=''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en,zh in terms)
    return f'''<h1>附錄 C　中英名詞對照</h1>
<p class="lead">產業經濟學英文題幹常把相近模型放在同一題。先辨認 competition variable、timing、entry 與 differentiation，再進公式。</p>
<h2 id="市場結構策略">市場結構與策略</h2><p>Market power 不等於 market share；Cournot、Bertrand 與 Stackelberg 的差異首先在決策變數與時序。</p>
<h2 id="競爭政策實證">競爭政策與實證</h2><p>Concentration、concerted action、counterfactual 與 identification 分屬結構描述、制度行為、政策比較與因果研究，不可互換。</p>
<h2 id="名詞表">名詞表</h2><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>
'''


def search_entries(chapters):
    entries=[]
    fields=[
      ('正式定義與核心概念',lambda c:' '.join(f'{a}：{b}' for a,b in c['definitions'])),
      ('核心公式與成立條件',lambda c:' '.join(f'{a}；{b}' for a,b in c['formulas'])),
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
      ('appendix-a','核心公式與模型速查','HHI、Lerner、MR=MC、Cournot、Bertrand、Stackelberg、Hotelling、重複賽局、Delta HHI、搜尋與研發等公式與模型條件。'),
      ('appendix-b','產業經濟學解題路線','市場界定、獨占、寡占、進入、合謀、垂直關係、併購、平台、實證與競爭政策的判斷流程。'),
      ('appendix-c','中英名詞對照','Industrial Organization 常見英文術語與繁體中文對照。'),
    ]
    for cid,title,text in appendix:
        entries.extend([
          {'chapterId':cid,'chapterTitle':title,'page':0,'title':title,'text':text},
          {'chapterId':cid,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
          {'chapterId':cid,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先固定相關市場、競爭變數與時序，再選模型，最後檢查進入、差異化、效率與反事實條件。'},
        ])
    entries.append({'chapterId':'appendix-b','chapterTitle':'產業經濟學解題路線','page':3,'title':'全書快速定位','text':'市場力量先界定市場；獨占先 MR=MC；Cournot 看數量、Bertrand 看價格、Stackelberg 看時序；合謀看未來懲罰；平台看兩側；政策與實證都要有反事實。'})
    assert len(entries)==150
    return entries


def append_sw_assets(sw,old_id,paths):
    if paths[0] in sw: return sw
    needle=f'./books/{old_id}/manifest.json'; idx=sw.find(needle)
    if idx<0: raise AssertionError(f'cannot locate existing book cache entry for {old_id}')
    starts=list(re.finditer(r'const\s+[A-Za-z0-9_$]+\s*=\s*\[',sw[:idx]))
    if not starts: raise AssertionError('cannot locate service-worker asset array')
    array_end=sw.find('];',idx)
    if array_end<0: raise AssertionError('cannot locate service-worker asset array end')
    body=sw[starts[-1].end():array_end]
    insertion=''.join(f'\n  {json.dumps(p,ensure_ascii=False)},' for p in paths)
    if body.rstrip().endswith(','): insertion=insertion.lstrip('\n')
    return sw[:array_end]+insertion+'\n'+sw[array_end:]


def main(site_root):
    site=Path(site_root); lib_path=site/'data/library.json'
    if not lib_path.is_file(): raise SystemExit(f'library not found: {lib_path}')
    library=json.loads(lib_path.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in library['books']]
    if BOOK in pre_ids: raise AssertionError(f'{BOOK} already exists')
    if len(pre_ids)!=12 or pre_ids[-1]!='money-banking': raise AssertionError(f'industrial economics generator expects current twelve-book money-banking tail: {pre_ids}')

    template_entry=copy.deepcopy(library['books'][-1]); old_id=template_entry['id']; template_entry=deep_replace(template_entry,old_id,BOOK)
    template_entry.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'cover':COVER,'accent':ACCENT,'status':'available'})
    if 'version' in template_entry: template_entry['version']=VERSION
    for key in ('description','summary'):
        if key in template_entry: template_entry[key]='一般大學產業經濟學／產業組織：市場力量、定價、寡占、進入、產品差異、垂直關係、創新、平台與競爭政策。'
    library['books'].append(template_entry); lib_path.write_text(jdump(library),encoding='utf-8')

    old_root=site/'books'/old_id
    old_manifest=json.loads((old_root/'manifest.json').read_text(encoding='utf-8'))
    old_questions=json.loads((old_root/'questions.json').read_text(encoding='utf-8'))
    root=site/'books'/BOOK; chdir=root/'chapters'; figdir=site/'assets/industrial-economics-svg'
    chdir.mkdir(parents=True,exist_ok=False); figdir.mkdir(parents=True,exist_ok=False)

    chapter_meta=[]; chapter_titles={}
    for ch in CHAPTERS:
        number=str(int(ch['id'][2:])); rel=f'chapters/{ch["id"]}.html'
        (root/rel).write_text(chapter_html(ch),encoding='utf-8')
        (figdir/f'{ch["slug"]}.svg').write_text(render_svg(ch),encoding='utf-8')
        chapter_meta.append({'id':ch['id'],'number':number,'title':ch['title'],'file':rel,'kind':'chapter'})
        chapter_titles[ch['id']]=f'第 {number} 章 {ch["title"]}'

    appendices=[
      ('appendix-a','A','核心公式與模型速查','chapters/appendix-a.html',appendix_a(CHAPTERS)),
      ('appendix-b','B','產業經濟學解題路線','chapters/appendix-b.html',appendix_b()),
      ('appendix-c','C','中英名詞對照','chapters/appendix-c.html',appendix_c()),
    ]
    for cid,number,title,rel,body in appendices:
        (root/rel).write_text(body,encoding='utf-8'); chapter_meta.append({'id':cid,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest=deep_replace(copy.deepcopy(old_manifest),old_id,BOOK)
    manifest.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'version':VERSION,'cover':COVER,'accent':ACCENT,'updatedAt':UPDATED_AT,'chapters':chapter_meta,'features':{'reader':True,'quiz':True,'formula':True}})
    manifest['releaseNotes']=[{'version':VERSION,'date':UPDATED_AT,'title':'新增一般大學產業經濟學教材','changes':['新增 20 章正文與 3 份附錄','新增 100 題題庫、150 筆搜尋索引與 20 張自製 SVG','市場界定、HHI、獨占、Cournot／Bertrand／Stackelberg、合謀、垂直關係、併購、平台與競爭政策均明示模型條件'],'progressImpact':'新增獨立書籍，不改動既有書籍章節 ID、題目 ID 或閱讀進度。'}]
    for key in ('description','summary'):
        if key in manifest: manifest[key]='從必要微觀直覺銜接一般大學產業經濟學，涵蓋市場力量、策略競爭、進入、差異化、垂直關係、創新、平台與競爭政策。'
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
    cache += [f'./assets/industrial-economics-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    sw_path=site/'sw.js'; sw_path.write_text(append_sw_assets(sw_path.read_text(encoding='utf-8'),old_id,cache),encoding='utf-8')
    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':len(qitems),'search':len(entries),'figures':len(CHAPTERS),'pre_books':len(pre_ids),'post_books':len(library['books'])},ensure_ascii=False))


if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/generate_industrial_economics.py SITE_ROOT')
    main(sys.argv[1])
