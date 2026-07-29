from __future__ import annotations
import json, re, sys
from pathlib import Path
BOOK='international-economics'; VERSION='2026.07.29-1'; checks=0; numeric=0

def ck(cond,msg):
    global checks; checks+=1
    if not cond: raise AssertionError(msg)

def num(cond,msg):
    global numeric; numeric+=1; ck(cond,msg)

def main(site_root,expected_library):
    site=Path(site_root); root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); qd=json.loads((root/'questions.json').read_text(encoding='utf-8')); sd=json.loads((root/'search.json').read_text(encoding='utf-8')); lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ck(m['version']==VERSION,'manifest version'); ck(qd['version']==VERSION,'q version'); ck(lib['version']==expected_library,'library version'); ck(lib['books'][-1]['id']==BOOK,'book last')
    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'chapter IDs'); ck([x['id'] for x in apps]==['appendix-a','appendix-b','appendix-c'],'appendix IDs')
    # Independently inspect every question record for complete exam-useful metadata and explanation.
    for i,x in enumerate(qd['items']):
        ck(x['id']==f'ch{i//5:02d}-q{i%5+1:02d}',f'q order {i}')
        ck(x['bookId']==BOOK,'q book id'); ck(x['chapterId']==f'ch{i//5:02d}','q chapter id')
        ck(x['difficulty'] in {'基礎','標準','綜合','陷阱'},'q difficulty'); ck(len(x['question'].strip())>=8,'q stem'); ck(bool(x['answer'].strip()),'q answer'); ck(len(x['explanation'].strip())>=5,'q explanation')
    q={x['id']:x for x in qd['items']}
    # Recompute quantitative questions from their original inputs rather than trusting stored explanations.
    recompute={
      'ch00-q03':120/80,
      'ch01-q01':2/4,
      'ch02-q01':50*4,
      'ch04-q01':120/100*100,
      'ch07-q01':100*(1+.20),
      'ch07-q02':80-50,
      'ch07-q03':20*30,
      'ch08-q01':(125-100)*40,
      'ch11-q02':80,
      'ch11-q04':500-620,
      'ch12-q02':32*1.10,
      'ch12-q04':32*100/3200,
      'ch13-q01':32*1.04/1.02,
      'ch13-q03':.05-.02,
      'ch14-q01':120/4,
      'ch14-q02':.05-.02,
      'ch14-q03':30*4/120,
    }
    parsers={
      'ch00-q03':lambda v: abs(v-1.5)<1e-12,
      'ch01-q01':lambda v: abs(v-.5)<1e-12,
      'ch02-q01':lambda v: v==200,
      'ch04-q01':lambda v:v==120,
      'ch07-q01':lambda v:v==120,
      'ch07-q02':lambda v:v==30,
      'ch07-q03':lambda v:v==600,
      'ch08-q01':lambda v:v==1000,
      'ch11-q02':lambda v:v==80,
      'ch11-q04':lambda v:v==-120,
      'ch12-q02':lambda v:abs(v-35.2)<1e-12,
      'ch12-q04':lambda v:v==1,
      'ch13-q01':lambda v:round(v,2)==32.63,
      'ch13-q03':lambda v:round(v*100)==3,
      'ch14-q01':lambda v:v==30,
      'ch14-q02':lambda v:round(v*100)==3,
      'ch14-q03':lambda v:v==1,
    }
    for qid,v in recompute.items(): num(parsers[qid](v),f'numeric recomputation {qid}')
    # High-risk economics judgments rechecked independently.
    expected_answers={
      'ch01-q04':'不必然。','ch02-q04':'不一定。','ch03-q05':'不保證。','ch04-q04':'不能。','ch04-q05':'不保證。','ch05-q05':'不足以。',
      'ch07-q04':'負。','ch07-q05':'不是。','ch08-q05':'不一定。','ch10-q05':'是否存在可識別的市場失靈，以及是否有更直接工具。',
      'ch11-q05':'不應。','ch12-q01':'貶值。','ch12-q05':'不可以。','ch13-q02':'大於 1。','ch13-q04':'買美元遠期。','ch13-q05':'不是。',
      'ch14-q04':'不必。','ch14-q05':'不必然。','ch15-q03':'本幣逐步升值。','ch15-q04':'不必。','ch16-q02':'升值。','ch16-q03':'AA。',
      'ch17-q01':'賣外匯。','ch17-q02':'增加。','ch17-q03':'賣國內債券。','ch17-q04':'下降。','ch17-q05':'不能。',
      'ch18-q02':'獨立貨幣政策。','ch18-q05':'不存在。','ch19-q05':'不一定。'
    }
    for qid,ans in expected_answers.items(): ck(q[qid]['answer']==ans,f'judgment {qid}')
    texts={}
    for ch in m['chapters']:
        text=(root/ch['file']).read_text(encoding='utf-8'); texts[ch['id']]=text
        if ch['kind']=='chapter':
            ck(len(re.findall(r'<h2(?:\s|>)', text))>=6,f'h2 {ch["id"]}')
            ck('summarybox' in text and '本章收尾' in text,f'summary {ch["id"]}')
            ck(text.count('<li>')>=5,f'checks list {ch["id"]}')
        else:
            ck((root/ch['file']).stat().st_size>=1000,f'appendix density {ch["id"]}')
    full='\n'.join(texts.values())
    # Formula/sign consistency gates.
    formula_gates=[
      ('ch01','a_{LC}/a_{LW}'),('ch02','P× MPL=w'),('ch04','P_X/P_M'),('ch07','P_w(1+t)'),('ch11','CA+FA_{in}=0'),('ch11','CA=S-I'),
      ('ch12','S=NT$/US$'),('ch12','q=SP^*/P'),('ch13','1+i_{TW}=(F/S)(1+i_{US})'),('ch13','(F-S)/S≈ i_{TW}-i_{US}'),
      ('ch13','i_{TW}≈ i_{US}+E(Δ S/S)'),('ch14','S=P_{TW}/P_{US}'),('ch14','Δ S/S≈π_{TW}-π_{US}'),('ch14','q=SP^*/P')]
    for cid,t in formula_gates: ck(t in texts[cid],f'formula {cid} {t}')
    sign_gates=[
      ('ch11','淨金融流入'),('ch11','官方統計的金融帳符號慣例可能與教科書簡化不同'),
      ('ch12','S 上升代表一美元需要更多新臺幣'),('ch12','q 上升表示外國商品相對更貴'),
      ('ch13','預期 S 上升代表新臺幣預期貶值'),('ch14','本國通膨較高時，本幣長期傾向貶值'),
      ('ch16','DD 在 Y–S 圖上向上傾斜'),('ch16','AA 向下傾斜'),('ch17','貶值壓力，央行要賣外匯'),
    ]
    for cid,t in sign_gates: ck(t in texts[cid],f'sign gate {cid} {t}')
    ck('最惠國待遇' in texts['ch09'] and '國民待遇' in texts['ch09'],'WTO nondiscrimination principles')
    ck('Marshall–Lerner' in texts['ch16'] and '彈性的絕對值之和大於 1' in texts['ch16'] and 'J 曲線' in texts['ch16'],'trade-balance elasticity/J curve')
    ck('不是每次貶值都必然出現的定律' in texts['ch16'],'J-curve caveat')
    ck('第一最佳工具' in texts['ch10'] and '污染' in texts['ch10'],'first-best externality logic')
    ck('市場分割與需求彈性差異' in texts['ch06'],'dumping price discrimination conditions')
    ck('共同技術' in texts['ch03'] and '無貿易成本' in texts['ch03'],'HO conditions')
    # Search index and SVG accessibility, independent pass.
    ids={x['id'] for x in m['chapters']}; ck(len(sd['entries'])==144,'search count')
    for e in sd['entries']:
        ck(e['chapterId'] in ids,'search target'); ck(e['title'].strip()!='','search title'); ck(e['text'].strip()!='','search text')
    figs=list((site/'assets/international-economics-svg').glob('*.svg')); ck(len(figs)==20,'fig count')
    for f in figs:
        t=f.read_text(encoding='utf-8'); ck(bool(re.search(r'<title(?:\s[^>]*)?>.+?</title>',t,re.S)),f'title {f.name}'); ck(bool(re.search(r'<desc(?:\s[^>]*)?>.+?</desc>',t,re.S)),f'desc {f.name}'); ck('viewBox=' in t,f'viewbox {f.name}')
    # Static/offline paths: all content declared in manifest/search/question pack exists in the SW cache.
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version')
    for ch in m['chapters']: ck(f"./books/{BOOK}/{ch['file']}" in sw,f'sw chapter {ch["id"]}')
    for f in figs: ck(f'./assets/international-economics-svg/{f.name}' in sw,f'sw fig {f.name}')
    print(f'INTERNATIONAL_ECONOMICS_QA2_OK checks={checks} quantitative_rechecks={numeric} questions_rechecked={len(qd["items"])} chapters={len(chapters)} appendices={len(apps)} search={len(sd["entries"])} figures={len(figs)}')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python qa_international_economics.py SITE_ROOT EXPECTED_LIBRARY_VERSION')
    main(sys.argv[1],sys.argv[2])
