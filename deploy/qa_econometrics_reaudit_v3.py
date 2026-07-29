#!/usr/bin/env python3
from __future__ import annotations

import html,json,math,re,sys
from collections import Counter
from pathlib import Path
from econometrics_v3_corrections import VERSION

BOOK='econometrics'; EXPECTED_IDS=[f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)]

def visible(raw:str)->str: return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',raw))).strip()
def close(a:float,b:float,tol:float=1e-9)->bool: return abs(a-b)<=tol

def main(site_root:str,expected_library_version:str|None=None)->None:
    site=Path(site_root); root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8')); qtop=json.loads((root/'questions.json').read_text(encoding='utf-8')); search=json.loads((root/'search.json').read_text(encoding='utf-8')); library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    cmeta=[m for m in manifest['chapters'] if m['kind']=='chapter']; ameta=[m for m in manifest['chapters'] if m['kind']=='appendix']
    raw={m['id']:(root/m['file']).read_text(encoding='utf-8') for m in cmeta}; chapters={k:visible(v) for k,v in raw.items()}; apps={m['id']:visible((root/m['file']).read_text(encoding='utf-8')) for m in ameta}; questions=qtop['items']; qmap={q['id']:q for q in questions}; checks=0
    def C(cond,msg):
        nonlocal checks
        if not cond: raise AssertionError(msg)
        checks+=1

    C(manifest['id']==BOOK,'manifest id'); C(manifest['version']==VERSION,'manifest version'); C(qtop['bookId']==BOOK,'question book'); C(qtop['version']==VERSION,'question version')
    C([m['id'] for m in cmeta]==[f'ch{i:02d}' for i in range(20)],'chapter ids'); C([m['id'] for m in ameta]==['appendix-a','appendix-b','appendix-c'],'appendix ids')
    C(qtop['count']==len(questions)==100,'100 questions'); C([q['id'] for q in questions]==EXPECTED_IDS,'question ids/order'); C(Counter(q['chapterId'] for q in questions)=={f'ch{i:02d}':5 for i in range(20)},'five per chapter'); C(len(search['entries'])==189,'189 search'); C(len(list((site/'assets/econometrics-svg').glob('*.svg')))==20,'20 svgs')
    for q in questions:
        C(bool(q['question'].strip()),f'{q["id"]} question'); C(bool(q['answer'].strip()),f'{q["id"]} answer'); C(bool(q['explanation'].strip()),f'{q["id"]} explanation'); C(q['bookId']==BOOK,f'{q["id"]} book')
    ids=[b['id'] for b in library['books']]; C(ids.count(BOOK)==1,'one econometrics'); C('industrial-economics' in ids and ids.index(BOOK)<ids.index('industrial-economics'),'registry order'); C('industry-trade' not in ids or ids.index('industrial-economics')<ids.index('industry-trade'),'later order')
    if expected_library_version: C(library['version']==expected_library_version,'library version')
    C(f"study-library-{library['version']}" in (site/'sw.js').read_text(encoding='utf-8'),'sw version')

    for token in ('strict exogeneity','整段 X 歷史','time-varying confounder','不等於 X 自動外生'): C(token.casefold() in chapters['ch13'].casefold(),f'v2 panel {token}')
    for token in ('SATE','PATE','代表性抽樣','不能只靠 random assignment'): C(token.casefold() in chapters['ch15'].casefold(),f'v2 experiment {token}')
    C('strict exogeneity' in qmap['ch13-q04']['answer']+' '+qmap['ch13-q04']['explanation'],'q13 v2'); C('SATE' in qmap['ch15-q02']['answer']+' '+qmap['ch15-q02']['explanation'] and 'PATE' in qmap['ch15-q02']['answer']+' '+qmap['ch15-q02']['explanation'],'q15 v2')

    for token in ('Complier','LATE','Monotonicity','defiers','ATE','ATT'): C(token.casefold() in chapters['ch14'].casefold(),f'ch14 {token}')
    C(r'LATE=E[Y(1)-Y(0)\mid D(1)>D(0)]' in raw['ch14'],'LATE formula')
    q14=qmap['ch14-q05']['answer']+' '+qmap['ch14-q05']['explanation']
    for token in ('Compliers','LATE','monotonicity','ATE','ATT'): C(token.casefold() in q14.casefold(),f'q14 {token}')
    for token in ('compliers','LATE','ATT','TOT','assignment 作為實際 treatment 的工具'): C(token.casefold() in chapters['ch15'].casefold(),f'ch15 {token}')
    C('若要估接受處置者的局部效果' not in chapters['ch15'],'old noncompliance wording removed')
    q15=qmap['ch15-q04']['answer']+' '+qmap['ch15-q04']['explanation']
    for token in ('原始隨機 assignment','compliers','LATE'): C(token.casefold() in q15.casefold(),f'q15 {token}')
    for token in ('no anticipation','提前反應','pre-treatment','parallel trends'): C(token.casefold() in chapters['ch16'].casefold(),f'ch16 {token}')
    for token in ('local compliers','LATE','monotonicity','exclusion','cutoff'): C(token.casefold() in chapters['ch17'].casefold(),f'ch17 {token}')
    q17=qmap['ch17-q05']['answer']+' '+qmap['ch17-q05']['explanation']
    for token in ('local compliers','LATE','monotonicity','整體 ATE'): C(token.casefold() in q17.casefold(),f'q17 {token}')
    for token in ('validation RMSE','final test set','尚未打開','model selection','test 已參與 model selection'): C(token.casefold() in chapters['ch18'].casefold(),f'ch18 {token}')
    C('training RMSE=0.5、test RMSE=3' not in chapters['ch18'],'old test selection removed')
    q18=qmap['ch18-q03']['question']+' '+qmap['ch18-q03']['answer']+' '+qmap['ch18-q03']['explanation']
    for token in ('validation RMSE','第二個模型','untouched test set','不能用 test 一邊選模型'): C(token.casefold() in q18.casefold(),f'q18 {token}')
    for token in ('LATE／CACE','monotonicity','ATE／ATT','no anticipation','local complier LATE','Validation／cross-validation','Final test set'): C(token.casefold() in apps['appendix-b'].casefold(),f'appendix b {token}')
    for token in ('Sample Average Treatment Effect','Population Average Treatment Effect','Complier','Local Average Treatment Effect','No Anticipation','Validation Set'): C(token.casefold() in apps['appendix-c'].casefold(),f'appendix c {token}')

    corpus='\n'.join(chapters.values())+'\n'+'\n'.join(q['answer']+' '+q['explanation'] for q in questions)
    for bad in ('Wald ratio 一定等於全母體 ATE','assignment 作 IV 就等於所有實際接受 treatment 者的效果','parallel trends 成立就不需要考慮 anticipation','fuzzy RDD 一定識別整體 ATE','用 final test set 選完模型後仍可把同一 test 當完全未碰過的最終評估'): C(bad.casefold() not in corpus.casefold(),f'negative gate {bad}')

    numeric=[('ch01-q01',10/math.sqrt(100),1.0,'1。'),('ch01-q02',(1/math.sqrt(400))/(1/math.sqrt(100)),.5,'1/2'),('ch01-q03',2+3*4,14.,'14'),('ch02-q01',3/2,1.5,'1.5'),('ch02-q02',10/3-(3/2)*2,1/3,'1/3'),('ch02-q04',1-20/100,.8,'0.80'),('ch03-q01',4/20,.2,'0.20'),('ch03-q02',math.sqrt(4/20),math.sqrt(.2),'0.447'),('ch04-q02',1-(1-.40)*(99/96),.38125,'0.381'),('ch05-q01',5+3*.2,5.6,'5.6'),('ch06-q01',2.4/.6,4.,'4'),('ch06-q02',2.4-1.96*.6,1.224,'1.224'),('ch07-q04',(math.exp(.1823)-1)*100,19.9974132126,'20%'),('ch08-q01',1.2/.4,3.,'3'),('ch09-q01',1/(1-.8),5.,'5'),('ch09-q04',2*(4/(4+1)),1.6,'1.6'),('ch10-q02',.8*.5*.5,.2,'0.20'),('ch11-q01',100+2-1,101.,'101'),('ch11-q02',100*(math.log(105)-math.log(100)),4.87901641694,'4.879'),('ch12-q01',2+.8*10,10.,'10'),('ch12-q02',2/(1-.8),10.,'10'),('ch13-q01',2*(5-3),4.,'4'),('ch14-q01',6/2,3.,'3'),('ch15-q01',75-70,5.,'5'),('ch16-q01',(70-50)-(55-45),10.,'10'),('ch17-q01',68-62,6.,'6'),('ch18-q01',(1+2+3)/3,2.,'2'),('ch18-q02',math.sqrt((1+4+9)/3),2.16024689947,'2.160'),('ch19-q02',100*.04,4.,'4 個百分點')]
    for qid,calc,expected,token in numeric:
        C(qid in qmap,f'numeric q {qid}'); C(close(calc,expected,1e-8),f'numeric calc {qid}'); C(token in qmap[qid]['answer'],f'numeric answer {qid}')
    print(f'ECONOMETRICS_REAUDIT_V3_OK checks={checks} chapters=20 appendices=3 questions=100 search=189 figures=20 question_rechecks=100 numeric_rechecks={len(numeric)} correction_areas=5 question_adjustments=4 ids_preserved=true')

if __name__=='__main__':
    if len(sys.argv) not in (2,3): raise SystemExit('usage: python deploy/qa_econometrics_reaudit_v3.py SITE_ROOT [EXPECTED_LIBRARY_VERSION]')
    main(sys.argv[1],sys.argv[2] if len(sys.argv)==3 else None)
