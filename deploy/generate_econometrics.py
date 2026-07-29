#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from econometrics_content_a import CHAPTERS_A
from econometrics_content_b import CHAPTERS_B
from econometrics_questions_a import QUESTIONS_A
from econometrics_questions_b import QUESTIONS_B

BOOK='econometrics'
TITLE='計量經濟學'
SUBTITLE='迴歸・因果推論・時間序列・縱橫資料'
VERSION='2026.07.29-1'
UPDATED_AT='2026-07-29'
COVER='計'
ACCENT='#2563eb'
CHAPTERS=CHAPTERS_A+CHAPTERS_B
QUESTIONS=QUESTIONS_A+QUESTIONS_B
DIFFICULTY_BY_SLOT={'q01':'基礎','q02':'標準','q03':'標準','q04':'綜合','q05':'陷阱'}


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
        f'<div class="formula-card"><p class="math display">\\[{formula}\\]</p><p>{html.escape(note)}</p></div>'
        for formula,note in ch['formulas']
    )
    intuition=''.join(f'<p>{html.escape(p)}</p>' for p in ch['intuition'])
    example=''.join(f'<p>{html.escape(p)}</p>' for p in ch['example'])
    checks=''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
<figure class="chapter-figure"><img loading="lazy" src="assets/econometrics-svg/{ch['slug']}.svg" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
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


def svg_wrap(title,desc,body,footer):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 400" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(desc)}</desc>
<rect width="840" height="400" rx="26" fill="#ffffff"/>
<text x="420" y="54" text-anchor="middle" font-size="29" font-weight="700" font-family="sans-serif" fill="#1e3a8a">{xml_escape(title)}</text>
{body}
<text x="420" y="365" text-anchor="middle" font-size="16" font-family="sans-serif" fill="#475569">{xml_escape(footer)}</text>
</svg>\n'''


def flow_svg(ch):
    title,labels=ch['figure']; xs=[42,238,434,630]; boxes=[]; arrows=[]
    for i,(x,label) in enumerate(zip(xs,labels)):
        boxes.append(f'<rect x="{x}" y="145" width="166" height="92" rx="18" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/><text x="{x+83}" y="198" text-anchor="middle" font-size="18" font-family="sans-serif" fill="#1e3a8a">{xml_escape(label)}</text>')
        if i<3:
            arrows.append(f'<line x1="{x+166}" y1="191" x2="{xs[i+1]-15}" y2="191" stroke="#64748b" stroke-width="4"/><polygon points="{xs[i+1]-15},191 {xs[i+1]-29},182 {xs[i+1]-29},200" fill="#64748b"/>')
    return svg_wrap(title,' → '.join(labels),''.join(arrows)+''.join(boxes),'先辨認 estimand 與識別條件，再選估計量與推論。')


def ols_svg(ch):
    body='''<line x1="95" y1="310" x2="770" y2="310" stroke="#64748b" stroke-width="2"/><line x1="95" y1="310" x2="95" y2="90" stroke="#64748b" stroke-width="2"/>
<line x1="135" y1="280" x2="735" y2="112" stroke="#2563eb" stroke-width="4"/>
<g fill="#0f172a"><circle cx="180" cy="265" r="7"/><circle cx="300" cy="245" r="7"/><circle cx="415" cy="182" r="7"/><circle cx="545" cy="195" r="7"/><circle cx="680" cy="120" r="7"/></g>
<g stroke="#ef4444" stroke-width="3" stroke-dasharray="6 5"><line x1="180" y1="265" x2="180" y2="267"/><line x1="300" y1="245" x2="300" y2="234"/><line x1="415" y1="182" x2="415" y2="188"/><line x1="545" y1="195" x2="545" y2="151"/><line x1="680" y1="120" x2="680" y2="127"/></g>
<text x="710" y="95" font-size="17" font-family="sans-serif" fill="#2563eb">OLS 線</text><text x="535" y="215" font-size="16" font-family="sans-serif" fill="#ef4444">垂直殘差</text><text x="780" y="330" font-size="17" font-family="sans-serif">X</text><text x="70" y="90" font-size="17" font-family="sans-serif">Y</text>'''
    return svg_wrap(ch['figure'][0],'資料點、OLS 迴歸線與垂直殘差示意',body,'OLS 選擇使垂直殘差平方和最小的直線。')


def hetero_svg(ch):
    pts=[]
    coords=[(145,205),(175,198),(205,215),(275,180),(310,230),(345,165),(430,130),(455,250),(500,180),(570,105),(600,275),(650,145),(700,290)]
    for x,y in coords: pts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#0f172a"/>')
    body='''<line x1="95" y1="310" x2="770" y2="310" stroke="#64748b" stroke-width="2"/><line x1="95" y1="310" x2="95" y2="90" stroke="#64748b" stroke-width="2"/>
<line x1="120" y1="212" x2="735" y2="190" stroke="#2563eb" stroke-width="4"/>'''+''.join(pts)+'''<path d="M120 190 L735 90" stroke="#f59e0b" stroke-width="2" stroke-dasharray="7 6" fill="none"/><path d="M120 232 L735 305" stroke="#f59e0b" stroke-width="2" stroke-dasharray="7 6" fill="none"/><text x="520" y="85" font-size="16" font-family="sans-serif" fill="#b45309">條件散布擴大</text>'''
    return svg_wrap(ch['figure'][0],'X 增加時誤差條件變異擴大的異質變異示意',body,'點估計可不變，但傳統同方差標準誤可能失真。')


def time_svg(ch):
    points='120,245 180,225 240,250 300,205 360,190 420,170 480,185 540,140 600,125 660,105 720,120'
    body=f'''<line x1="95" y1="310" x2="770" y2="310" stroke="#64748b" stroke-width="2"/><line x1="95" y1="310" x2="95" y2="85" stroke="#64748b" stroke-width="2"/><polyline points="{points}" fill="none" stroke="#2563eb" stroke-width="4"/><line x1="120" y1="250" x2="720" y2="105" stroke="#f59e0b" stroke-width="3" stroke-dasharray="8 6"/><text x="630" y="82" font-size="16" font-family="sans-serif" fill="#b45309">趨勢</text><text x="735" y="330" font-size="16" font-family="sans-serif">t</text>'''
    return svg_wrap(ch['figure'][0],'帶趨勢與短期波動的時間序列示意',body,'先看趨勢、季節與持續性，再決定差分、動態模型與推論。')


def did_svg(ch):
    body='''<line x1="110" y1="310" x2="750" y2="310" stroke="#64748b" stroke-width="2"/><line x1="110" y1="310" x2="110" y2="80" stroke="#64748b" stroke-width="2"/><line x1="400" y1="85" x2="400" y2="310" stroke="#94a3b8" stroke-width="2" stroke-dasharray="7 6"/>
<line x1="170" y1="230" x2="355" y2="205" stroke="#64748b" stroke-width="4"/><line x1="445" y1="190" x2="675" y2="160" stroke="#64748b" stroke-width="4"/>
<line x1="170" y1="200" x2="355" y2="175" stroke="#2563eb" stroke-width="4"/><line x1="445" y1="145" x2="675" y2="82" stroke="#2563eb" stroke-width="4"/>
<line x1="355" y1="175" x2="675" y2="132" stroke="#2563eb" stroke-width="3" stroke-dasharray="8 6"/>
<text x="665" y="72" font-size="16" font-family="sans-serif" fill="#2563eb">Treatment observed</text><text x="665" y="154" font-size="16" font-family="sans-serif" fill="#475569">Control</text><text x="595" y="124" font-size="15" font-family="sans-serif" fill="#2563eb">反事實趨勢</text><text x="384" y="330" font-size="16" font-family="sans-serif">Policy</text>'''
    return svg_wrap(ch['figure'][0],'處置組、控制組、政策時間與平行趨勢反事實示意',body,'DiD 比較兩組的「變化差」，核心識別是假設未處置趨勢可比較。')


def rdd_svg(ch):
    left=[(140,250),(190,235),(240,225),(290,210),(340,202),(380,195)]; right=[(460,135),(500,130),(550,122),(610,110),(675,100),(720,95)]
    dots=''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#0f172a"/>' for x,y in left+right)
    body='''<line x1="95" y1="310" x2="770" y2="310" stroke="#64748b" stroke-width="2"/><line x1="95" y1="310" x2="95" y2="75" stroke="#64748b" stroke-width="2"/><line x1="420" y1="80" x2="420" y2="310" stroke="#ef4444" stroke-width="3" stroke-dasharray="7 6"/><line x1="130" y1="255" x2="405" y2="190" stroke="#2563eb" stroke-width="4"/><line x1="435" y1="142" x2="735" y2="90" stroke="#2563eb" stroke-width="4"/>'''+dots+'''<line x1="410" y1="190" x2="430" y2="142" stroke="#f59e0b" stroke-width="5"/><text x="438" y="177" font-size="16" font-family="sans-serif" fill="#b45309">局部跳躍</text><text x="400" y="330" font-size="16" font-family="sans-serif" fill="#ef4444">cutoff</text>'''
    return svg_wrap(ch['figure'][0],'Running variable 在 cutoff 兩側的局部迴歸與結果跳躍',body,'RDD 的因果資訊集中在 cutoff 附近，不可無條件外推全樣本。')


def render_svg(ch):
    if ch['id']=='ch02': return ols_svg(ch)
    if ch['id']=='ch08': return hetero_svg(ch)
    if ch['id']=='ch11': return time_svg(ch)
    if ch['id']=='ch16': return did_svg(ch)
    if ch['id']=='ch17': return rdd_svg(ch)
    return flow_svg(ch)


def appendix_a(chapters):
    rows=[]
    for ch in chapters:
        for formula,note in ch['formulas']:
            rows.append(f'<tr><td>{html.escape(ch["title"])}</td><td class="math">\\({formula}\\)</td><td>{html.escape(note)}</td></tr>')
    return '''<h1>附錄 A　核心公式與假設速查</h1>
<p class="lead">計量最危險的背法是只背公式、不背成立條件。這份附錄把公式與「它究竟需要什麼」放在同一列。</p>
<h2 id="四層判斷">四層判斷</h2>
<ol><li><strong>Estimand：</strong>想知道的是描述、預測還是因果？</li><li><strong>Identification：</strong>外生性、parallel trends、IV exclusion、RDD continuity 等假設從哪裡來？</li><li><strong>Estimator：</strong>OLS、FE、2SLS、DiD 或 RDD 是否對應該設計？</li><li><strong>Inference：</strong>同方差、robust、HAC 或 cluster SE 是否符合資料依賴結構？</li></ol>
<h2 id="高頻區分">高頻區分</h2>
<ul><li>R² 是配適，不是因果證明。</li><li>Robust SE 修標準誤，不修內生性。</li><li>FE 消時間不變個體效果，不消所有 time-varying confounders。</li><li>IV first stage 證 relevance 的一部分，不證 exclusion。</li><li>DiD pre-trends 圖可診斷，不能證明反事實假設。</li><li>RDD 通常識別 cutoff 附近 local effect。</li></ul>
<h2 id="公式表">公式表</h2>
<table><thead><tr><th>章節</th><th>公式／關係</th><th>成立條件與用途</th></tr></thead><tbody>'''+''.join(rows)+'</tbody></table>\n'


def appendix_b():
    return '''<h1>附錄 B　計量經濟學解題路線</h1>
<p class="lead">遇到陌生題先辨認「哪一種資料、哪一種識別問題」，再選公式。反過來從公式猜題型最容易失分。</p>
<h2 id="OLS與推論">OLS 與推論</h2>
<ol><li>寫母體模型與目標 beta。</li><li>辨認 simple／multiple regression，確認係數單位。</li><li>若問因果，檢查 E(u|X)=0 或相應外生性。</li><li>點估計後再選 conventional／robust／cluster／HAC SE。</li><li>最後報係數、SE／CI 與經濟意義。</li></ol>
<h2 id="內生性與IV">內生性與 IV</h2>
<ol><li>先找 OVB、反向因果、同時性或測量誤差來源。</li><li>有 instrument 時分 relevance 與 exclusion／exogeneity。</li><li>二元 IV 可先算 reduced form／first stage 的 Wald ratio。</li><li>檢查 weak instrument；強 first stage 仍不等於 instrument 外生。</li></ol>
<h2 id="Panel與時間序列">Panel 與時間序列</h2>
<ol><li>Panel 先找時間不變 alpha_i；FD／FE 利用個體內變化。</li><li>RE 要額外相信 alpha_i 與 X 不相關。</li><li>時間序列先畫趨勢與檢查定態／持續性。</li><li>序列相關時分清點估計識別問題與 HAC 推論問題。</li></ol>
<h2 id="因果設計">實驗、DiD 與 RDD</h2>
<ol><li>實驗：assignment 是否隨機？有 noncompliance 先分 ITT 與 actual treatment。</li><li>DiD：先算兩組 post-pre，再相減；核心寫 parallel trends。</li><li>RDD：找 running variable、cutoff 與局部跳躍；答案寫 local effect。</li></ol>
<h2 id="最後檢查">最後檢查</h2>
<p>百分比／百分點、log 近似／精確效果、估計值／標準誤、統計顯著／實質重要、prediction／causality 都要分開。</p>
'''


def appendix_c():
    terms=[
      ('Econometrics','計量經濟學'),('Estimand','目標參數'),('Estimator','估計量'),('Estimate','估計值'),('Identification','識別'),
      ('Cross Section','橫斷面'),('Time Series','時間序列'),('Panel Data','縱橫資料'),('Ordinary Least Squares','普通最小平方法'),('Residual','殘差'),
      ('Fitted Value','配適值'),('Zero Conditional Mean','零條件平均'),('Homoskedasticity','同方差'),('Heteroskedasticity','異質變異'),('Robust Standard Error','穩健標準誤'),
      ('Gauss–Markov Theorem','Gauss–Markov 定理'),('BLUE','最佳線性無偏估計量'),('Omitted-Variable Bias','遺漏變數偏誤'),('Endogeneity','內生性'),('Confounder','混淆因子'),
      ('Standard Error','標準誤'),('Confidence Interval','信賴區間'),('p-value','p 值'),('F Test','F 檢定'),('Adjusted R-squared','調整後 R²'),
      ('Dummy Variable','虛擬變數'),('Interaction Term','交互作用項'),('Elasticity','彈性'),('Multicollinearity','多重共線性'),('Variance Inflation Factor','變異數膨脹因子'),
      ('Leverage','槓桿值'),('Influence','影響度'),('Measurement Error','測量誤差'),('Linear Probability Model','線性機率模型'),('Logit','Logit 模型'),
      ('Probit','Probit 模型'),('Marginal Effect','邊際效果'),('Stationarity','定態'),('Random Walk','隨機漫步'),('Spurious Regression','虛假迴歸'),
      ('Autocorrelation / Serial Correlation','自我相關／序列相關'),('HAC Standard Error','異質變異與自我相關一致標準誤'),('Fixed Effects','固定效果'),('First Differences','一階差分'),('Random Effects','隨機效果'),
      ('Instrumental Variable','工具變數'),('First Stage','第一階段'),('Reduced Form','縮減式'),('Two-Stage Least Squares','兩階段最小平方法'),('Weak Instrument','弱工具變數'),
      ('Potential Outcomes','潛在結果'),('Average Treatment Effect','平均處置效果'),('Intention-to-Treat','意向治療效果'),('Difference-in-Differences','差異中的差異'),('Parallel Trends','平行趨勢'),
      ('Event Study','事件研究圖'),('Regression Discontinuity Design','迴歸不連續設計'),('Running Variable','運行變數／門檻變數'),('Bandwidth','帶寬'),('Overfitting','過度配適'),
      ('Root Mean Squared Error','均方根誤差'),('Mean Absolute Error','平均絕對誤差'),('Clustered Standard Errors','群聚標準誤'),('Reproducibility','可重現性'),('Robustness Check','穩健性檢查'),
    ]
    rows=''.join(f'<tr><td>{html.escape(en)}</td><td>{html.escape(zh)}</td></tr>' for en,zh in terms)
    return f'''<h1>附錄 C　中英名詞與輸出表對照</h1>
<p class="lead">計量題常直接使用英文軟體輸出。先辨認欄位功能，再做推論，不要只找星號。</p>
<h2 id="輸出表">迴歸輸出表怎麼看</h2>
<table><thead><tr><th>常見欄位</th><th>意思</th></tr></thead><tbody><tr><td>Coef. / Estimate</td><td>係數估計值，先看單位與函數形式。</td></tr><tr><td>Std. Error</td><td>係數的估計標準誤；確認 conventional、robust、cluster 或 HAC。</td></tr><tr><td>t / z</td><td>估計值相對虛無值的標準化距離。</td></tr><tr><td>P&gt;|t| / P&gt;|z|</td><td>相應虛無假設下的 p-value。</td></tr><tr><td>[95% Conf. Interval]</td><td>指定方法下的 95% 信賴區間。</td></tr><tr><td>N / Observations</td><td>實際進入該規格的觀察值數。</td></tr><tr><td>R-squared</td><td>樣本內配適，不等於因果有效性。</td></tr></tbody></table>
<h2 id="名詞表">中英名詞表</h2><table><thead><tr><th>English</th><th>繁體中文</th></tr></thead><tbody>{rows}</tbody></table>
'''


def search_entries(chapters,appendix_meta):
    entries=[]
    sections=[
      ('本章要解決的問題',lambda c:c['problem']),
      ('白話直覺',lambda c:' '.join(c['intuition'])),
      ('正式定義與核心概念',lambda c:' '.join(f'{a}：{b}' for a,b in c['definitions'])),
      ('核心公式與成立條件',lambda c:' '.join(f'{a}；{b}' for a,b in c['formulas'])),
      ('完整標準例題',lambda c:' '.join(c['example'])),
      ('常見錯誤',lambda c:' '.join(c['traps'])),
      ('考試判斷方法',lambda c:' '.join(c['exam'])),
      ('理解檢查',lambda c:' '.join(c['checks'])),
    ]
    for ch in chapters:
        entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':0,'title':ch['title'],'text':ch['problem']+' '+' '.join(ch['intuition'])})
        for page,(title,getter) in enumerate(sections,start=1):
            entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':title,'text':getter(ch)})
    for ch_id,title,text in appendix_meta:
        entries.extend([
          {'chapterId':ch_id,'chapterTitle':title,'page':0,'title':title,'text':text},
          {'chapterId':ch_id,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
          {'chapterId':ch_id,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先辨認 estimand 與識別條件，再選估計量與標準誤，最後檢查單位、因果範圍與外推限制。'},
        ])
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
    if not pre_ids: raise AssertionError('library has no template book')
    if len(CHAPTERS)!=20 or [c['id'] for c in CHAPTERS]!=[f'ch{i:02d}' for i in range(20)]: raise AssertionError('chapter source integrity')
    if len(QUESTIONS)!=100: raise AssertionError('question source integrity')

    template=copy.deepcopy(library['books'][-1]); old_id=template['id']; template=deep_replace(template,old_id,BOOK)
    template['id']=BOOK; template['title']=TITLE; template['subtitle']=SUBTITLE; template['cover']=COVER; template['accent']=ACCENT; template['status']='available'
    for key in ('description','summary'):
        if key in template: template[key]='一般大學計量經濟學：OLS、多元迴歸、推論、內生性、IV、時間序列、panel 與現代因果推論。'
    library['books'].append(template); lib_path.write_text(jdump(library),encoding='utf-8')

    old_root=site/'books'/old_id
    old_manifest=json.loads((old_root/'manifest.json').read_text(encoding='utf-8')); old_questions=json.loads((old_root/'questions.json').read_text(encoding='utf-8'))
    root=site/'books'/BOOK; chdir=root/'chapters'; figdir=site/'assets/econometrics-svg'; chdir.mkdir(parents=True,exist_ok=False); figdir.mkdir(parents=True,exist_ok=False)
    chapter_meta=[]; chapter_titles={}
    for ch in CHAPTERS:
        number=str(int(ch['id'][2:])); rel=f'chapters/{ch["id"]}.html'
        (root/rel).write_text(chapter_html(ch),encoding='utf-8'); (figdir/f'{ch["slug"]}.svg').write_text(render_svg(ch),encoding='utf-8')
        chapter_meta.append({'id':ch['id'],'number':number,'title':ch['title'],'file':rel,'kind':'chapter'}); chapter_titles[ch['id']]=f'第 {number} 章 {ch["title"]}'

    appendices=[
      ('appendix-a','A','核心公式與假設速查','chapters/appendix-a.html',appendix_a(CHAPTERS)),
      ('appendix-b','B','計量經濟學解題路線','chapters/appendix-b.html',appendix_b()),
      ('appendix-c','C','中英名詞與輸出表對照','chapters/appendix-c.html',appendix_c()),
    ]
    for ch_id,number,title,rel,body in appendices:
        (root/rel).write_text(body,encoding='utf-8'); chapter_meta.append({'id':ch_id,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest=deep_replace(copy.deepcopy(old_manifest),old_id,BOOK); manifest['id']=BOOK; manifest['title']=TITLE; manifest['subtitle']=SUBTITLE; manifest['version']=VERSION; manifest['cover']=COVER; manifest['accent']=ACCENT; manifest['updatedAt']=UPDATED_AT; manifest['chapters']=chapter_meta
    manifest['releaseNotes']=[{'version':VERSION,'date':UPDATED_AT,'title':'新增一般大學計量經濟學教材','changes':['新增 20 章正文與 3 份附錄，從 OLS 銜接 IV、panel、time series、DiD 與 RDD','新增 100 題本科常見題型與可重算數值題','新增 20 張自製 SVG 與 189 筆全文搜尋索引','因果與相關、點估計與標準誤、prediction 與 causal interpretation 全程分開'],'progressImpact':'新增獨立書籍，不改動既有書籍章節、題目 ID 或閱讀進度。'}]
    for key in ('description','summary'):
        if key in manifest: manifest[key]='從近零基礎銜接一般大學計量經濟學，聚焦迴歸、推論、內生性、IV、時間序列、panel 與現代因果推論。'
    (root/'manifest.json').write_text(jdump(manifest),encoding='utf-8')

    qtop=deep_replace(copy.deepcopy(old_questions),old_id,BOOK); qtop['bookId']=BOOK; qtop['version']=VERSION; qitems=[]
    for src in QUESTIONS:
        slot=src['id'].rsplit('-',1)[-1]
        qitems.append({'id':src['id'],'bookId':BOOK,'chapterId':src['chapterId'],'chapterTitle':chapter_titles[src['chapterId']],'topic':next(ch['title'] for ch in CHAPTERS if ch['id']==src['chapterId']),'difficulty':DIFFICULTY_BY_SLOT[slot],'question':src['question'],'answer':src['answer'],'explanation':src['explanation'],'source':'本書自編標準題型'})
    if len({q['id'] for q in qitems})!=100: raise AssertionError('duplicate question id')
    qtop['count']=len(qitems); qtop['items']=qitems; (root/'questions.json').write_text(jdump(qtop),encoding='utf-8')

    appendix_meta=[('appendix-a','核心公式與假設速查','OLS、推論、函數形式、時間序列、panel、IV、DiD 與 RDD 的公式和成立條件。'),('appendix-b','計量經濟學解題路線','從 estimand、identification 到 estimator、standard error 與 interpretation 的解題流程。'),('appendix-c','中英名詞與輸出表對照','計量經濟學英文術語與迴歸輸出表欄位對照。')]
    entries=search_entries(CHAPTERS,appendix_meta); (root/'search.json').write_text(jdump({'entries':entries}),encoding='utf-8')

    cache=[f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json']
    cache += [f'./books/{BOOK}/{x["file"]}' for x in chapter_meta]
    cache += [f'./assets/econometrics-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    sw_path=site/'sw.js'; sw_path.write_text(append_sw_assets(sw_path.read_text(encoding='utf-8'),old_id,cache),encoding='utf-8')
    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':len(qitems),'search':len(entries),'figures':len(CHAPTERS),'pre_books':len(pre_ids),'post_books':len(library['books'])},ensure_ascii=False))


if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/generate_econometrics.py SITE_ROOT')
    main(sys.argv[1])
