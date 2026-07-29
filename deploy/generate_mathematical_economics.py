#!/usr/bin/env python3
from __future__ import annotations

import copy, html, json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from mathematical_economics_content import CHAPTERS
from mathematical_economics_questions import build_questions

BOOK='mathematical-economics'
TITLE='數理經濟學'
SUBTITLE='函數・矩陣・微積分・比較靜態・最佳化與動態系統'
VERSION='2026.07.29-1'
UPDATED_AT='2026-07-29'
COVER='數'
ACCENT='#7c3aed'
DIFFICULTY={'q01':'基礎','q02':'標準','q03':'標準','q04':'進階','q05':'進階'}


def jdump(x): return json.dumps(x,ensure_ascii=False,indent=2)+'\n'

def deep_replace(v,old,new):
    if isinstance(v,str): return v.replace(old,new)
    if isinstance(v,list): return [deep_replace(x,old,new) for x in v]
    if isinstance(v,dict): return {k:deep_replace(x,old,new) for k,x in v.items()}
    return v

def ul(items): return '<ul>'+''.join(f'<li>{html.escape(x)}</li>' for x in items)+'</ul>'

def chapter_html(ch):
    defs=''.join(f'<dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd>' for a,b in ch['definitions'])
    formulas=''.join(f'<div class="formula-card"><p class="math display">\\[{html.escape(a)}\\]</p><p>{html.escape(b)}</p></div>' for a,b in ch['formulas'])
    intuition=''.join(f'<p>{html.escape(x)}</p>' for x in ch['intuition'])
    example=''.join(f'<p>{html.escape(x)}</p>' for x in ch['example'])
    checks=''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/mathematical-economics-svg/{ch['slug']}.svg" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
<h2 id="本章要解決的問題">本章要解決的問題</h2><p>{html.escape(ch['problem'])}</p>
<h2 id="白話直覺">白話直覺</h2>{intuition}
<h2 id="正式定義與核心概念">正式定義與核心概念</h2><dl class="term-list">{defs}</dl>
<h2 id="核心公式與成立條件">核心公式與成立條件</h2>{formulas}
<h2 id="完整標準例題">完整標準例題</h2><div class="worked-example">{example}</div>
<h2 id="常見錯誤">常見錯誤</h2>{ul(ch['traps'])}
<h2 id="考試判斷方法">考試判斷方法</h2>{ul(ch['exam'])}
<h2 id="理解檢查">理解檢查</h2><ol class="quick-check">{checks}</ol>
'''

def render_svg(ch):
    title,labels=ch['figure']; xs=[50,245,440,635]; boxes=[]; arrows=[]
    for i,(x,label) in enumerate(zip(xs,labels)):
        boxes.append(f'<rect x="{x}" y="150" width="150" height="92" rx="18" fill="#f5f3ff" stroke="#7c3aed" stroke-width="3"/><text x="{x+75}" y="199" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#4c1d95">{xml_escape(label)}</text>')
        if i<3: arrows.append(f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#64748b" stroke-width="4"/><polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#64748b"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 835 390" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(' → '.join(labels))}</desc><rect width="835" height="390" rx="26" fill="#ffffff"/>
<text x="417" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#4c1d95">{xml_escape(title)}</text>{''.join(arrows)}{''.join(boxes)}
<text x="417" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先辨認數學物件，再運算；最後回頭檢查條件、符號與可行域。</text></svg>\n'''

def appendix_a():
    rows=[]
    for ch in CHAPTERS:
        for formula,note in ch['formulas']:
            rows.append(f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({html.escape(formula)}\\)</td><td>{html.escape(note)}</td></tr>')
    return '<h1>附錄 A　核心公式速查</h1><p class="lead">考前用這份表確認公式、符號與成立條件；數理經濟學最危險的失分通常不是算術，而是把必要條件當充分條件或漏掉可行域。</p><table><thead><tr><th>章節</th><th>公式</th><th>條件／用途</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'

def appendix_b():
    return '''<h1>附錄 B　數理經濟學解題路線</h1>
<p class="lead">陌生題先分類，再選工具。不要一看到符號就微分，也不要一看到限制就不分等式／不等式直接套 Lagrange。</p>
<h2>方程與矩陣</h2><ol><li>數未知數與獨立方程。</li><li>線性系統先寫 Ax=b。</li><li>需要唯一解時檢查 determinant／rank／可逆性。</li><li>最後代回全部方程。</li></ol>
<h2>微分與比較靜態</h2><ol><li>固定基準點、內生變數與外生參數。</li><li>顯函數直接微分；隱式均衡先寫 F=0 再全微分。</li><li>比較靜態不是時間路徑。</li><li>小變動近似要標示近似號。</li></ol>
<h2>最佳化</h2><ol><li>先寫可行域。</li><li>無限制：FOC→SOC／凹凸性→端點。</li><li>等式限制：Lagrangian＋限制式。</li><li>不等式：KKT 四塊一起檢查；不能漏互補鬆弛。</li></ol>
<h2>動態</h2><ol><li>差分方程令 x_{t+1}=x_t 求穩態。</li><li>微分方程令 ẋ=0 求穩態。</li><li>再看特徵根絕對值或 F′(x*) 的符號。</li><li>穩態、穩定與最適是三個不同概念。</li></ol>'''

def appendix_c():
    terms=[('Variable','變數'),('Parameter','參數'),('Function','函數'),('Equilibrium','均衡'),('Vector','向量'),('Matrix','矩陣'),('Determinant','行列式'),('Inverse Matrix','反矩陣'),('Eigenvalue','特徵值'),('Quadratic Form','二次型'),('Limit','極限'),('Derivative','導數'),('Taylor Approximation','Taylor 近似'),('Partial Derivative','偏導數'),('Total Differential','全微分'),('Gradient','梯度'),('Jacobian','Jacobian 矩陣'),('Hessian','Hessian 矩陣'),('Comparative Statics','比較靜態'),('Implicit Function Theorem','隱函數定理'),('Elasticity','彈性'),('Log Differentiation','對數微分'),('First-Order Condition','一階條件'),('Second-Order Condition','二階條件'),('Lagrangian','Lagrangian'),('Lagrange Multiplier','Lagrange 乘數'),('KKT Conditions','KKT 條件'),('Complementary Slackness','互補鬆弛'),('Envelope Theorem','包絡定理'),('Value Function','值函數'),('Homogeneous Function','齊次函數'),('Euler Theorem','Euler 定理'),('Integral','積分'),('Difference Equation','差分方程'),('Differential Equation','微分方程'),('Steady State','穩態'),('Stability','穩定性')]
    rows=''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>' for a,b in terms)
    return f'<h1>附錄 C　中英名詞與符號對照</h1><p class="lead">英文題幹常把相近數學詞混在一起考。先確認 term 的精確意思，再決定公式。</p><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>'

def search_entries():
    entries=[]; fields=[('正式定義與核心概念',lambda c:' '.join(f'{a}：{b}' for a,b in c['definitions'])),('核心公式與成立條件',lambda c:' '.join(f'{a}；{b}' for a,b in c['formulas'])),('完整標準例題',lambda c:' '.join(c['example'])),('常見錯誤',lambda c:' '.join(c['traps'])),('考試判斷方法',lambda c:' '.join(c['exam'])),('理解檢查',lambda c:' '.join(c['checks']))]
    for ch in CHAPTERS:
        entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':0,'title':ch['title'],'text':ch['problem']+' '+' '.join(ch['intuition'])})
        for page,(title,getter) in enumerate(fields,start=1): entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':title,'text':getter(ch)})
    apps=[('appendix-a','核心公式速查','線性代數、微積分、最佳化、比較靜態與動態公式條件速查。'),('appendix-b','數理經濟學解題路線','方程矩陣、微分比較靜態、最佳化與動態系統的判斷流程。'),('appendix-c','中英名詞與符號對照','Mathematical Economics 常見英文術語與繁體中文對照。')]
    for cid,title,text in apps:
        for page,label in enumerate([title,'快速定位','考試使用方式']): entries.append({'chapterId':cid,'chapterTitle':title,'page':page,'title':label,'text':text})
    entries.append({'chapterId':'appendix-b','chapterTitle':'數理經濟學解題路線','page':3,'title':'全書快速定位','text':'先辨認數學物件與可行域：聯立看矩陣，局部變動看微分，比較靜態看隱函數，最佳化分無限制／等式／不等式，動態再看穩定性。'})
    assert len(entries)==150
    return entries

def append_sw_assets(sw,old_id,paths):
    if paths[0] in sw: return sw
    needle=f'./books/{old_id}/manifest.json'; idx=sw.find(needle)
    if idx<0: raise AssertionError(f'cannot locate existing cache anchor {old_id}')
    starts=list(re.finditer(r'const\s+[A-Za-z0-9_$]+\s*=\s*\[',sw[:idx]));
    if not starts: raise AssertionError('cannot locate service worker asset array')
    end=sw.find('];',idx)
    if end<0: raise AssertionError('cannot locate service worker asset array end')
    insertion=''.join(f'\n  {json.dumps(p,ensure_ascii=False)},' for p in paths)
    return sw[:end]+insertion+'\n'+sw[end:]

def main(site_root):
    site=Path(site_root); lp=site/'data/library.json'; library=json.loads(lp.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in library['books']]
    if BOOK in pre_ids: raise AssertionError(f'{BOOK} already exists')
    if len(pre_ids)!=12 or pre_ids[-1]!='money-banking': raise AssertionError(f'mathematical economics expects twelve-book money-banking tail: {pre_ids}')
    template=copy.deepcopy(library['books'][-1]); old_id=template['id']; template=deep_replace(template,old_id,BOOK)
    template.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'cover':COVER,'accent':ACCENT,'status':'available'})
    if 'version' in template: template['version']=VERSION
    for key in ('description','summary'):
        if key in template: template[key]='一般大學數理經濟學：函數、矩陣、微積分、比較靜態、最佳化、積分與動態系統。'
    library['books'].append(template); lp.write_text(jdump(library),encoding='utf-8')
    old_root=site/'books'/old_id; old_manifest=json.loads((old_root/'manifest.json').read_text(encoding='utf-8')); old_questions=json.loads((old_root/'questions.json').read_text(encoding='utf-8'))
    root=site/'books'/BOOK; chdir=root/'chapters'; figdir=site/'assets/mathematical-economics-svg'; chdir.mkdir(parents=True,exist_ok=False); figdir.mkdir(parents=True,exist_ok=False)
    meta=[]; titles={}
    for ch in CHAPTERS:
        number=str(int(ch['id'][2:])); rel=f'chapters/{ch["id"]}.html'; (root/rel).write_text(chapter_html(ch),encoding='utf-8'); (figdir/f'{ch["slug"]}.svg').write_text(render_svg(ch),encoding='utf-8'); meta.append({'id':ch['id'],'number':number,'title':ch['title'],'file':rel,'kind':'chapter'}); titles[ch['id']]=f'第 {number} 章 {ch["title"]}'
    apps=[('appendix-a','A','核心公式速查','chapters/appendix-a.html',appendix_a()),('appendix-b','B','數理經濟學解題路線','chapters/appendix-b.html',appendix_b()),('appendix-c','C','中英名詞與符號對照','chapters/appendix-c.html',appendix_c())]
    for cid,num,title,rel,body in apps: (root/rel).write_text(body,encoding='utf-8'); meta.append({'id':cid,'number':num,'title':title,'file':rel,'kind':'appendix'})
    manifest=deep_replace(copy.deepcopy(old_manifest),old_id,BOOK); manifest.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'version':VERSION,'cover':COVER,'accent':ACCENT,'updatedAt':UPDATED_AT,'chapters':meta,'features':{'reader':True,'quiz':True,'formula':True}})
    manifest['releaseNotes']=[{'version':VERSION,'date':UPDATED_AT,'title':'新增一般大學數理經濟學教材','changes':['新增 20 章正文與 3 份附錄','新增 100 題題庫、150 筆搜尋索引與 20 張自製 SVG','核心涵蓋矩陣、微積分、比較靜態、Hessian、Lagrange、KKT、積分與一階動態'],'progressImpact':'新增獨立書籍，不改動既有書籍章節 ID、題目 ID、錯題紀錄或閱讀進度。'}]
    (root/'manifest.json').write_text(jdump(manifest),encoding='utf-8')
    raw=build_questions(); qtop=deep_replace(copy.deepcopy(old_questions),old_id,BOOK); qtop['bookId']=BOOK; qtop['version']=VERSION; qitems=[]
    for src in raw:
        slot=src['id'].rsplit('-',1)[-1]; qitems.append({'id':src['id'],'bookId':BOOK,'chapterId':src['chapterId'],'chapterTitle':titles[src['chapterId']],'topic':next(ch['title'] for ch in CHAPTERS if ch['id']==src['chapterId']),'difficulty':DIFFICULTY[slot],'question':src['question'],'answer':src['answer'],'explanation':src['explanation'],'source':'本書自編標準題型'})
    qtop['count']=len(qitems); qtop['items']=qitems; (root/'questions.json').write_text(jdump(qtop),encoding='utf-8'); entries=search_entries(); (root/'search.json').write_text(jdump({'entries':entries}),encoding='utf-8')
    cache=[f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json']+[f'./books/{BOOK}/{x["file"]}' for x in meta]+[f'./assets/mathematical-economics-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    swp=site/'sw.js'; swp.write_text(append_sw_assets(swp.read_text(encoding='utf-8'),old_id,cache),encoding='utf-8')
    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':len(qitems),'search':len(entries),'figures':20,'pre_books':12,'post_books':13},ensure_ascii=False))

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/generate_mathematical_economics.py SITE_ROOT')
    main(sys.argv[1])
