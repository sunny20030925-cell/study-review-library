from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path

BOOK='macroeconomics'
VERSION='2026.07.29-1'
LIB='2026.07.29-8'
EXPECTED_ORDER=['calculus','accounting','economics','statistics','commercial-law','cost-accounting','macroeconomics']
checks=0

def ck(cond, msg):
    global checks
    checks += 1
    if not cond: raise AssertionError(msg)

def main(arg):
    site=Path(arg)
    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ck(manifest['id']==BOOK,'manifest id')
    ck(manifest['version']==questions['version']==VERSION,'book version')
    ck(lib['version']==LIB,'library version')
    ck([b['id'] for b in lib['books']]==EXPECTED_ORDER,'seven-book order')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']
    appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'chapter count')
    ck(len(appendices)==3,'appendix count')
    ck(questions['count']==100==len(questions['items']),'question count')
    ck(Counter(q['chapterId'] for q in questions['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions each chapter')
    ck(len({q['id'] for q in questions['items']})==100,'unique question ids')
    ck(len(search['entries'])==143,'search count')
    qmap={q['id']:q for q in questions['items']}
    expected={
      'ch00-q03':f'約 {5-3}%。',
      'ch01-q04':f'S={1000-650-200}，I={1000-650-200}。',
      'ch01-q05':f'NX={300-380}。',
      'ch02-q01':f'{(126-120)/120:.0%}。',
      'ch02-q03':f'{2.4/2.0*100:.0f}。',
      'ch02-q04':f'約 {6-2}%。',
      'ch03-q01':f'約 {50/(900+50)*100:.2f}%。',
      'ch03-q04':f'{0.02/(0.02+0.18):.0%}。',
      'ch04-q03':f'約 {2+0.3*4+0.7*1:.1f}%。',
      'ch06-q01':f'私人儲蓄 {1200-250-700}、政府儲蓄 {250-300}、國民儲蓄 {1200-700-300}。',
      'ch07-q01':f'{7000/10000:g}。',
      'ch09-q03':f'{1/0.1:g}。',
      'ch10-q03':f'約由 {2+1}% 升到 {2+4}%。',
      'ch11-q02':f'NT${10/(1-0.75):.0f} 億。',
      'ch11-q03':f'{-0.75/(1-0.75):g}。',
      'ch16-q03':f'約增加 {(0.04-0.02)*1*100:.0f} 個 GDP 百分點。',
      'ch17-q01':'約不變。',
      'ch18-q01':f'{500-420}。',
    }
    for qid, ans in expected.items(): ck(qmap[qid]['answer']==ans,f'{qid}: {qmap[qid]["answer"]!r} != {ans!r}')
    text_all=[]
    for ch in manifest['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>500,f'chapter file {ch["id"]}')
        txt=p.read_text(encoding='utf-8'); text_all.append(txt)
        ck('\f' not in txt and '\t' not in txt,f'control chars {ch["id"]}')
        ck('<script' not in txt.lower(),f'no inline script {ch["id"]}')
        if ch['kind']=='chapter': ck('理解檢查' in txt,f'practice {ch["id"]}')
    full='\n'.join(text_all)
    for token in ['名目','實質','GDP','CPI','自然失業率','成長會計','Solow','黃金律','可貸資金','恆常所得','Tobin','貨幣乘數','Fisher','Keynesian Cross','定額稅乘數','IS–LM','預期通膨固定','總合需求','Phillips','初級盈餘','\\Delta b\\approx(r-g)b-ps','Taylor','實質匯率','Mundell','不可能三角']:
        ck(token in full,f'missing core token {token}')
    core_titles='|'.join(ch['title'] for ch in chapters)
    for excluded in ['Ramsey–Cass–Koopmans','世代交疊模型','DSGE','動態規劃','Hamiltonian']:
        ck(excluded not in core_titles,f'advanced topic promoted to core chapter: {excluded}')
    for overclaim in ['S-I=NX 就是完整國際收支','財政政策永遠有效','貨幣政策永遠無效','固定匯率下貨幣政策一定完全有效']:
        ck(overclaim not in full,f'forbidden overclaim {overclaim}')
    ck('NT$' in full,'TWD examples')
    ck('NT$/US$' in full or 'NT$／US$' in full,'FX quote convention')
    figs=sorted((site/'assets/macroeconomics-svg').glob('*.svg')); ck(len(figs)==20,'figure count')
    for f in figs:
        s=f.read_text(encoding='utf-8')
        ck('<title' in s and '<desc' in s and 'viewBox=' in s,f'svg accessibility {f.name}')
        ck('href="http' not in s and "href='http" not in s,f'no remote svg asset {f.name}')
    ids={x['id'] for x in manifest['chapters']}
    for e in search['entries']:
        ck(e['chapterId'] in ids,'search chapter id')
        ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
        ck(isinstance(e['page'],int) and e['page']>=0,'search page')
    sw=(site/'sw.js').read_text(encoding='utf-8')
    for token in ['study-library-2026-07-29-8','./books/macroeconomics/manifest.json','./books/macroeconomics/questions.json','./books/macroeconomics/search.json','./books/macroeconomics/chapters/ch19.html','./books/macroeconomics/chapters/appendix-c.html','./assets/macroeconomics-svg/mundell-fleming.svg']:
        ck(token in sw,f'sw cache {token}')
    print(f'MACROECONOMICS_QA_OK checks={checks} chapters=20 appendices=3 questions=100 search=143 figures=20 numeric_rechecks={len(expected)}')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python validate_macroeconomics.py SITE_ROOT')
    main(sys.argv[1])
