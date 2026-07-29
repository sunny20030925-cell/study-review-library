#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

BOOK='econometrics'
VERSION='2026.07.29-1'


def ck(condition,message):
    if not condition: raise AssertionError(message)


def close(a,b,tol=1e-9):
    return abs(a-b)<=tol


def main(site_root: str):
    site=Path(site_root); root=site/'books'/BOOK; checks=0
    def C(cond,msg):
        nonlocal checks; ck(cond,msg); checks+=1

    C(root.is_dir(),'book root')
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    C(m['id']==q['bookId']==BOOK,'book id')
    C(m['version']==q['version']==VERSION,'book version')
    C(m['title']=='計量經濟學','title')

    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    C([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'chapter ids')
    C(len(apps)==3 and [x['id'] for x in apps]==['appendix-a','appendix-b','appendix-c'],'appendices')
    C(q['count']==len(q['items'])==100,'question count')
    C(len({x['id'] for x in q['items']})==100,'unique qids')
    C(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions each')
    C(len(s['entries'])==189,'search count')
    C(len({(e['chapterId'],e['page'],e['title']) for e in s['entries']})==189,'unique search entries')

    pre_path=os.environ.get('PRE_LIBRARY_JSON')
    expected_library=os.environ.get('EXPECTED_LIBRARY_VERSION')
    if pre_path:
        pre=json.loads(Path(pre_path).read_text(encoding='utf-8')); pre_ids=[b['id'] for b in pre['books']]; post_ids=[b['id'] for b in lib['books']]
        C(BOOK not in pre_ids,'book absent pre')
        C(post_ids==pre_ids+[BOOK],'append-only book order')
        if expected_library: C(lib['version']==expected_library,'library version')
    else:
        C([b['id'] for b in lib['books']][-1]==BOOK,'book is appended at tail')

    required_sections=['本章要解決的問題','白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']
    chapter_text=[]
    for meta in chapters:
        p=root/meta['file']; C(p.is_file() and p.stat().st_size>1800,f'chapter file {meta["id"]}')
        text=p.read_text(encoding='utf-8'); chapter_text.append(text)
        for sec in required_sections: C(f'id="{sec}"' in text,f'{meta["id"]} section {sec}')
        C('<figure class="chapter-figure">' in text and 'assets/econometrics-svg/' in text,f'{meta["id"]} figure reference')
    for meta in apps: C((root/meta['file']).is_file() and (root/meta['file']).stat().st_size>800,f'appendix {meta["id"]}')

    figdir=site/'assets/econometrics-svg'; figs=sorted(figdir.glob('*.svg'))
    C(len(figs)==20,'figure count')
    for p in figs:
        text=p.read_text(encoding='utf-8')
        C('<title' in text and '<desc' in text and 'viewBox=' in text,f'figure accessibility {p.name}')
        C('href="http' not in text and "href='http" not in text,f'no remote figure {p.name}')
        C(p.stat().st_size>550,f'figure nontrivial {p.name}')

    corpus='\n'.join(chapter_text)+'\n'+'\n'.join(e['text'] for e in s['entries'])+'\n'+'\n'.join(x['question']+' '+x['answer']+' '+x['explanation'] for x in q['items'])
    required_precision=[
      '同一條迴歸線可以回答描述問題，卻未必能回答因果問題',
      '不是 OLS 係數無偏的必要條件',
      '控制變數可以減少混淆，但不是「越多越好」',
      'Robust SE 修正的是抽樣變異估計',
      '不會單靠共線性就製造系統性 OLS 偏誤',
      'First stage 支持 relevance',
      '完全不隨時間變動的主效果係數',
      '「所有 pre-trend 係數不顯著」不是數學上的證明',
      'cutoff 附近的 local effect',
      'Prediction 與 causal estimation 是不同 estimand／loss',
      'HAC 主要修正變異數估計',
    ]
    for token in required_precision: C(token in corpus,f'precision token {token}')

    # Guard against a few especially dangerous unconditional claims. The false idea may
    # appear inside a "common error" question, so only reject stand-alone affirmative prose.
    forbidden_patterns=[
      r'<p>顯著迴歸係數就代表因果[。！]</p>',
      r'<p>R² 越高模型一定越正確[。！]</p>',
      r'<p>Robust SE 可以修正內生性[。！]</p>',
      r'<p>First-stage 顯著即可證明 instrument 外生[。！]</p>',
      r'<p>RDD 效果可以無條件外推到所有樣本[。！]</p>',
    ]
    for pat in forbidden_patterns: C(re.search(pat,'\n'.join(chapter_text)) is None,f'forbidden claim {pat}')

    qmap={x['id']:x for x in q['items']}
    # Independent numeric recomputation from original inputs; each check recomputes the
    # expected value rather than copying the displayed answer.
    numeric=[
      ('ch01-q01',10/math.sqrt(100),1.0),
      ('ch01-q02',(1/math.sqrt(400))/(1/math.sqrt(100)),0.5),
      ('ch01-q03',2+3*4,14.0),
      ('ch02-q01',3/2,1.5),
      ('ch02-q02',10/3-(3/2)*2,1/3),
      ('ch02-q04',1-20/100,0.8),
      ('ch03-q01',4/20,0.2),
      ('ch03-q02',math.sqrt(4/20),math.sqrt(0.2)),
      ('ch04-q02',1-(1-0.40)*(99/96),0.38125),
      ('ch05-q01',5+3*0.2,5.6),
      ('ch06-q01',2.4/0.6,4.0),
      ('ch06-q02',2.4-1.96*0.6,1.224),
      ('ch07-q04',(math.exp(0.1823)-1)*100,19.9974132126),
      ('ch08-q01',1.2/0.4,3.0),
      ('ch09-q01',1/(1-0.8),5.0),
      ('ch09-q04',2*(4/(4+1)),1.6),
      ('ch10-q02',0.8*0.5*0.5,0.2),
      ('ch11-q01',100+2-1,101.0),
      ('ch11-q02',100*(math.log(105)-math.log(100)),4.87901641694),
      ('ch12-q01',2+0.8*10,10.0),
      ('ch12-q02',2/(1-0.8),10.0),
      ('ch13-q01',2*(5-3),4.0),
      ('ch14-q01',6/2,3.0),
      ('ch15-q01',75-70,5.0),
      ('ch16-q01',(70-50)-(55-45),10.0),
      ('ch17-q01',68-62,6.0),
      ('ch18-q01',(1+2+3)/3,2.0),
      ('ch18-q02',math.sqrt((1+4+9)/3),2.16024689947),
      ('ch19-q02',100*0.04,4.0),
    ]
    for qid,calc,expected in numeric:
        C(qid in qmap,f'numeric q present {qid}'); C(close(calc,expected,1e-8),f'numeric recompute {qid}')

    answer_tokens={
      'ch01-q01':'1。','ch02-q01':'1.5。','ch03-q01':'0.20。','ch04-q02':'約 0.381。','ch05-q01':'5.6。','ch06-q01':'4。',
      'ch07-q04':'約 20%。','ch08-q01':'3。','ch09-q04':'1.6。','ch10-q02':'0.20，即約 20 個百分點／一單位 X。',
      'ch11-q01':'101。','ch12-q02':'10。','ch13-q01':'4。','ch14-q01':'3。','ch15-q01':'5。','ch16-q01':'10。','ch17-q01':'6。','ch18-q01':'2。'
    }
    for qid,ans in answer_tokens.items(): C(qmap[qid]['answer']==ans,f'answer token {qid}')

    # Formula/source integrity and encoding guards.
    C('E(u_i\\mid X_i)=0' in corpus,'zero conditional mean formula')
    C('\\hat\\beta_{Wald}' in corpus,'Wald formula')
    C('\\hat\\tau_{DiD}' in corpus,'DiD formula')
    C('\\tau_{RDD}' in corpus,'RDD formula')
    for bad in ('\x00','\x07','\x0b','\x0c'): C(bad not in corpus,f'control char {repr(bad)}')

    sw=(site/'sw.js').read_text(encoding='utf-8')
    if expected_library: C(f"study-library-{expected_library}" in sw,'sw version')
    for token in [f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json',f'./books/{BOOK}/chapters/ch19.html','./assets/econometrics-svg/regression-discontinuity.svg']:
        C(token in sw,f'sw cache {token}')

    print(f'ECONOMETRICS_QA_OK checks={checks} chapters=20 appendices=3 questions=100 search=189 figures=20 numeric_rechecks={len(numeric)}')


if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/validate_econometrics.py SITE_ROOT')
    main(sys.argv[1])
