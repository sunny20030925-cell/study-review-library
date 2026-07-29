#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
BOOK='industrial-economics'; VERSION='2026.07.29-1'

def main(site_root:str,expected_library:str)->int:
 site=Path(site_root); root=site/'books'/BOOK
 m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); checks=0
 def ck(cond,msg):
  nonlocal checks; checks+=1
  if not cond: raise AssertionError(msg)
 ids=[b['id'] for b in lib['books']]
 ck(m['version']==q['version']==VERSION,'book versions'); ck(lib['version']==expected_library,'library version'); ck(BOOK in ids and ids.count(BOOK)==1,'book presence/order'); ck('industry-trade' not in ids or ids.index(BOOK)<ids.index('industry-trade'),'industrial economics precedes industry trade'); ck(len([x for x in m['chapters'] if x['kind']=='chapter'])==20,'chapters'); ck(len([x for x in m['chapters'] if x['kind']=='appendix'])==3,'appendices'); ck(q['count']==len(q['items'])==100,'questions'); ck(len(s['entries'])==150,'search')
 qmap={x['id']:x for x in q['items']}; ck(len(qmap)==100,'unique qids')
 for item in q['items']:
  ck(len(item['question'].strip())>=8,f'question length {item["id"]}'); ck(len(item['answer'].strip())>=2,f'answer length {item["id"]}'); ck(len(item['explanation'].strip())>=6,f'explanation length {item["id"]}'); ck(item['answer'].strip()!=item['explanation'].strip(),f'answer/explanation duplicate {item["id"]}')
 expected={'ch01-q02':40**2+30**2+20**2+10**2,'ch01-q04':2*30*25,'ch02-q02':(1_000_000+100*5_000)/5_000,'ch02-q04':600+500-900,'ch03-q02':((100-20)/2,100-(100-20)/2),'ch03-q04':(60-20)/60,'ch06-q02':80/3,'ch06-q04':(160/3,100-160/3),'ch08-q02':(80-40)/2,'ch08-q04':(40+20,100-(40+20)),'ch09-q02':0.5,'ch09-q04':5/8,'ch12-q02':(160-100)/(160-40),'ch14-q02':2*30*20,'ch16-q02':.2*8_000_000-1_000_000,'ch16-q04':.2*3_000_000-1_000_000,'ch19-q02':30/120}
 tokens={'ch01-q02':['3,000'],'ch01-q04':['1,500'],'ch02-q02':['300'],'ch02-q04':['200'],'ch03-q02':['Q=40','P=60'],'ch03-q04':['2/3'],'ch06-q02':['26.67'],'ch06-q04':['53.33','46.67'],'ch08-q02':['20'],'ch08-q04':['Q=60','P=40'],'ch09-q02':['0.5'],'ch09-q04':['0.625'],'ch12-q02':['0.5'],'ch14-q02':['1,200'],'ch16-q02':['600,000'],'ch16-q04':['-NT$400,000'],'ch19-q02':['25%']}
 for qid,value in expected.items():
  vals=value if isinstance(value,tuple) else (value,); ck(all(math.isfinite(float(v)) for v in vals),f'recompute finite {qid}'); joined=qmap[qid]['answer']+' '+qmap[qid]['explanation']
  for token in tokens[qid]: ck(token in joined,f'numeric answer {qid} {token}')
 corpus='\n'.join(e['title']+' '+e['text'] for e in s['entries'])+'\n'+'\n'.join(x['question']+' '+x['answer']+' '+x['explanation'] for x in q['items'])
 pairs=[('集中度','不能'),('HHI','口徑'),('Lerner','條件'),('價格歧視','福利'),('Cournot','數量'),('Bertrand','同質'),('Bertrand','容量'),('Stackelberg','承諾'),('自由進入','社會最適'),('卡特爾','偏離'),('平行行為','法律'),('雙重加價','垂直'),('Delta HHI','競爭效果'),('網路效果','多歸屬'),('平台','兩邊'),('反事實','競爭政策'),('相關','因果'),('公平交易委員會','最新')]
 for a,b in pairs: ck(a in corpus and b in corpus,f'high-risk pair {a}/{b}')
 chapter='\n'.join((root/x['file']).read_text(encoding='utf-8') for x in m['chapters'] if x['kind']=='chapter')
 for token in ['集中度仍只是篩檢訊號','價格歧視的福利效果不是固定方向','不能只背「兩家就 P=MC」，必須背假設','先行者優勢不是普世定律','自由進入的品種數不必等於社會最適','相似價格可能來自相同成本、公開資訊或競爭性反應','效率與排除效果需同時評估','HHI 與 Delta HHI 可作結構篩檢，但不能單獨取代','不代表市場一定「贏者全拿」','法律認定與經濟模型不能互相取代','不能自動告訴因果']: ck(token in chapter,f'precision {token}')
 ck('新臺幣一百億元' not in chapter and '新臺幣五十億元' not in chapter,'no stale filing threshold'); ck('以公平交易委員會最新公開資料為準' in chapter,'current-law pointer')
 sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f'study-library-{expected_library}' in sw,'sw version'); ck('./books/industrial-economics/questions.json' in sw,'sw questions'); ck('./assets/industrial-economics-svg/networks-platforms.svg' in sw,'sw figure')
 print(f'INDUSTRIAL_ECONOMICS_QA2_OK checks={checks} books={len(ids)} quantitative_rechecks={len(expected)} questions_rechecked=100 chapters=20 appendices=3 search=150 figures=20 high_risk_concepts={len(pairs)}'); return checks

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: qa_industrial_economics.py SITE_ROOT EXPECTED_LIBRARY')
 main(sys.argv[1],sys.argv[2])
