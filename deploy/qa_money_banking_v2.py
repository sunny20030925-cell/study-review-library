#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from collections import Counter
from pathlib import Path

BOOK='money-banking'
VERSION='2026.07.29-2'
checks=0

def ck(cond,msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)

def main(site_root: str, expected_library: str) -> None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in lib['books']]

    ck(lib['version']==expected_library,'library version')
    ck(len(ids)==12 and ids[-3:]==['international-economics','public-finance','money-banking'],'twelve-book canonical tail')
    ck(len(ids)==len(set(ids)),'unique library ids')
    ck(manifest['id']==BOOK and manifest['version']==VERSION,'manifest v2')
    ck(questions['bookId']==BOOK and questions['version']==VERSION,'questions v2')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']
    appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters')
    ck(len(appendices)==3,'3 appendices')
    ck(questions['count']==len(questions['items'])==100,'100 questions')
    ck(Counter(q['chapterId'] for q in questions['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions per chapter')
    ck(len({q['id'] for q in questions['items']})==100,'unique question ids')
    ck(len(search['entries'])==150,'150 search entries')
    ck(manifest.get('releaseNotes',[{}])[0].get('version')==VERSION,'v2 release note first')

    alltext=[]
    for ch in manifest['chapters']:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>1200,f'chapter/appendix file {ch["id"]}')
        text=p.read_text(encoding='utf-8'); alltext.append(text)
    full='\n'.join(alltext)

    required = [
        '票面利率','當期收益率','到期殖利率','持有期間報酬率','小幅殖利率變動','凸性',
        '個體審慎監理','總體審慎政策','LCR','NSFR','具償付／還款能力','流動性不足',
        '準備貨幣（reserve money／base money，常稱貨幣基數）','銀行存放央行的準備只是準備貨幣的組成之一',
        '跨行清算','資金成本','簡單存款乘數','不能拿來斷言準備金增加 1 元',
        '準備金制度、貼現窗口制度、公開市場操作、金融機構轉存款與選擇性信用管理',
        'Fisher equation','Fisher effect','(1+i)=(1+r)(1+π^e)','i≈r+π^e',
        '量化寬鬆（QE）','不是財政支出','固定用 <code>E = NT$/US$</code>','新臺幣貶值'
    ]
    for tok in required: ck(tok in full,f'missing corrected token: {tok}')

    forbidden = [
        '銀行可以無限制憑空放款','銀行放款完全不受資本與流動性限制','貨幣乘數在現實中永遠等於 1/rr',
        '準備金增加 1 元，現實世界的 M2 就必定增加固定倍數','QE 必然使 M2 等比例增加',
        '任何資不抵債銀行都應由央行無條件救助','殖利率曲線反轉必然造成衰退',
        '任何匯率上升都代表本幣升值','Fisher equation 已經證明預期通膨必然造成名目利率等幅上升'
    ]
    for tok in forbidden: ck(tok not in full,f'forbidden stale overclaim: {tok}')

    for cid in ['ch02','ch03','ch08','ch09','ch10','ch13','ch15','ch18','ch19']:
        text=(root/'chapters'/f'{cid}.html').read_text(encoding='utf-8')
        ck('二次複核' in text,f'v2 correction block {cid}')

    qmap={q['id']:q for q in questions['items']}
    note_qids=['ch02-q05','ch03-q01','ch08-q01','ch09-q01','ch10-q01','ch10-q02','ch19-q02']
    for qid in note_qids:
        ck('二次複核補充' in qmap[qid]['explanation'],f'question clarification {qid}')

    expected={
      'ch02-q01':'NT$10,000。','ch02-q02':'NT$108,160。','ch02-q05':'約 4%。',
      'ch03-q01':'約下降 2.5%。','ch06-q01':'NT$80 億。','ch06-q02':'0.8%。','ch06-q03':'10%。','ch06-q04':'NT$30 億。',
      'ch07-q01':'-NT$200 億。','ch07-q02':'約 -NT$2 億。','ch10-q01':'10。','ch10-q02':'約 3.43。',
      'ch11-q01':'NT$160 萬。','ch12-q02':'增加 NT$50 億。','ch15-q02':'約 5%。','ch15-q03':'約由 5% 升到 7%。',
      'ch16-q02':'3%。','ch17-q01':'6.5%。','ch19-q02':'由 NT$310,000 升到 NT$320,000。'
    }
    for qid,ans in expected.items(): ck(qmap[qid]['answer']==ans,f'numeric answer preserved {qid}')
    recompute={
      'pv':10500/1.05,
      'fv':100000*(1.04**2),
      'duration':-5*0.005*100,
      'bank_equity':1000-920,
      'roa':8/1000*100,
      'roe':8/80*100,
      'net_interest':80-50,
      'gap':300-500,
      'gap_income':(300-500)*0.01,
      'simple_multiplier':1/0.1,
      'general_multiplier':1.2/(0.1+0.05+0.2),
      'real_balance':200/1.25,
      'omo':50,
      'fisher':8-3,
      'fisher_from':3+2,
      'fisher_to':3+4,
      'phillips':2+0.5*2,
      'taylor':1+4+0.5*(4-2)+0.5*1,
      'fx_from':31*10000,
      'fx_to':32*10000,
    }
    ck(abs(recompute['pv']-10000)<1e-9,'recompute pv')
    ck(abs(recompute['fv']-108160)<1e-9,'recompute fv')
    ck(abs(recompute['duration']+2.5)<1e-9,'recompute duration')
    ck(recompute['bank_equity']==80,'recompute bank equity')
    ck(abs(recompute['roa']-0.8)<1e-9,'recompute roa')
    ck(abs(recompute['roe']-10)<1e-9,'recompute roe')
    ck(recompute['net_interest']==30,'recompute net interest')
    ck(recompute['gap']==-200 and recompute['gap_income']==-2,'recompute gap')
    ck(recompute['simple_multiplier']==10,'recompute simple multiplier')
    ck(abs(recompute['general_multiplier']-3.4285714286)<1e-6,'recompute general multiplier')
    ck(recompute['real_balance']==160,'recompute real balance')
    ck(recompute['omo']==50,'recompute omo')
    ck(recompute['fisher']==5 and recompute['fisher_from']==5 and recompute['fisher_to']==7,'recompute fisher examples')
    ck(recompute['phillips']==3,'recompute phillips')
    ck(recompute['taylor']==6.5,'recompute taylor')
    ck(recompute['fx_from']==310000 and recompute['fx_to']==320000,'recompute fx')

    valid_ids={x['id'] for x in manifest['chapters']}
    for e in search['entries']:
        ck(e['chapterId'] in valid_ids,'search chapter id')
        ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
    search_corpus='\n'.join(e['text'] for e in search['entries'])
    for tok in ['Fisher equation','簡單存款乘數','具還款能力但流動性不足','E=NT$/US$']:
        ck(tok in re.sub(r'<[^>]+>','',search_corpus),f'search corrected concept {tok}')

    figs=sorted((site/'assets/money-banking-svg').glob('*.svg'))
    ck(len(figs)==20,'20 figures')
    for p in figs:
        svg=p.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg,f'svg accessibility {p.name}')
        ck('href="http' not in svg and "href='http" not in svg,f'no remote svg {p.name}')

    sw=(site/'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw,'sw final library version')
    for tok in [f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',f'./books/{BOOK}/chapters/ch19.html','./assets/money-banking-svg/open-economy-money.svg']:
        ck(tok in sw,f'sw money path {tok}')

    print(f'MONEY_BANKING_V2_QA_OK checks={checks} books=12 library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20 corrections=9 question_adjustments=7 quantitative_rechecks=20')

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: qa_money_banking_v2.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
