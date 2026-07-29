from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

BOOK='cost-accounting'; VERSION='2026.07.29-1'; LIB='2026.07.29-7'
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
    ck([b['id'] for b in lib['books']].count(BOOK)==1,'library contains cost accounting once')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']
    appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==19,'chapter count')
    ck(len(appendices)==3,'appendix count')
    ck(questions['count']==95==len(questions['items']),'question count')
    ck(Counter(q['chapterId'] for q in questions['items'])=={f'ch{i:02d}':5 for i in range(19)},'five questions each chapter')
    ck(len({q['id'] for q in questions['items']})==95,'unique question ids')
    ck(len(search['entries'])==146,'search count')
    qmap={q['id']:q for q in questions['items']}
    # Independent numerical rechecks: each line recomputes from raw inputs rather than trusting prose.
    expected={
      'ch01-q01':f'NT${30000+150000-20000:,}。',
      'ch01-q02':f'NT${160000-12000:,}。',
      'ch01-q03':f'NT${40000+390000-50000:,}。',
      'ch01-q04':f'NT${70000+380000-90000:,}。',
      'ch02-q01':f'NT${18*4000:,}。',
      'ch02-q03':f'NT${(146000-110000)/(9000-5000):g}／機器小時。',
      'ch02-q04':f'NT${146000-9*9000:,}。',
      'ch03-q01':f'NT${500-300:,}。',
      'ch03-q02':f'{(500-300)/500:.0%}。',
      'ch03-q03':f'{int(400000/(500-300)):,} 單位。',
      'ch03-q04':f'{int((400000+120000)/(500-300)):,} 單位。',
      'ch04-q01':f'NT${1200000/60000:g}／機器小時。',
      'ch04-q02':f'NT${20*350:,}。',
      'ch05-q01':f'NT${50000*1.2:,.0f}。',
      'ch05-q02':f'NT${80000+50000+60000:,}。',
      'ch05-q03':f'NT${190000/500:g}／單位。',
      'ch06-q01':f'少分 NT${990000-960000:,}。',
      'ch06-q03':f'多分 NT${810000-780000:,}。',
      'ch07-q01':f'{int(8000+2000*.4):,} 單位。',
      'ch07-q02':f'NT${352000/8800:g}／約當單位。',
      'ch08-q01':f'{int(1000*(1-.6)):,} 單位。',
      'ch08-q02':f'{int(400+6000+2000*.3):,} 單位。',
      'ch09-q01':f'{int(10000*.02):,} 單位。',
      'ch09-q02':f'{260-200:,} 單位。',
      'ch10-q01':f'NT${600000/300:,.0f}／次。',
      'ch10-q02':f'NT${2000*40:,}。',
      'ch11-q01':f'NT${300000/(2000+3000):g}／小時。',
      'ch11-q02':f'NT${2000*60:,}。',
      'ch12-q01':f'NT${900000*600000/(600000+300000):,.0f}。',
      'ch12-q02':f'NT${900000*300000/(600000+300000):,.0f}。',
      'ch12-q03':f'NT${500000-140000:,}。',
      'ch14-q01':f'NT${5200*(31-30):,} U。',
      'ch14-q02':f'NT${30*(5200-5000):,} U。',
      'ch14-q03':f'NT${3900*(205-200):,} U。',
      'ch14-q04':f'NT${200*(4000-3900):,} F。',
      'ch15-q01':f'NT${4200*(13-12):,} U。',
      'ch15-q02':f'NT${12*(4200-4000):,} U。',
      'ch15-q03':f'NT${615000-600000:,} U。',
      'ch15-q04':f'NT${600000-570000:,} U。',
      'ch16-q01':f'NT${300000/10000:g}／單位。',
      'ch16-q02':f'{10000-8500:,} 單位。',
      'ch16-q03':f'NT${(10000-8500)*(300000/10000):,.0f}。',
      'ch17-q01':f'NT${800000/40000:g}／機器小時。',
      'ch17-q02':f'NT${800000/50000:g}／機器小時。',
    }
    for qid, ans in expected.items(): ck(qmap[qid]['answer']==ans, f'{qid}: {qmap[qid]["answer"]!r} != {ans!r}')
    # Structural and content QA.
    text_all=[]
    for ch in manifest['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>400,f'chapter file {ch["id"]}')
        text=p.read_text(encoding='utf-8'); text_all.append(text)
        ck('<h2' in text,f'h2 {ch["id"]}')
        ck('理解檢查' in text or ch['kind']=='appendix',f'practice {ch["id"]}')
        ck('<script' not in text.lower(),f'no inline script {ch["id"]}')
    full='\n'.join(text_all)
    for token in ['成本標的','製成品成本','相關範圍','貢獻邊際','預定製造費用分攤率','分批成本制','少分','約當產量','FIFO','正常損壞','作業基礎成本制','服務部門','聯產品','標準成本','材料價格差異','固定製造費用生產量差異','吸收成本法','實務產能','總額檢核']:
        ck(token in full,f'missing core token {token}')
    core_titles='|'.join(ch['title'] for ch in chapters)
    for excluded in ['主預算','資本預算','責任會計','移轉價格','平衡計分卡','定價決策']:
        ck(excluded not in core_titles,f'cross-subject chapter {excluded}')
    # Currency convention and formula sanity.
    ck('NT$' in full,'TWD examples')
    ck('產品成本 = 直接材料 + 直接人工 + 製造費用' in full,'product cost formula')
    ck('COGM = 期初在製品 + 本期製造成本 - 期末在製品' in full,'COGM formula')
    ck('MPV=AQ' in full and 'MQV=SP' in full,'material variance formulas')
    # SVG accessibility and cache coverage.
    figs=sorted((site/'assets/cost-accounting-svg').glob('*.svg')); ck(len(figs)==19,'figure count')
    for f in figs:
        s=f.read_text(encoding='utf-8')
        ck('<title' in s and '<desc' in s and 'viewBox=' in s,f'svg accessibility {f.name}')
        ck('href="http' not in s and "href='http" not in s,f'no remote svg asset {f.name}')
    sw=(site/'sw.js').read_text(encoding='utf-8')
    for token in [f'study-library-{LIB}', './books/cost-accounting/manifest.json','./books/cost-accounting/questions.json','./books/cost-accounting/search.json','./books/cost-accounting/chapters/ch18.html','./books/cost-accounting/chapters/appendix-c.html','./assets/cost-accounting-svg/integration.svg']:
        ck(token in sw,f'sw cache {token}')
    # Search entries must point to real chapters and nonempty searchable text.
    ids={x['id'] for x in manifest['chapters']}
    for e in search['entries']:
        ck(e['chapterId'] in ids,'search chapter id')
        ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
        ck(isinstance(e['page'],int) and e['page']>=0,'search page')
    print(f'COST_ACCOUNTING_QA_OK checks={checks} chapters=19 appendices=3 questions=95 search=146 figures=19 numeric_rechecks={len(expected)}')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python validate_cost_accounting.py SITE_ROOT')
    main(sys.argv[1])
