#!/usr/bin/env python3
from __future__ import annotations

import copy
import html
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from civil_law_overview_content import CHAPTERS
from civil_law_overview_questions import build_questions

BOOK='civil-law-overview'
TITLE='民法概要'
SUBTITLE='總則・債・物權・親屬・繼承'
VERSION='2026.07.29-1'
UPDATED_AT='2026-07-29'
COVER='民'
ACCENT='#1d4ed8'
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
    rules=''.join(
        f'<div class="formula-card"><p><strong>{html.escape(label)}</strong></p><p>{html.escape(rule)}</p></div>'
        for label,rule in ch['rules']
    )
    intuition=''.join(f'<p>{html.escape(p)}</p>' for p in ch['intuition'])
    example=''.join(f'<p>{html.escape(p)}</p>' for p in ch['example'])
    checks=''.join(f'<li>{html.escape(x)}</li>' for x in ch['checks'])
    baseline='''<div class="warningbox"><strong>法規基準：</strong>本書依 2026-07-29 可查得之中華民國現行民法與相關施行法整理。涉及成年年齡、期間、方式與身分規則時，考題若指定不同時點，應以該時點法規為準。</div>''' if ch['id']=='ch00' else ''
    special='''<div class="warningbox"><strong>現行法提醒：</strong>民法第 166-1 條雖已增訂，但施行日期仍待另定；本書不把「不動產負擔契約須公證」當成現行已施行的一般規則。</div>''' if ch['id']=='ch13' else ''
    return f'''<p class="chapter-kicker">第 {int(ch['id'][2:])} 章</p>
<h1>{html.escape(ch['title'])}</h1>
<p class="lead">{html.escape(ch['problem'])}</p>
{baseline}{special}
<figure class="chapter-figure"><img loading="lazy" src="assets/civil-law-overview-svg/{ch['slug']}.svg" alt="{html.escape(ch['figure'][0])}"><figcaption>{html.escape(ch['figure'][0])}</figcaption></figure>
<h2 id="本章要解決的問題">本章要解決的問題</h2>
<p>{html.escape(ch['problem'])}</p>
<h2 id="白話直覺">白話直覺</h2>
{intuition}
<h2 id="正式定義與核心概念">正式定義與核心概念</h2>
<dl class="term-list">{defs}</dl>
<h2 id="核心法條與成立條件">核心法條與成立條件</h2>
{rules}
<h2 id="完整標準案例">完整標準案例</h2>
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
    fills=['#eff6ff','#dbeafe','#bfdbfe','#dbeafe']
    for i,(x,label) in enumerate(zip(xs,labels)):
        boxes.append(f'<rect x="{x}" y="150" width="150" height="92" rx="18" fill="{fills[i]}" stroke="#1d4ed8" stroke-width="3"/><text x="{x+75}" y="194" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#1e3a8a">{xml_escape(label)}</text>')
        if i<3:
            arrows.append(f'<line x1="{x+150}" y1="196" x2="{xs[i+1]-18}" y2="196" stroke="#64748b" stroke-width="4"/><polygon points="{xs[i+1]-18},196 {xs[i+1]-32},187 {xs[i+1]-32},205" fill="#64748b"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 835 390" role="img" aria-labelledby="title desc">
<title id="title">{xml_escape(title)}</title><desc id="desc">{xml_escape(' → '.join(labels))}</desc>
<rect width="835" height="390" rx="26" fill="#ffffff"/>
<text x="417" y="72" text-anchor="middle" font-size="30" font-weight="700" font-family="sans-serif" fill="#1e3a8a">{xml_escape(title)}</text>
{''.join(arrows)}{''.join(boxes)}
<text x="417" y="318" text-anchor="middle" font-size="17" font-family="sans-serif" fill="#475569">先找請求權基礎，再逐一檢查要件、抗辯與法律效果。</text>
</svg>\n'''


def appendix_a():
    rows=[
      ('成年／未成年人','民法 12、13','18 歲成年；未滿 7 歲無行為能力；7 歲以上未成年人為限制行為能力。'),
      ('錯誤撤銷','民法 90','第 88、89 條撤銷權自意思表示後 1 年消滅。'),
      ('詐欺／脅迫撤銷','民法 93','發現詐欺或脅迫終止後 1 年；意思表示後逾 10 年不得撤銷。'),
      ('一般請求權時效','民法 125','原則 15 年；有較短特別期間者從其規定。'),
      ('定期給付','民法 126','利息、租金等各期請求權原則 5 年。'),
      ('侵權時效','民法 197','知悉損害及賠償義務人起 2 年；行為時起 10 年。'),
      ('約定利率上限','民法 205','週年利率超過 16% 的超過部分約定無效。'),
      ('物之瑕疵權利期間','民法 365','通知後 6 個月或交付後 5 年；故意不告知瑕疵對 6 個月規則另有例外。'),
      ('不動產物權法律行為','民法 758','書面＋登記；非經登記不生物權效力。'),
      ('共有物一般管理','民法 820','人數過半＋應有部分過半；應有部分逾 2/3 時人數不計。'),
      ('結婚年齡／方式','民法 980、982','18 歲；書面＋二人以上證人簽名＋戶政登記。'),
      ('兩願離婚','民法 1050','書面＋二人以上證人簽名＋戶政登記。'),
      ('婚生否認','民法 1063','夫妻之一方或子女自知悉起 2 年；子女未成年時知悉者仍得成年後 2 年內提起。'),
      ('拋棄繼承','民法 1174','知悉得繼承起 3 個月內，以書面向法院為之。'),
      ('遺囑能力','民法 1186','限制行為能力人無須法定代理人允許；未滿 16 歲不得為遺囑。'),
    ]
    body=''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>' for a,b,c in rows)
    return f'''<h1>附錄 A　高頻條文、年齡與期間速查</h1>
<p class="lead">這張表只用來考前定位；真正作答案仍要回到完整條文與題目法規時點。尤其期間題要分起算點、完成日、中斷或除斥期間，不能只背單一數字。</p>
<div class="warningbox"><strong>未施行提醒：</strong>民法第 166-1 條施行日期仍待另定；不要把它當現行已生效的一般規則。</div>
<table><thead><tr><th>主題</th><th>核心條文</th><th>速查內容</th></tr></thead><tbody>{body}</tbody></table>
'''


def appendix_b():
    return '''<h1>附錄 B　民法案例題請求權基礎解題法</h1>
<p class="lead">案例題不要從故事第一句開始逐句翻譯成法律。先寫「誰對誰，想要什麼」，再建立請求權清單。</p>
<h2 id="第一步">第一步：確定目標與當事人</h2>
<ol><li>寫 A 對 B，避免人物多時混線。</li><li>寫 A 要求的是交付、返還、賠償、停止妨害、解除、撤銷，還是身分／繼承效果。</li><li>先分契約關係、物權關係、法定之債、親屬或繼承。</li></ol>
<h2 id="第二步">第二步：列請求權基礎</h2>
<ol><li>有契約先看契約履行與債務不履行。</li><li>有物被占有，確認所有權與占有權源，再看第 767 條等物上請求。</li><li>無契約但有人得利，掃不當得利；有不法損害，掃侵權。</li><li>身分與死亡案件改走親屬、繼承的特別規則。</li></ol>
<h2 id="第三步">第三步：逐一檢查四格</h2>
<table><thead><tr><th>四格</th><th>要問的問題</th></tr></thead><tbody><tr><td>發生</td><td>構成要件是否全部具備？</td></tr><tr><td>變動</td><td>是否撤銷、解除、讓與、抵銷或其他變動？</td></tr><tr><td>受阻</td><td>是否有時效、同時履行、與有過失、善意第三人等抗辯或限制？</td></tr><tr><td>效果</td><td>最後能請求交付、返還、賠償或其他何種效果？</td></tr></tbody></table>
<h2 id="最後檢查">最後檢查</h2>
<ul><li>有沒有把債權效力和物權變動混成一件事？</li><li>有沒有把無效、得撤銷、效力未定混用？</li><li>有沒有漏掉期間、方式、善意第三人或法規時點？</li><li>數字題是否先算順位、份額或期間，再寫法律結論？</li></ul>
'''


def appendix_c():
    pairs=[
      ('無效','自始不生當事人所欲法律效果；仍要注意轉換、善意第三人等個別規定。'),
      ('得撤銷','撤銷前有效；依法撤銷後原則視為自始無效。'),
      ('效力未定','法律行為是否生效待有權人承認等後續事實確定。'),
      ('債權','特定人對特定人的相對請求。'),
      ('物權','對特定物直接支配、具有排他與對世性的權利。'),
      ('解除','使有效契約關係依法消滅並進入回復原狀等效果。'),
      ('終止','通常使繼續性法律關係向將來消滅，不當然溯及既往。'),
      ('消滅時效','期間完成使義務人取得拒絕給付抗辯，非簡單等同債權消失。'),
      ('除斥期間','形成權等依法定期間不行使而消滅，與消滅時效制度效果不同。'),
      ('占有','對物的事實上管領，不等於所有權。'),
      ('應繼分','依法律計算的法定繼承份額。'),
      ('特留分','特定繼承人受法律保障的最低份額，以應繼分的一定比例計算。'),
    ]
    rows=''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>' for a,b in pairs)
    return f'''<h1>附錄 C　易混淆法律效果與現行法提醒</h1>
<p class="lead">民法最常見失分不是完全不知道，而是把相近名詞寫成同一效果。本表用最短文字做最後一道防混淆。</p>
<table><thead><tr><th>名詞</th><th>快速區分</th></tr></thead><tbody>{rows}</tbody></table>
<h2 id="現行法提醒">現行法提醒</h2>
<ul><li>成年年齡現為 18 歲；相關新制自 2023-01-01 施行。</li><li>民法第 166-1 條目前仍未施行。</li><li>相同性別二人婚姻須同時注意《司法院釋字第七四八號解釋施行法》，不能只讀民法婚姻章文字。</li><li>本書基準日為 2026-07-29；法規修改後應重新核對條文與施行日期。</li></ul>
'''


def search_entries(chapters):
    entries=[]
    fields=[
      ('正式定義與核心概念',lambda c:' '.join(f'{a}：{b}' for a,b in c['definitions'])),
      ('核心法條與成立條件',lambda c:' '.join(f'{a}：{b}' for a,b in c['rules'])),
      ('完整標準案例',lambda c:' '.join(c['example'])),
      ('常見錯誤',lambda c:' '.join(c['traps'])),
      ('考試判斷方法',lambda c:' '.join(c['exam'])),
      ('理解檢查',lambda c:' '.join(c['checks'])),
    ]
    for ch in chapters:
        entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':0,'title':ch['title'],'text':ch['problem']+' '+' '.join(ch['intuition'])})
        for page,(title,getter) in enumerate(fields,start=1):
            entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':title,'text':getter(ch)})
    appendix=[
      ('appendix-a','高頻條文、年齡與期間速查','18 歲成年、一般請求權 15 年、定期給付 5 年、侵權 2 年／10 年、瑕疵 6 個月／5 年、拋棄繼承 3 個月。'),
      ('appendix-b','民法案例題請求權基礎解題法','誰對誰、請求權基礎、構成要件、抗辯與法律效果的四格案例題方法。'),
      ('appendix-c','易混淆法律效果與現行法提醒','無效、得撤銷、效力未定、解除、終止、消滅時效、特留分，以及第 166-1 條未施行提醒。'),
    ]
    for cid,title,text in appendix:
        entries.extend([
          {'chapterId':cid,'chapterTitle':title,'page':0,'title':title,'text':text},
          {'chapterId':cid,'chapterTitle':title,'page':1,'title':'快速定位','text':text},
          {'chapterId':cid,'chapterTitle':title,'page':2,'title':'考試使用方式','text':'先固定法律關係與法規時點，再逐一檢查構成要件、例外、期間及法律效果。'},
        ])
    entries.append({'chapterId':'appendix-b','chapterTitle':'民法案例題請求權基礎解題法','page':3,'title':'全書快速定位','text':'總則先定共同語法；債編找人對人請求；物權分登記與交付；親屬看法定方式；繼承先順位再份額。'})
    assert len(entries)==150
    return entries


def append_sw_assets(sw,old_id,paths):
    if paths[0] in sw: return sw
    needle=f'./books/{old_id}/manifest.json'; idx=sw.find(needle)
    if idx<0: raise AssertionError(f'cannot locate existing cache entry for {old_id}')
    starts=list(re.finditer(r'const\s+[A-Za-z0-9_$]+\s*=\s*\[',sw[:idx]))
    if not starts: raise AssertionError('cannot locate service-worker asset array')
    array_start=starts[-1].end()-1; array_end=sw.find('];',idx)
    if array_end<0: raise AssertionError('cannot locate service-worker asset array end')
    insertion=''.join(f'\n  {json.dumps(p,ensure_ascii=False)},' for p in paths)
    return sw[:array_end]+insertion+'\n'+sw[array_end:]


def main(site_root):
    site=Path(site_root); lib_path=site/'data/library.json'
    if not lib_path.is_file(): raise SystemExit(f'library not found: {lib_path}')
    library=json.loads(lib_path.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in library['books']]
    if BOOK in pre_ids: raise AssertionError(f'{BOOK} already exists')
    if len(pre_ids)<12 or len(set(pre_ids))!=len(pre_ids): raise AssertionError(f'civil generator requires a valid formal library tail: {pre_ids}')

    template_entry=copy.deepcopy(library['books'][-1]); old_id=template_entry['id']; template_entry=deep_replace(template_entry,old_id,BOOK)
    template_entry.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'cover':COVER,'accent':ACCENT,'status':'available'})
    if 'version' in template_entry: template_entry['version']=VERSION
    for key in ('description','summary'):
        if key in template_entry: template_entry[key]='一般大學民法概要：總則、債、物權、親屬與繼承，以請求權基礎與常考現行法規則為主。'
    library['books'].append(template_entry); lib_path.write_text(jdump(library),encoding='utf-8')

    old_root=site/'books'/old_id
    old_manifest=json.loads((old_root/'manifest.json').read_text(encoding='utf-8'))
    old_questions=json.loads((old_root/'questions.json').read_text(encoding='utf-8'))
    root=site/'books'/BOOK; chdir=root/'chapters'; figdir=site/'assets/civil-law-overview-svg'
    chdir.mkdir(parents=True,exist_ok=False); figdir.mkdir(parents=True,exist_ok=False)

    chapter_meta=[]; chapter_titles={}
    for ch in CHAPTERS:
        number=str(int(ch['id'][2:])); rel=f'chapters/{ch["id"]}.html'
        (root/rel).write_text(chapter_html(ch),encoding='utf-8')
        (figdir/f'{ch["slug"]}.svg').write_text(render_svg(ch),encoding='utf-8')
        chapter_meta.append({'id':ch['id'],'number':number,'title':ch['title'],'file':rel,'kind':'chapter'})
        chapter_titles[ch['id']]=f'第 {number} 章 {ch["title"]}'

    appendices=[
      ('appendix-a','A','高頻條文、年齡與期間速查','chapters/appendix-a.html',appendix_a()),
      ('appendix-b','B','民法案例題請求權基礎解題法','chapters/appendix-b.html',appendix_b()),
      ('appendix-c','C','易混淆法律效果與現行法提醒','chapters/appendix-c.html',appendix_c()),
    ]
    for cid,number,title,rel,body in appendices:
        (root/rel).write_text(body,encoding='utf-8'); chapter_meta.append({'id':cid,'number':number,'title':title,'file':rel,'kind':'appendix'})

    manifest=deep_replace(copy.deepcopy(old_manifest),old_id,BOOK)
    manifest.update({'id':BOOK,'title':TITLE,'subtitle':SUBTITLE,'version':VERSION,'cover':COVER,'accent':ACCENT,'updatedAt':UPDATED_AT,'chapters':chapter_meta,'features':{'reader':True,'quiz':True,'formula':True}})
    manifest['releaseNotes']=[{'version':VERSION,'date':UPDATED_AT,'title':'新增一般大學民法概要教材','changes':['新增 20 章正文與 3 份附錄，涵蓋總則、債、物權、親屬、繼承','新增 100 題題庫、150 筆搜尋索引與 20 張自製 SVG','成年年齡、時效、物權公示、婚姻方式、繼承順位等高風險現行法逐項複核','明確標示民法第 166-1 條尚未施行，並補同性婚姻特別法提醒'],'progressImpact':'新增獨立書籍，不改動既有書籍章節 ID、題目 ID 或閱讀進度。'}]
    for key in ('description','summary'):
        if key in manifest: manifest[key]='從近零基礎銜接一般大學民法概要，依請求權基礎建立總則、債、物權、親屬與繼承的案例解題框架。'
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
    cache += [f'./assets/civil-law-overview-svg/{ch["slug"]}.svg' for ch in CHAPTERS]
    sw_path=site/'sw.js'; sw_path.write_text(append_sw_assets(sw_path.read_text(encoding='utf-8'),old_id,cache),encoding='utf-8')
    print(json.dumps({'book':BOOK,'version':VERSION,'chapters':20,'appendices':3,'questions':len(qitems),'search':len(entries),'figures':len(CHAPTERS),'pre_books':len(pre_ids),'post_books':len(library['books'])},ensure_ascii=False))

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/generate_civil_law_overview.py SITE_ROOT')
    main(sys.argv[1])
