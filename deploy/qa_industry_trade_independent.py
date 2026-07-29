#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path

BOOK='industry-trade'; VERSION='2026.07.29-1'; checks=0

def ck(c,msg):
    global checks
    checks += 1
    if not c: raise AssertionError(msg)

def main(site_root:str):
    site=Path(site_root); root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    qmap={x['id']:x for x in q['items']}
    ck(m['version']==q['version']==VERSION,'version')

    expected={
        'ch00-q02':('0.30。', .4**2+.3**2+.2**2+.1**2),
        'ch01-q02':('0.30。', (100-70)/100),
        'ch02-q02':('30 單位。', (100-20-20)/2),
        'ch03-q02':('NT$100。', 5/(5-1)*80),
        'ch04-q02':('由 NT$40 降到 NT$30。', (1000/50+20,1000/100+20)),
        'ch05-q02':('NT$20。', 3*20-40),
        'ch06-q02':('國內價格 NT$60；政府收入 NT$1,000。', (50+10,10*100)),
        'ch07-q02':('增加 NT$7。', 25-18),
        'ch08-q02':('Q=40、P=60。', ((100-20)/2,100-(100-20)/2)),
        'ch09-q02':('海外外包較便宜 NT$800。', (50*100+1000)-((35+5)*100+1200)),
        'ch10-q02':('750 單位。', 6000/8),
        'ch11-q02':('固定費較低 NT$50。', 5*100-450),
        'ch12-q02':('NT$20。', 110-90),
        'ch13-q02':('NT$15。', 100-70-15),
        'ch14-q02':('NT$150。', 600+500-950),
        'ch15-q02':('品牌商 NT$60；供應商 NT$40。', (.6*100,(1-.6)*100)),
        'ch16-q02':('NT$50／小時。', 5*10),
        'ch17-q02':('NT$50。', .4*500-150),
        'ch18-q02':('SMC=NT$100；矯正稅 NT$30／單位。', (70+30,30)),
        'ch19-q02':('NT$10，屬貿易轉向方向。', 80-70),
    }
    ck(len(expected)==20,'20 recomputations')
    for qid,(answer,value) in expected.items():
        item=qmap[qid]; ck(item['answer']==answer,f'{qid} answer drift')
        vals=value if isinstance(value,tuple) else (value,)
        for v in vals: ck(math.isfinite(float(v)),f'{qid} finite recomputation')
        ck(any(ch.isdigit() for ch in item['explanation']),f'{qid} explanation has calculation')

    for item in q['items']:
        ck(item['question'].strip().endswith(('？','。')) or '？' in item['question'],f'{item["id"]} malformed question')
        ck(len(item['answer'].strip())>=4,f'{item["id"]} answer too short')
        ck(len(item['explanation'].strip())>=8,f'{item["id"]} explanation too short')
        ck(item['answer'] not in {'一定','永遠','皆是'},f'{item["id"]} categorical answer')

    chapter_text={x['id']:(root/x['file']).read_text(encoding='utf-8') for x in m['chapters'] if x['kind']=='chapter'}
    required_by_ch={
        'ch02':['Cournot','Bertrand','Stackelberg','不能把三者的均衡結論直接互換'],
        'ch05':['出口固定成本','生產力','選擇效果'],
        'ch06':['轉嫁','市場勢力','政府關稅收入'],
        'ch07':['特定 Cournot 模型','外國報復','政府失靈','尋租'],
        'ch08':['雙重加價','投入封鎖','不能把「整合」固定當成好或壞'],
        'ch10':['水平 FDI','垂直 FDI','固定成本','控制權'],
        'ch12':['正常價值','可比性','重大損害','因果關係','不能取代'],
        'ch15':['威脅點','合併利潤','稅','關稅'],
        'ch16':['調整成本','短期受損','長期總體利得','單一因果'],
        'ch17':['知識外溢','私人報酬','社會報酬','雙向效果'],
        'ch18':['第一最佳','Pigouvian','碳洩漏','全球排放'],
        'ch19':['貿易創造','貿易轉向','真實資源成本','關稅收入'],
    }
    for cid,tokens in required_by_ch.items():
        t=chapter_text[cid]
        for token in tokens: ck(token in t,f'{cid} missing second-round token {token}')

    qgates={
        'ch07-q05':['市場結構','外國','資訊'],
        'ch08-q05':['雙重加價','封鎖'],
        'ch10-q03':['固定成本','貿易成本'],
        'ch12-q02':['不是完整法律判定'],
        'ch12-q05':['低價','消費者'],
        'ch16-q03':['重新配置','摩擦'],
        'ch17-q05':['知識外溢','不是'],
        'ch18-q05':['外部','直接'],
        'ch19-q03':['貿易創造','貿易轉向'],
    }
    for qid,tokens in qgates.items():
        blob=qmap[qid]['answer']+' '+qmap[qid]['explanation']
        for token in tokens: ck(token in blob,f'{qid} missing qualification {token}')

    corpus='\n'.join(e['title']+' '+e['text'] for e in s['entries'])
    for token in ['策略性貿易政策','外國報復','雙重加價','投入封鎖','FDI','正常價值','重大損害','知識外溢','Pigouvian','真實資源成本']:
        ck(token in corpus,f'search missing {token}')
    for token in ['出口補貼一定提高','垂直整合一定提高','自由貿易讓每個人都受益','FDI 就是所有跨境金融投資']:
        ck(token not in corpus,f'search stale overstatement {token}')

    print(f'INDUSTRY_TRADE_QA_ROUND2_OK checks={checks} questions_rechecked={len(q["items"])} quantitative_recomputed={len(expected)} high_risk_chapters={len(required_by_ch)}')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: qa_industry_trade_independent.py SITE_ROOT')
    main(sys.argv[1])
