from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

BOOK='cost-accounting'; VERSION='2026.07.29-2'; LIB='2026.07.29-8'
checks=0

def ck(cond, msg):
    global checks
    checks += 1
    if not cond: raise AssertionError(msg)

def main(arg):
    site=Path(arg); root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ck(manifest['id']==BOOK,'manifest id')
    ck(manifest['version']==questions['version']==VERSION,'book version')
    ck(manifest['releaseNotes'][0]['version']==VERSION,'latest release note')
    ck('獨立二次內容審計' in manifest['releaseNotes'][0]['title'],'release title')
    ck(lib['version']==LIB,'library version')
    ck([b['id'] for b in lib['books']].count(BOOK)==1,'library contains book once')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']
    appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==19,'chapter count')
    ck(len(appendices)==3,'appendix count')
    ck(questions['count']==95==len(questions['items']),'question count')
    ck(Counter(q['chapterId'] for q in questions['items'])=={f'ch{i:02d}':5 for i in range(19)},'five questions each')
    ck(len({q['id'] for q in questions['items']})==95,'unique question ids')
    ck(len(search['entries'])==150,'search count')
    qmap={q['id']:q for q in questions['items']}

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
      'ch14-q01':f'NT${5400*(31-30):,} U。',
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

    ck(qmap['ch00-q05']['answer']=='直接人工與製造費用。','conversion cost answer')
    ck('檢驗點' in qmap['ch09-q03']['answer'],'normal spoilage inspection point')
    ck('銷售價值通常不重大' in qmap['ch12-q05']['answer'],'by-product distinction')
    ck('AQP' in qmap['ch14-q01']['question'] and '5,400' in qmap['ch14-q01']['answer'],'purchase quantity price variance')
    ck('AQU' in qmap['ch14-q02']['question'],'usage quantity variance')
    ck('合理分攤' in qmap['ch16-q04']['explanation'],'absorption allocation boundary')
    ck(qmap['ch17-q05']['answer']=='在當期認列為費用。','unallocated overhead treatment')

    texts=[]
    for ch in manifest['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>400,f'chapter file {ch["id"]}')
        html=p.read_text(encoding='utf-8'); texts.append(html)
        ck('<h2' in html,f'h2 {ch["id"]}')
        ck('理解檢查' in html or ch['kind']=='appendix',f'practice {ch["id"]}')
        ck('<script' not in html.lower(),f'no inline script {ch["id"]}')
        ck('\t' not in html,f'no tab-corrupted formula {ch["id"]}')
    full='\n'.join(texts)
    plain=' '.join(BeautifulSoup(full,'html.parser').get_text(' ',strip=True).split())

    required=(
      '主要成本（prime costs）','加工成本（conversion costs）','淨進料',
      '銷售組合固定','固定製造費用的遞延或釋放','每一成本成分都要用自己的約當產量',
      '期初 WIP 已帶入的轉入成本屬前期成本','尚未到達檢驗點',
      '物量法（physical-measure method）','副產品（by-product）',
      '實際購買量 AQP','實際使用量 AQU','MPV=AQP','MQV=SP',
      '期末存貨內含固定OH-期初存貨內含固定OH','正常產能原則',
      '產量異常偏低時','未分攤部分應在當期認列','產量異常偏高時',
      'actual quantity purchased','actual quantity used',
    )
    for token in required: ck(token in plain or token in full,f'missing corrected token {token}')
    forbidden=(
      '且生產量與銷售量差異不致扭曲分析',
      '通常由合格產品吸收；異常損壞',
      '乘上實際購買或實際使用數量',
      '\\[MPV=AQ\\times(AP-SP)\\]',
      '\\[MQV=SP\\times(AQ-SQ)\\]',
      '對外財務報導的存貨成本通常採吸收成本觀念',
      '\\[WA單位成本=(期初WIP成本+本期新增成本)\\div WA約當產量\\]',
    )
    for token in forbidden: ck(token not in full,f'obsolete wording remains: {token}')

    ck('產品成本 = 直接材料 + 直接人工 + 製造費用' in full,'product cost formula')
    ck('COGM = 期初在製品 + 本期製造成本 - 期末在製品' in full,'COGM formula')
    ck('AQP\\times(AP-SP)' in full and 'AQU\\times(AP-SP)' in full,'price variance formulas')
    ck('SP\\times(AQU-SQ)' in full,'quantity variance formula')
    ck('期末存貨內含固定OH-期初存貨內含固定OH' in full,'income reconciliation')
    ck('主預算' in (root/'chapters/ch18.html').read_text(encoding='utf-8'),'scope boundary retained')

    figs=sorted((site/'assets/cost-accounting-svg').glob('*.svg')); ck(len(figs)==19,'figure count')
    for f in figs:
        s=f.read_text(encoding='utf-8')
        ck('<title' in s and '<desc' in s and 'viewBox' in s,f'svg accessibility {f.name}')
        ck('href="http' not in s and "href='http" not in s,f'no remote svg {f.name}')

    sw=(site/'sw.js').read_text(encoding='utf-8')
    for token in [f'study-library-{LIB}','./books/cost-accounting/manifest.json','./books/cost-accounting/questions.json','./books/cost-accounting/search.json','./books/cost-accounting/chapters/ch18.html','./books/cost-accounting/chapters/appendix-c.html','./assets/cost-accounting-svg/integration.svg']:
        ck(token in sw,f'sw cache {token}')

    ids={x['id'] for x in manifest['chapters']}
    seen=set()
    for e in search['entries']:
        ck(e['chapterId'] in ids,'search chapter id')
        ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
        ck(isinstance(e['page'],int) and e['page']>=0,'search page')
        key=(e['chapterId'],e['page']); ck(key not in seen,'unique search page'); seen.add(key)
    for token in ['主要成本','副產品','AQP','正常產能規則']:
        ck(any(token in e['text'] or token in e['title'] for e in search['entries']),f'search includes {token}')

    print(f'COST_ACCOUNTING_V2_QA_OK checks={checks} chapters=19 appendices=3 questions=95 search=150 figures=19 numeric_rechecks={len(expected)}')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python validate_cost_accounting.py SITE_ROOT')
    main(sys.argv[1])
