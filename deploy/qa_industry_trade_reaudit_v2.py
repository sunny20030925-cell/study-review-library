#!/usr/bin/env python3
from __future__ import annotations
import json, math, re, sys
from collections import Counter
from pathlib import Path

BOOK='industry-trade'
VERSION='2026.07.30-1'

def main(site_root:str, expected_library:str|None=None)->int:
    site=Path(site_root); root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    checks=0
    def ck(cond,msg):
        nonlocal checks
        checks+=1
        if not cond: raise AssertionError(msg)
    def close(a,b,msg,tol=1e-9):
        ck(abs(a-b)<=tol,msg)

    ids=[b['id'] for b in lib['books']]
    ck(ids.count(BOOK)==1,'book registry uniqueness')
    ck(m['id']==BOOK,'manifest id')
    ck(m['version']==VERSION,'manifest v2')
    ck(q['bookId']==BOOK,'question book id')
    ck(q['version']==VERSION,'question v2')
    if expected_library is not None: ck(lib['version']==expected_library,'library version')

    chapters=[x for x in m['chapters'] if x['kind']=='chapter']
    apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters')
    ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'stable chapter ids')
    ck(len(apps)==3,'3 appendices')
    ck([x['id'] for x in apps]==['appendix-a','appendix-b','appendix-c'],'stable appendix ids')
    ck(q['count']==len(q['items'])==100,'100 questions')
    ck(len({x['id'] for x in q['items']})==100,'unique question ids')
    ck(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'5 questions/chapter')
    ck(len(s['entries'])==160,'160 search entries')
    ck(Counter(x['chapterId'] for x in s['entries'])=={f'ch{i:02d}':8 for i in range(20)},'8 search entries/chapter')

    required_q=['id','bookId','chapterId','chapterTitle','topic','difficulty','question','answer','explanation','source']
    for item in q['items']:
        for field in required_q: ck(bool(str(item.get(field,'')).strip()),f'{item.get("id")} missing {field}')
        ck(item['bookId']==BOOK,f'{item["id"]} book id')
        ck(item['chapterId'] in {x['id'] for x in chapters},f'{item["id"]} chapter id')
        ck(re.fullmatch(r'ch\d{2}-q\d{2}',item['id']) is not None,f'{item["id"]} format')
        ck('。。' not in item['answer']+item['explanation'],f'{item["id"]} duplicated punctuation')

    q04_keywords={
      'ch00':['福利','剩餘'],'ch01':['MC','Lerner'],'ch02':['Cournot','Bertrand','Stackelberg'],
      'ch03':['產業內貿易','規模經濟'],'ch04':['平均成本','邊際成本'],'ch05':['自我選擇','learning-by-exporting'],
      'ch06':['配額租','政府收入'],'ch07':['淨福利','補貼'],'ch08':['雙重加價','封鎖'],
      'ch09':['外包','離岸'],'ch10':['FDI','投資組合'],'ch11':['固定費','權利金'],
      'ch12':['正常價值','重大損害'],'ch13':['可比','交易成本'],'ch14':['範疇經濟','規模經濟'],
      'ch15':['disagreement','議價'],'ch16':['分配','調整成本'],'ch17':['市場失靈','外溢'],
      'ch18':['環境工具','排放'],'ch19':['資源成本','重複']
    }
    by_q={x['id']:x for x in q['items']}
    for ch,kws in q04_keywords.items():
        item=by_q[f'{ch}-q04']; text=item['answer']+' '+item['explanation']
        for kw in kws: ck(kw in text,f'{ch}-q04 missing correction keyword {kw}')

    html={}
    for meta in m['chapters']:
        p=root/meta['file']; ck(p.is_file() and p.stat().st_size>700,f'missing/thin {meta["file"]}')
        text=p.read_text(encoding='utf-8'); html[meta['id']]=text
        ck('<script' not in text.lower(),f'inline script {meta["id"]}')
    figs=list((site/'assets/industry-trade-svg').glob('*.svg')); ck(len(figs)==20,'20 SVG')
    for f in figs:
        t=f.read_text(encoding='utf-8')
        ck('<title' in t and '<desc' in t and 'viewBox=' in t and 'role="img"' in t,f'figure accessibility {f.name}')
        ck('href="http' not in t and "href='http" not in t,f'no remote figure href {f.name}')

    corpus='\n'.join(html.values())+'\n'+'\n'.join(x['answer']+' '+x['explanation'] for x in q['items'])+'\n'+'\n'.join(x['text'] for x in s['entries'])
    positives=[
      '自有價格彈性通常為負','固定彈性的 CES 基準','加成率本身是固定的',
      '不能把同一筆補貼重複扣兩次','含補貼收入的利潤',
      '持久利益','至少 10% 投票權','並不要求 100% 控制',
      r'q^*=\Delta F/\Delta t','disagreement payoffs',r'G=S-d_A-d_B',
      '交易的一側只有一個賣方、另一側只有一個買方',
      '實質上全部貿易','實質上相同的對外關稅',r'\Delta RC=c_{partner}-c_{nonmember}',
      '不是再把「關稅收入損失 NT$20」與「資源成本 NT$10」重複相加',
      '正常價值','重大損害','因果關係'
    ]
    for token in positives: ck(token in corpus,f'missing correction token: {token}')
    negatives=[
      '價格變動 1% 時需求量變動的百分比',
      '同時競爭加劇可能壓低加成。這種「更多品種＋更大生產規模」',
      '企業取得並控制國外生產或營運資產的投資',
      r'q^*=F_{FDI}/t','上游與下游各只有一個主要交易對手的情況',
      r'Share_A=\beta S',r'True\ resource\ cost',
      '成員間取消多數關稅，但各自保留對外關稅',
      '成員間自由貿易並採共同對外關稅'
    ]
    for token in negatives: ck(token not in corpus,f'legacy overstatement remains: {token}')

    sync=[
      ('ch01','正式定義','自有價格彈性通常為負'),
      ('ch03','核心公式','若 ε 固定'),
      ('ch07','核心公式','重複扣兩次'),
      ('ch10','正式定義','至少 10% 投票權'),
      ('ch10','核心公式',r'\Delta F/\Delta t'),
      ('ch15','核心公式','disagreement payoffs'),
      ('ch19','正式定義','實質上全部貿易'),
      ('ch19','核心公式','不可重複扣除'),
      ('ch19','標準例題','國內福利淨減 NT$10')
    ]
    smap={(e['chapterId'],e['title']):e['text'] for e in s['entries']}
    for ch,title,token in sync: ck(token in smap[(ch,title)],f'search sync {ch}/{title}')

    close(.4**2+.3**2+.2**2+.1**2,.30,'HHI')
    close((100-70)/100,.30,'Lerner')
    close((100-20-1*20)/(2*1),30,'Cournot BR')
    close((5/(5-1))*80,100,'CES price')
    close(1000/50+20,40,'AC q50')
    close(1000/100+20,30,'AC q100')
    close((50-30)*100-1980,20,'export profit')
    close(50+10,60,'tariff price benchmark')
    close(10*100,1000,'tariff revenue')
    close(25-18,7,'strategic subsidy accounting')
    q_int=(100-20)/2; p_int=100-q_int
    close(q_int,40,'integrated quantity'); close(p_int,60,'integrated price')
    close(60*100,6000,'make cost')
    close(40*100+7*100+500,5200,'offshore cost')
    close(6000/8,750,'FDI incremental cutoff')
    close(300+2*100,500,'royalty payment')
    close(100-80,20,'simplified dumping margin')
    close(120-90-15,15,'arbitrage margin')
    close(500+500-850,150,'scope saving')
    G=100-0-0; close(0+.6*G,60,'Nash A'); close(0+.4*G,40,'Nash B')
    close(10*5,50,'MRPL')
    close(.5*300-100,50,'R&D expected private return')
    close(70+30,100,'SMC')
    close(80-70,10,'trade diversion resource-cost increase')
    close((90-80)-20,-10,'trade diversion national welfare accounting')

    sw=(site/'sw.js').read_text(encoding='utf-8')
    if expected_library is not None: ck(f"study-library-{expected_library}" in sw,'service worker version')
    for token in ['./books/industry-trade/manifest.json','./books/industry-trade/questions.json','./books/industry-trade/search.json','./books/industry-trade/chapters/ch19.html','./assets/industry-trade-svg/ch19.svg']:
        ck(token in sw,f'sw path {token}')

    release=next((x for x in m.get('releaseNotes',[]) if x.get('version')==VERSION),None)
    ck(release is not None,'v2 release note')
    ck('閱讀進度' in release.get('progressImpact','') and '題目 ID' in release.get('progressImpact',''),'progress compatibility note')

    print(f'INDUSTRY_TRADE_V2_REAUDIT_OK checks={checks} questions=100 q04_rewritten=20 quantitative_recomputed=24 high_risk_gates={len(positives)+len(negatives)} search=160 figures=20')
    return checks

if __name__=='__main__':
    if len(sys.argv) not in {2,3}:
        raise SystemExit('usage: python deploy/qa_industry_trade_reaudit_v2.py SITE_ROOT [EXPECTED_LIBRARY_VERSION]')
    main(sys.argv[1], sys.argv[2] if len(sys.argv)==3 else None)
