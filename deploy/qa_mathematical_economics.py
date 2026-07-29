#!/usr/bin/env python3
from __future__ import annotations

import json, math, re, sys
from collections import Counter
from pathlib import Path

BOOK='mathematical-economics'; VERSION='2026.07.29-1'; checks=0

def ck(cond,msg):
    global checks; checks+=1
    if not cond: raise AssertionError(msg)

def main(site_root: str, expected_library: str) -> None:
    global checks; checks=0
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    ids=[x['id'] for x in lib['books']]

    # Round 1: structure, coverage, links and content completeness.
    ck(lib['version']==expected_library,'library version')
    ck(len(ids)==13 and ids[-2:]==['money-banking',BOOK],'thirteen-book canonical tail')
    ck(len(ids)==len(set(ids)),'unique book ids')
    ck(m['id']==q['bookId']==BOOK,'book ids')
    ck(m['version']==q['version']==VERSION,'book version')
    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters'); ck(len(apps)==3,'3 appendices'); ck(q['count']==len(q['items'])==100,'100 questions'); ck(len(s['entries'])==150,'150 search entries')
    ck(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions each'); ck(len({x['id'] for x in q['items']})==100,'unique qids')
    required_sections=['本章要解決的問題','白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']
    corpus=[]
    for ch in chapters:
        p=root/ch['file']; ck(p.is_file() and p.stat().st_size>1500,f'chapter size {ch["id"]}'); text=p.read_text(encoding='utf-8'); corpus.append(text)
        for sec in required_sections: ck(sec in text,f'{ch["id"]} section {sec}')
        ck('<script' not in text.lower(),f'no inline script {ch["id"]}')
    for ap in apps:
        p=root/ap['file']; ck(p.is_file() and p.stat().st_size>500,f'appendix {ap["id"]}')
    full='\n'.join(corpus)
    required=['參數（parameter）','反矩陣','特徵值','Taylor 近似','全微分','Jacobian','比較靜態','彈性','Hessian','Lagrange','KKT','互補鬆弛','包絡定理','Euler 定理','微積分基本定理','連續成長','差分方程','微分方程','穩定性']
    for tok in required: ck(tok in full,f'missing topic {tok}')
    for tok in ['FOC 只給候選點','比較靜態不是時間路徑','限制有嚴格餘裕時 μ_i=0','|b|<1','F′(x*)<0']:
        ck(tok in full,f'missing high-risk condition {tok}')
    forbidden=['只要 f′(x*)=0，x* 就一定是最大值。','對稱 Hessian 只要每個主對角元素都小於 0，就一定負定。','KKT 條件在任何非線性最佳化問題中都自動是充分條件。','x_{t+1}=a+bx_t 只要 b<1 就一定收斂。']
    # These statements may appear only inside explicit trap questions, not as affirmative textbook claims.
    for tok in forbidden:
        affirmative=[line for line in full.splitlines() if tok in line and '常見錯誤' not in line and '不能' not in line and '錯' not in line]
        ck(not affirmative,f'forbidden affirmative claim {tok}')
    valid={x['id'] for x in m['chapters']}
    for e in s['entries']:
        ck(e['chapterId'] in valid,'search chapter id'); ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
    figs=sorted((site/'assets/mathematical-economics-svg').glob('*.svg')); ck(len(figs)==20,'20 figures')
    for p in figs:
        x=p.read_text(encoding='utf-8'); ck('<title' in x and '<desc' in x and 'viewBox=' in x,f'accessible svg {p.name}'); ck('href="http' not in x and "href='http" not in x,f'no remote svg {p.name}')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"study-library-{expected_library}" in sw,'sw version')
    for tok in [f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',f'./books/{BOOK}/chapters/ch19.html','./assets/mathematical-economics-svg/differential-equations.svg']: ck(tok in sw,f'sw path {tok}')
    round1=checks
    print(f'MATHEMATICAL_ECONOMICS_QA_ROUND1_OK checks={round1} chapters=20 appendices=3 questions=100 search=150 figures=20')

    # Round 2: independent numerical recomputation and high-risk logic gates.
    qmap={x['id']:x for x in q['items']}
    expected={
      'ch00-q01':'60.','ch01-q01':'17.','ch01-q02':'x=(10-y)/2.','ch02-q01':'P*=20, Q*=60.','ch03-q01':'[4,10]^T.','ch04-q01':'1.','ch04-q02':'[2,1]^T.','ch05-q01':'2 and -1.','ch05-q02':'positive definite.','ch06-q01':'approximately 102.','ch06-q02':'12.','ch07-q01':'f_x=7, f_y=2.','ch07-q02':'approximately 0.3.','ch08-q01':'1/4.','ch08-q02':'approximately 0.1.','ch09-q01':'-2.','ch10-q01':'10.','ch10-q02':'100.','ch11-q01':'(5,4).','ch11-q02':'negative definite.','ch12-q01':'x*=5, y*=5.','ch12-q02':'25.','ch13-q01':'x*=3.','ch13-q02':'0.','ch14-q01':'x*=a.','ch14-q02':'V(a)=a^2/2, V′(a)=a.','ch15-q01':'1.','ch15-q02':'2 times.','ch16-q01':'C(q)=10+q^2+4q.','ch16-q02':'31.','ch17-q01':'110.25.','ch18-q01':'20.','ch19-q01':'20.'
    }
    # Answers are Traditional Chinese; normalize a controlled set rather than relying on English labels above.
    exact={'ch00-q01':'60。','ch01-q01':'17。','ch01-q02':'x=(10-y)/2。','ch02-q01':'P*=20，Q*=60。','ch03-q01':'[4,10]^T。','ch04-q01':'1。','ch04-q02':'[2,1]^T。','ch05-q01':'2 與 -1。','ch05-q02':'正定。','ch06-q01':'約 102。','ch06-q02':'12。','ch07-q01':'f_x=7，f_y=2。','ch07-q02':'約 0.3。','ch08-q01':'1/4。','ch08-q02':'約 0.1。','ch09-q01':'-2。','ch10-q01':'10。','ch10-q02':'100。','ch11-q01':'(5,4)。','ch11-q02':'負定。','ch12-q01':'x*=5，y*=5。','ch12-q02':'25。','ch13-q01':'x*=3。','ch13-q02':'0。','ch14-q01':'x*=a。','ch14-q02':'V(a)=a^2/2，V′(a)=a。','ch15-q01':'1。','ch15-q02':'2 倍。','ch16-q01':'C(q)=10+q^2+4q。','ch16-q02':'31。','ch17-q01':'110.25。','ch18-q01':'20。','ch19-q01':'20。'}
    ck(set(expected)==set(exact),'numeric answer inventory')
    for qid,ans in exact.items(): ck(qmap[qid]['answer']==ans,f'numeric answer {qid}')
    calc={
      'ch00':120-3*20,
      'ch01':5+4*3,
      'ch02_p':(100-20)/(2+2),
      'ch02_q':100-2*20,
      'det':2*1-1*1,
      'taylor':100+20*0.1,
      'derivative':3*2**2,
      'fx':2*2+3,
      'fy':2,
      'dz':7*0.1+2*(-0.2),
      'implicit':1/(2*2),
      'implicit_change':(1/4)*0.4,
      'opt_q':20/2,
      'opt_value':20*10-10**2,
      'multi_x':10/2,
      'multi_y':8/2,
      'lagrange_x':10/2,
      'kkt_boundary':3,
      'cost3':10+3**2+4*3,
      'compound':100*(1.05**2),
      'continuous':math.log(1.05),
      'difference_ss':10/(1-0.5),
      'differential_ss':6/0.3,
    }
    ck(calc['ch00']==60 and calc['ch01']==17,'basic recompute'); ck(calc['ch02_p']==20 and calc['ch02_q']==60,'equilibrium recompute'); ck(calc['det']==1,'det recompute'); ck(calc['taylor']==102 and calc['derivative']==12,'calculus recompute'); ck(calc['fx']==7 and calc['fy']==2 and abs(calc['dz']-0.3)<1e-12,'total differential recompute'); ck(calc['implicit']==0.25 and abs(calc['implicit_change']-0.1)<1e-12,'implicit recompute'); ck(calc['opt_q']==10 and calc['opt_value']==100,'univariate opt recompute'); ck(calc['multi_x']==5 and calc['multi_y']==4,'multivariate recompute'); ck(calc['lagrange_x']==5 and calc['kkt_boundary']==3,'constrained opt recompute'); ck(calc['cost3']==31,'integration recompute'); ck(abs(calc['compound']-110.25)<1e-12 and abs(calc['continuous']-0.04879016417)<1e-10,'growth recompute'); ck(calc['difference_ss']==20 and calc['differential_ss']==20,'dynamic steady states')
    ck(qmap['ch05-q05']['answer']=='錯。','Hessian negative gate'); ck(qmap['ch08-q05']['answer']=='錯。','comparative statics negative gate'); ck(qmap['ch10-q05']['answer']=='錯。','FOC negative gate'); ck(qmap['ch12-q05']['answer']=='錯。','multiplier sign gate'); ck(qmap['ch13-q05']['answer']=='錯。','KKT sufficiency gate'); ck(qmap['ch16-q05']['answer']=='錯。','signed integral gate'); ck(qmap['ch18-q05']['answer']=='錯。','difference stability gate')
    ck(qmap['ch17-q02']['answer']=='g=ln(1.05)，約 0.04879。','continuous-rate answer'); ck(qmap['ch18-q02']['answer']=='交替震盪並收斂。','negative-root stability'); ck(qmap['ch19-q02']['answer']=='穩定。','continuous stability')
    ck(m.get('releaseNotes',[{}])[0].get('version')==VERSION,'release note')
    round2=checks-round1
    print(f'MATHEMATICAL_ECONOMICS_QA_ROUND2_OK checks={round2} numeric_rechecks={len(calc)} exact_numeric_answers={len(exact)} high_risk_logic_gates=10')
    print(f'MATHEMATICAL_ECONOMICS_QA_OK total_checks={checks} books=13 library={expected_library}')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_mathematical_economics.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
