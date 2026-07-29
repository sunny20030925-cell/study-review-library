#!/usr/bin/env python3
from __future__ import annotations

import json, math, re, sys
from collections import Counter
from pathlib import Path

BOOK='mathematical-economics'
VERSION='2026.07.29-1'


def main(site_root: str, expected_library: str) -> None:
    site=Path(site_root); root=site/'books'/BOOK
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    checks=0
    def ck(cond,msg):
        nonlocal checks
        checks+=1
        if not cond: raise AssertionError(msg)

    # Round 1: structure, coverage, PWA paths, IDs and rendered formula hygiene.
    ck(library['version']==expected_library,'library version')
    ck(len(ids)==16 and ids[-3:]==['computer-fundamentals','game-theory',BOOK],f'canonical tail {ids[-3:]}')
    ck(len(ids)==len(set(ids)),'unique book ids')
    ck(manifest['id']==questions['bookId']==BOOK,'book IDs')
    ck(manifest['version']==questions['version']==VERSION,'content version')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']; appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters'); ck(len(appendices)==3,'3 appendices')
    ck(questions['count']==len(questions['items'])==100,'100 questions')
    ck(Counter(x['chapterId'] for x in questions['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions per chapter')
    ck(len({x['id'] for x in questions['items']})==100,'unique question IDs')
    ck(len(search['entries'])==150,'150 search entries')
    sections=['本章要解決的問題','白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']
    corpus=[]
    for ch in chapters:
        p=root/ch['file']; ck(p.is_file(),f'missing {ch["id"]}')
        text=p.read_text(encoding='utf-8'); plain=re.sub(r'<[^>]+>','',text); corpus.append(text)
        ck(len(plain)>=650,f'too thin {ch["id"]}: {len(plain)}')
        for sec in sections: ck(sec in text,f'{ch["id"]} missing {sec}')
        ck('<script' not in text.lower(),f'inline script {ch["id"]}')
        ck("\\'" not in text,f'bad derivative-prime markup {ch["id"]}')
    for ap in appendices:
        p=root/ap['file']; ck(p.is_file() and p.stat().st_size>500,f'appendix {ap["id"]}')
        ck("\\'" not in p.read_text(encoding='utf-8'),f'bad prime markup {ap["id"]}')
    full='\n'.join(corpus)
    required=['反矩陣','特徵值','Taylor 近似','全微分','Jacobian','比較靜態','彈性','Hessian','Lagrange','KKT','互補鬆弛','包絡定理','Euler 定理','微積分基本定理','差分方程','微分方程','穩定性']
    for token in required: ck(token in full,f'missing topic {token}')
    logic_tokens=['FOC','必要條件','不是追時間路徑','互補鬆弛','|b|<1','F′(x*)<0']
    for token in logic_tokens: ck(token in full,f'missing logic guard {token}')
    valid={x['id'] for x in manifest['chapters']}
    for e in search['entries']:
        ck(e['chapterId'] in valid,'search chapter id')
        ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
        ck("\\'" not in e['text'],'search bad prime markup')
    figures=sorted((site/'assets/mathematical-economics-svg').glob('*.svg')); ck(len(figures)==20,'20 figures')
    for p in figures:
        x=p.read_text(encoding='utf-8'); ck('<title' in x and '<desc' in x and 'viewBox=' in x,f'accessibility {p.name}'); ck('href="http' not in x and "href='http" not in x,f'remote SVG {p.name}')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"study-library-{expected_library}" in sw,'service worker version')
    for token in [f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',f'./books/{BOOK}/chapters/ch19.html','./assets/mathematical-economics-svg/differential-equations.svg']: ck(token in sw,f'sw path {token}')
    round1=checks
    print(f'MATHEMATICAL_ECONOMICS_QA_ROUND1_OK checks={round1} chapters=20 appendices=3 questions=100 search=150 figures=20')

    # Round 2: independent arithmetic, calculus, optimization and stability reconstruction.
    q={x['id']:x for x in questions['items']}
    exact={
      'ch00-q01':'60。','ch01-q01':'17。','ch01-q02':'x=(10-y)/2。','ch02-q01':'P*=20，Q*=60。','ch03-q01':'[4,10]^T。',
      'ch04-q01':'1。','ch04-q02':'[2,1]^T。','ch05-q01':'2 與 -1。','ch05-q02':'正定。','ch06-q01':'約 102。','ch06-q02':'12。',
      'ch07-q01':'f_x=7，f_y=2。','ch07-q02':'約 0.3。','ch08-q01':'1/4。','ch08-q02':'約 0.1。','ch09-q01':'-2。','ch10-q01':'10。',
      'ch10-q02':'100。','ch11-q01':'(5,4)。','ch11-q02':'負定。','ch12-q01':'x*=5，y*=5。','ch12-q02':'25。','ch13-q01':'x*=3。',
      'ch13-q02':'0。','ch14-q01':'x*=a。','ch14-q02':'V(a)=a^2/2，V′(a)=a。','ch15-q01':'1。','ch15-q02':'2 倍。',
      'ch16-q01':'C(q)=10+q^2+4q。','ch16-q02':'31。','ch17-q01':'110.25。','ch18-q01':'20。','ch19-q01':'20。'}
    for qid,ans in exact.items(): ck(q[qid]['answer']==ans,f'answer {qid}: {q[qid]["answer"]!r}')
    numeric={
      'demand':120-3*20,'linear':5+4*3,'eq_p':(100-20)/(2+2),'eq_q':100-2*20,'det':2*1-1*1,
      'taylor':100+20*.1,'derivative':3*2**2,'fx':2*2+3,'fy':2,'dz':7*.1+2*(-.2),
      'implicit':1/(2*2),'implicit_change':.25*.4,'opt_q':20/2,'opt_value':20*10-10**2,
      'multi_x':10/2,'multi_y':8/2,'lagrange':10/2,'kkt_boundary':3,'cost3':10+3**2+4*3,
      'compound':100*1.05**2,'continuous':math.log(1.05),'difference_ss':10/(1-.5),'differential_ss':6/.3}
    ck(numeric['demand']==60 and numeric['linear']==17,'basic arithmetic')
    ck(numeric['eq_p']==20 and numeric['eq_q']==60,'equilibrium')
    ck(numeric['det']==1,'determinant')
    ck(numeric['taylor']==102 and numeric['derivative']==12,'calculus')
    ck(numeric['fx']==7 and numeric['fy']==2 and abs(numeric['dz']-.3)<1e-12,'total differential')
    ck(numeric['implicit']==.25 and abs(numeric['implicit_change']-.1)<1e-12,'implicit comparative statics')
    ck(numeric['opt_q']==10 and numeric['opt_value']==100,'univariate optimization')
    ck(numeric['multi_x']==5 and numeric['multi_y']==4,'multivariate optimization')
    ck(numeric['lagrange']==5 and numeric['kkt_boundary']==3,'constrained optimization')
    ck(numeric['cost3']==31,'integration')
    ck(abs(numeric['compound']-110.25)<1e-12 and abs(numeric['continuous']-0.04879016417)<1e-10,'growth rates')
    ck(numeric['difference_ss']==20 and numeric['differential_ss']==20,'dynamic steady states')
    negative=['ch05-q05','ch08-q05','ch10-q05','ch12-q05','ch13-q05','ch16-q05','ch18-q05']
    for qid in negative: ck(q[qid]['answer']=='錯。',f'negative gate {qid}')
    ck(q['ch17-q02']['answer']=='g=ln(1.05)，約 0.04879。','continuous-rate gate')
    ck(q['ch18-q02']['answer']=='交替震盪並收斂。','difference stability gate')
    ck(q['ch19-q02']['answer']=='穩定。','differential stability gate')
    ck(manifest['releaseNotes'][0]['version']==VERSION,'release note')
    round2=checks-round1
    print(f'MATHEMATICAL_ECONOMICS_QA_ROUND2_OK checks={round2} numeric_rechecks={len(numeric)} exact_answer_rechecks={len(exact)} high_risk_logic_gates=10')
    print(f'MATHEMATICAL_ECONOMICS_QA_OK total_checks={checks} books=16 library={expected_library}')


if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_mathematical_economics.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
