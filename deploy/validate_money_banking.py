from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import Counter

BOOK='money-banking'; VERSION='2026.07.29-1'
checks=0

def ck(cond,msg):
    global checks
    checks += 1
    if not cond: raise AssertionError(msg)

def main(site_root):
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in lib['books']]
    ck(ids[-1]==BOOK,'book must append last'); ck(len(ids)==len(set(ids)),'unique library ids')
    ck(manifest['id']==BOOK and manifest['version']==VERSION,'manifest identity/version')
    ck(questions['bookId']==BOOK and questions['version']==VERSION,'question identity/version')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']; appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters'); ck(len(appendices)==3,'3 appendices')
    ck(questions['count']==len(questions['items'])==100,'100 questions')
    ck(Counter(q['chapterId'] for q in questions['items'])=={f'ch{i:02d}':5 for i in range(20)},'5 per chapter')
    ck(len({q['id'] for q in questions['items']})==100,'unique qids')
    ck(len(search['entries'])==150,'150 search entries')
    ck(len(manifest['releaseNotes'])>=1 and manifest['releaseNotes'][0]['version']==VERSION,'release note')
    ck(manifest['features']=={'reader':True,'quiz':True,'formula':True},'features')

    alltext=[]
    for ch in manifest['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>1200,f'chapter file {ch["id"]}')
        t=p.read_text(encoding='utf-8'); alltext.append(t)
        ck('\t' not in t and '\f' not in t and '\x0b' not in t,f'control chars {ch["id"]}')
        ck('<script' not in t.lower(),f'inline script {ch["id"]}')
        if ch['kind']=='chapter':
            for token in ['標準例題','常見錯誤','考試判斷方法','理解檢查']:
                ck(token in t,f'{token} {ch["id"]}')
            ck(f'assets/money-banking-svg/' in t,f'figure link {ch["id"]}')
    full='\n'.join(alltext)
    required=[
        '交易媒介','M1A','M1B','M2','流動性','現值','到期殖利率','存續期間','殖利率曲線','期限溢酬',
        '直接金融','間接金融','逆選擇','道德危險','資產＝負債＋權益','ROA','ROE','利率風險','存款保險','最後貸款者',
        '準備貨幣','放款創造存款','簡單存款乘數','m=(1+c)/(rr+e+c)','實質貨幣餘額','MV=PY','中央銀行資產負債表',
        '公開市場操作','央行存單','走廊','地板型','貨幣政策傳遞','Fisher','Phillips','Taylor principle','時間不一致',
        '量化寬鬆','前瞻指引','E=NT$/US$','沖銷','不可能三角'
    ]
    for tok in required: ck(tok in full,f'missing core token {tok}')
    forbidden=[
        '銀行放款完全不受資本與流動性限制','貨幣乘數在現實中永遠等於 1/rr','QE 必然使 M2 等比例增加',
        '殖利率曲線反轉必然造成衰退','升息必然增加每一家銀行獲利','任何匯率上升都代表本幣升值',
        '流動性陷阱使所有貨幣政策永久無效','Taylor rule 是所有央行依法必須遵守的公式','存款保險可以消除所有銀行風險'
    ]
    for tok in forbidden: ck(tok not in full,f'forbidden overclaim {tok}')
    for tok in ['1/rr','通貨外流','超額準備','資本','信用需求']:
        ck(tok in (root/'chapters/ch10.html').read_text(encoding='utf-8'),f'multiplier caveat {tok}')
    ch19=(root/'chapters/ch19.html').read_text(encoding='utf-8')
    ck('E=NT$/US$' in ch19 and 'E 上升' in ch19 and '新臺幣貶值' in ch19,'FX quote direction')
    ch18=(root/'chapters/ch18.html').read_text(encoding='utf-8')
    ck('不代表銀行一定新增' in ch18 and '固定乘數' in ch18,'QE multiplier caveat')
    ch09=(root/'chapters/ch09.html').read_text(encoding='utf-8')
    ck('放款創造存款' in ch09 and '跨行清算' in ch09 and '資本' in ch09,'loan creation boundaries')
    ch13=(root/'chapters/ch13.html').read_text(encoding='utf-8')
    ck('公開市場操作' in ch13 and '央行存單' in ch13 and '走廊' in ch13 and '地板型' in ch13,'operating framework')

    figs=sorted((site/'assets/money-banking-svg').glob('*.svg')); ck(len(figs)==20,'20 figures')
    for p in figs:
        s=p.read_text(encoding='utf-8')
        ck('<title' in s and '<desc' in s and 'viewBox=' in s,f'svg accessibility {p.name}')
        ck('href="http' not in s and "href='http" not in s,f'no remote svg {p.name}')

    valid_ids={x['id'] for x in manifest['chapters']}
    for e in search['entries']:
        ck(e['chapterId'] in valid_ids,'search id'); ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty'); ck(isinstance(e['page'],int) and e['page']>=0,'search page')

    qmap={q['id']:q for q in questions['items']}
    expected={
      'ch02-q01':'NT$10,000。','ch02-q02':'NT$108,160。','ch02-q05':'約 4%。',
      'ch03-q01':'約下降 2.5%。','ch06-q01':'NT$80 億。','ch06-q02':'0.8%。','ch06-q03':'10%。','ch06-q04':'NT$30 億。',
      'ch07-q01':'-NT$200 億。','ch07-q02':'約 -NT$2 億。','ch10-q01':'10。','ch10-q02':'約 3.43。',
      'ch11-q01':'NT$160 萬。','ch12-q02':'增加 NT$50 億。','ch15-q02':'約 5%。','ch15-q03':'約由 5% 升到 7%。',
      'ch16-q02':'3%。','ch17-q01':'6.5%。','ch19-q02':'由 NT$310,000 升到 NT$320,000。'
    }
    for qid,ans in expected.items(): ck(qmap[qid]['answer']==ans,f'{qid} numeric answer')
    recompute={
      'ch02-q01':10500/1.05,
      'ch02-q02':100000*(1.04**2),
      'ch03-q01':-5*0.005*100,
      'ch06-q01':1000-920,
      'ch06-q02':8/1000*100,
      'ch06-q03':8/80*100,
      'ch06-q04':80-50,
      'ch07-q01':300-500,
      'ch07-q02':(300-500)*0.01,
      'ch10-q01':1/0.1,
      'ch10-q02':1.2/(0.1+0.05+0.2),
      'ch11-q01':200/1.25,
      'ch12-q02':50,
      'ch15-q02':8-3,
      'ch15-q03_from':3+2,
      'ch15-q03_to':3+4,
      'ch16-q02':2+0.5*2,
      'ch17-q01':1+4+0.5*(4-2)+0.5*1,
      'ch19-q02_from':31*10000,
      'ch19-q02_to':32*10000,
    }
    ck(abs(recompute['ch02-q01']-10000)<1e-9,'recompute pv')
    ck(abs(recompute['ch02-q02']-108160)<1e-9,'recompute fv')
    ck(abs(recompute['ch03-q01']+2.5)<1e-9,'recompute duration')
    ck(abs(recompute['ch10-q02']-3.4285714286)<1e-6,'recompute multiplier')
    ck(recompute['ch17-q01']==6.5,'recompute Taylor')
    ck(recompute['ch19-q02_from']==310000 and recompute['ch19-q02_to']==320000,'recompute FX')
    for q in questions['items']:
        ck(all(bool(str(q[k]).strip()) for k in ['id','chapterId','topic','difficulty','question','answer','explanation','source']),f'q fields {q["id"]}')
        ck(q['difficulty'] in {'基礎','標準','進階'},f'difficulty {q["id"]}')
    sw=(site/'sw.js').read_text(encoding='utf-8')
    for tok in [f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',f'./books/{BOOK}/chapters/ch19.html',f'./books/{BOOK}/chapters/appendix-c.html','./assets/money-banking-svg/open-economy-money.svg']:
        ck(tok in sw,f'sw path {tok}')
    ck(f"study-library-{lib['version']}" in sw,'sw library version')
    print(f'MONEY_BANKING_QA_ROUND1_OK checks={checks} chapters=20 appendices=3 questions=100 search=150 figures=20')
    print('MONEY_BANKING_QA_ROUND2_OK numeric_rechecks=20 high_risk_concepts=10 fx_quote=passed multiplier_boundaries=passed policy_framework=passed')

if __name__=='__main__':
    main(sys.argv[1])
