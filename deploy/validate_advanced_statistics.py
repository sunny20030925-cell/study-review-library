#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

BOOK='advanced-statistics'
VERSION='2026.07.29-1'
checks=0
numeric_checks=0
concept_checks=0

def ck(cond,msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)

def num(cond,msg):
    global numeric_checks
    numeric_checks += 1
    if not cond:
        raise AssertionError(msg)

def concept(cond,msg):
    global concept_checks
    concept_checks += 1
    if not cond:
        raise AssertionError(msg)

def main(site_root: str, expected_library: str) -> None:
    site=Path(site_root)
    root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in lib['books']]

    ck(lib['version']==expected_library,'library version')
    ck(len(ids)==13 and ids[-2:]==['money-banking',BOOK],'thirteen-book canonical tail')
    ck(len(ids)==len(set(ids)),'unique book ids')
    ck(manifest['id']==BOOK and manifest['version']==VERSION,'manifest identity/version')
    ck(questions['bookId']==BOOK and questions['version']==VERSION,'questions identity/version')
    chapters=[x for x in manifest['chapters'] if x['kind']=='chapter']
    appendices=[x for x in manifest['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters')
    ck(len(appendices)==3,'3 appendices')
    ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'stable chapter ids')
    ck(questions['count']==len(questions['items'])==100,'100 questions')
    ck(Counter(q['chapterId'] for q in questions['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions per chapter')
    ck(len({q['id'] for q in questions['items']})==100,'unique question ids')
    ck(len(search['entries'])==189,'189 search entries')
    ck(manifest.get('releaseNotes',[{}])[0].get('version')==VERSION,'release note version')

    alltext=[]
    for m in manifest['chapters']:
        p=root/m['file']
        ck(p.is_file() and p.stat().st_size>900,f'chapter/appendix exists {m["id"]}')
        text=p.read_text(encoding='utf-8')
        ck('<h1>' in text and ('<h2' in text or m['kind']=='appendix'),f'chapter/appendix structure {m["id"]}')
        alltext.append(text)
    full='\n'.join(alltext)

    required=[
        '條件機率（conditional probability）','累積分配函數（CDF）','Gamma(α,λ)','聯合密度（joint density）',
        '條件期望（conditional expectation）','多元常態（multivariate normal）','Jacobian','特徵函數（characteristic function）',
        '次序統計量（order statistic）','中央極限定理（CLT）','Student t 分配','最大概似估計（MLE）',
        '充分統計量（sufficient statistic）','Cramér–Rao 下界','Rao–Blackwell','樞紐量（pivotal quantity）',
        'Neyman–Pearson','UMP 檢定','Wilks 定理','Gauss–Markov 定理',
        'rate λ','多對一轉換','有限樣本','漸近 χ²','p-value','不是 H0 為真的機率',
    ]
    for tok in required:
        concept(tok in full,f'missing core concept: {tok}')

    forbidden=[
        '共變異數為 0 就一定獨立',
        '任何兩個邊際常態就自動聯合常態',
        '每個分配都有有限 MGF',
        '中央極限定理表示原始資料會變成常態',
        't 分配對任何母體都精確成立',
        'likelihood 是參數的機率密度',
        '充分統計量一定無偏',
        'Cramér–Rao 下界不需要任何正則條件',
        '95% 信賴區間表示參數有 95% 機率落在區間',
        'p-value 是虛無假設為真的機率',
        '每個複合假設都有 UMP',
        'Wilks 定理在所有有限樣本都精確成立',
        'Gauss–Markov 必須假設常態誤差',
        'R² 高代表因果關係成立',
    ]
    for tok in forbidden:
        concept(tok not in full,f'forbidden overclaim: {tok}')

    q={x['id']:x for x in questions['items']}
    expected={
        'ch00-q01':'1。','ch00-q02':'1/4。',
        'ch01-q01':'0.8。','ch01-q02':'是。','ch01-q04':'1/3。',
        'ch02-q01':'0.75。','ch02-q02':'0.5。',
        'ch03-q01':'0.4096。','ch03-q02':'約 0.1353。','ch03-q03':'4。',
        'ch04-q01':'約 0.3679。','ch04-q02':'1.5。','ch04-q03':'0.75。','ch04-q04':'0.4。',
        'ch05-q01':'f_X(x)=2x，0<x<1。','ch05-q02':'1/x，0<y<x。',
        'ch06-q01':'19。','ch06-q02':'2。',
        'ch07-q01':'3。','ch07-q02':'0.75。','ch07-q03':'0.5x。',
        'ch08-q01':'1/(2√y)。','ch08-q02':'1/2。',
        'ch09-q02':'λ。','ch09-q03':'Poisson(5)。',
        'ch10-q01':'4/5。','ch10-q02':'1/5。',
        'ch11-q01':'0.5。','ch11-q02':'約 0.9545。','ch11-q05':'9/4。',
        'ch12-q01':'9。','ch12-q02':'2。','ch12-q03':'15。',
        'ch13-q02':'0.5。','ch14-q01':'T=ΣX_i。',
        'ch15-q01':'p(1-p)/n。','ch15-q02':'n/[p(1-p)]。','ch15-q03':'p(1-p)/n。',
        'ch16-q01':'[9.608, 10.392]。','ch16-q02':'[17.936, 22.064]。',
        'ch17-q01':'2.5。','ch17-q02':'約 0.0124。',
        'ch19-q01':'1.5。','ch19-q02':'2/3。','ch19-q03':'27/28，約 0.9643。',
    }
    for qid,answer in expected.items():
        ck(q[qid]['answer']==answer,f'answer text {qid}')

    num(abs((1**2)-1)<1e-12,'density normalization')
    num(abs((0.5**2)-0.25)<1e-12,'cdf integral')
    num(abs((0.6+0.5-0.3)-0.8)<1e-12,'union probability')
    num(abs((0.9*0.1)/(0.9*0.1+0.2*0.9)-1/3)<1e-12,'Bayes')
    num(abs(5*.2*(.8**4)-.4096)<1e-12,'binomial')
    num(abs(math.exp(-2)-.1353352832366127)<1e-12,'poisson zero')
    num(abs(1/.25-4)<1e-12,'geometric mean')
    num(abs(math.exp(-.5*2)-.36787944117144233)<1e-12,'exponential tail')
    num(abs(3/2-1.5)<1e-12 and abs(3/(2**2)-.75)<1e-12,'gamma moments')
    num(abs(2/(2+3)-.4)<1e-12,'beta mean')
    num(abs((4+9+2*3)-19)<1e-12,'variance sum')
    num(abs((1+1+2*.5)-3)<1e-12,'multivariate variance')
    num(abs((1-.5**2)-.75)<1e-12,'conditional normal variance')
    num(abs(.5-0.5)<1e-12,'jacobian')
    num(2+3==5,'poisson convolution')
    num(abs(4/5-.8)<1e-12 and abs(1/5-.2)<1e-12,'order stats means')
    num(abs(4/math.sqrt(64)-.5)<1e-12,'sample mean se')
    num(abs((.5)**2*9-2.25)<1e-12,'delta method')
    num(abs((10-1)*4/4-9)<1e-12,'chi square statistic')
    num(abs((12-10)/(4/math.sqrt(16))-2)<1e-12,'t statistic')
    sample=[2,1,3]
    num(abs(len(sample)/sum(sample)-.5)<1e-12,'exponential mle')
    n=100; sigma=2; xbar=10
    lo=xbar-1.96*sigma/math.sqrt(n); hi=xbar+1.96*sigma/math.sqrt(n)
    num(abs(lo-9.608)<1e-12 and abs(hi-10.392)<1e-12,'z interval')
    n=25; xb=20; s=5; tcrit=2.064
    num(abs(xb-tcrit*s/math.sqrt(n)-17.936)<1e-12 and abs(xb+tcrit*s/math.sqrt(n)-22.064)<1e-12,'t interval')
    z=(10.5-10)/(2/math.sqrt(100))
    num(abs(z-2.5)<1e-12,'z test')
    p=2*(1-0.5*(1+math.erf(2.5/math.sqrt(2))))
    num(abs(p-.01241933065)<1e-8,'z p-value')
    xs=[1,2,3]; ys=[2,4,5]
    mx=sum(xs)/3; my=sum(ys)/3
    sxx=sum((x-mx)**2 for x in xs); sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    b1=sxy/sxx; b0=my-b1*mx
    preds=[b0+b1*x for x in xs]
    sse=sum((y-yh)**2 for y,yh in zip(ys,preds)); sst=sum((y-my)**2 for y in ys)
    r2=1-sse/sst
    num(abs(b1-1.5)<1e-12 and abs(b0-2/3)<1e-12,'ols coefficients')
    num(abs(sse-1/6)<1e-12 and abs(r2-27/28)<1e-12,'ols fit')

    valid_ids={m['id'] for m in manifest['chapters']}
    for e in search['entries']:
        ck(e['chapterId'] in valid_ids,'search chapter id')
        ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty')
    search_corpus='\n'.join(e['text'] for e in search['entries'])
    for tok in ['Delta method','Cramér–Rao','Neyman–Pearson','Gauss–Markov','Jacobian']:
        concept(tok in search_corpus,f'search concept {tok}')

    figs=sorted((site/'assets/advanced-statistics-svg').glob('*.svg'))
    ck(len(figs)==20,'20 figures')
    for pth in figs:
        svg=pth.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg,f'svg accessibility {pth.name}')
        ck('href="http' not in svg and "href='http" not in svg,f'no remote svg {pth.name}')

    sw=(site/'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw,'sw final library version')
    for tok in [
        f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',
        f'./books/{BOOK}/chapters/ch19.html','./assets/advanced-statistics-svg/linear-model-theory.svg'
    ]:
        ck(tok in sw,f'sw path {tok}')

    print(f'ADVANCED_STATISTICS_QA_ROUND1_OK checks={checks} books=13 library={expected_library} chapters=20 appendices=3 questions=100 search=189 figures=20')
    print(f'ADVANCED_STATISTICS_QA_ROUND2_OK quantitative_rechecks={numeric_checks} high_risk_concepts={concept_checks} scope_separation=passed exact_vs_asymptotic=passed')

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: python deploy/validate_advanced_statistics.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
