#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from collections import Counter
from pathlib import Path
BOOK='industrial-economics'; VERSION='2026.07.29-1'

def main(site_root:str,expected_library:str)->int:
 site=Path(site_root); root=site/'books'/BOOK
 m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8')); lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); checks=0
 def ck(cond,msg):
  nonlocal checks; checks+=1
  if not cond: raise AssertionError(msg)
 ck(m['id']==BOOK,'manifest id'); ck(m['version']==VERSION,'manifest version'); ck(q['bookId']==BOOK,'question book id'); ck(q['version']==VERSION,'question version'); ck(lib['version']==expected_library,'library version')
 ids=[b['id'] for b in lib['books']]; ck(len(ids)>=13 and BOOK in ids,'industrial economics must remain in registry'); ck(ids.count(BOOK)==1,'single industrial economics registry entry')
 chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
 ck(len(chapters)==20,'chapter count'); ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'chapter ids'); ck(len(apps)==3,'appendix count'); ck([x['id'] for x in apps]==['appendix-a','appendix-b','appendix-c'],'appendix ids')
 ck(q['count']==len(q['items'])==100,'question count'); ck(len({x['id'] for x in q['items']})==100,'unique qids'); ck(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions per chapter'); ck(len(s['entries'])==150,'search count')
 cids={x['id'] for x in chapters}
 for item in q['items']:
  ck(item['bookId']==BOOK,f'question book {item["id"]}'); ck(item['chapterId'] in cids,f'question chapter {item["id"]}'); ck(bool(item['question'].strip()),f'question {item["id"]}'); ck(bool(item['answer'].strip()),f'answer {item["id"]}'); ck(bool(item['explanation'].strip()),f'explanation {item["id"]}'); ck(re.fullmatch(r'ch\d{2}-q\d{2}',item['id']) is not None,f'id format {item["id"]}')
 headings=['本章要解決的問題','白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']; html=[]; precise=[]
 for meta in m['chapters']:
  p=root/meta['file']; ck(p.is_file(),f'missing {meta["file"]}'); text=p.read_text(encoding='utf-8'); html.append(text); ck('<h1>' in text,f'h1 {meta["id"]}'); ck('href="http' not in text and "href='http" not in text,f'remote href {meta["id"]}')
  if meta['kind']=='chapter':
   precise.append(text)
   for h in headings: ck(h in text,f'{meta["id"]} heading {h}')
   ck('assets/industrial-economics-svg/' in text,f'figure ref {meta["id"]}')
 figs=sorted((site/'assets/industrial-economics-svg').glob('*.svg')); ck(len(figs)==20,'figure count')
 for p in figs:
  text=p.read_text(encoding='utf-8'); ck('<title' in text and '<desc' in text and 'viewBox=' in text,f'figure accessibility {p.name}'); ck('href="http' not in text and "href='http" not in text,f'figure remote {p.name}')
 corpus='\n'.join(html)+'\n'+'\n'.join(e['title']+' '+e['text'] for e in s['entries'])+'\n'+'\n'.join(x['question']+' '+x['answer']+' '+x['explanation'] for x in q['items'])
 for token in ['HHI','Lerner','MR=MC','Cournot','Bertrand','Stackelberg','價格歧視','雙重加價','折現因子','網路效果','反事實','相關不等於因果','市場界定']: ck(token in corpus,f'core concept {token}')
 ptxt='\n'.join(precise)
 for token in ['集中度仍只是篩檢訊號','價格歧視的福利效果不是固定方向','不能只背「兩家就 P=MC」，必須背假設','先行者優勢不是普世定律','自由進入的品種數不必等於社會最適','相似價格可能來自相同成本、公開資訊或競爭性反應','效率與排除效果需同時評估','HHI 與 Delta HHI 可作結構篩檢，但不能單獨取代','不代表市場一定「贏者全拿」','法律認定與經濟模型不能互相取代','不能自動告訴因果']: ck(token in ptxt,f'precision correction {token}')
 sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f'study-library-{expected_library}' in sw,'sw version')
 for token in ['./books/industrial-economics/manifest.json','./books/industrial-economics/questions.json','./books/industrial-economics/search.json','./books/industrial-economics/chapters/ch19.html','./assets/industrial-economics-svg/empirical-io.svg']: ck(token in sw,f'sw path {token}')
 print(f'INDUSTRIAL_ECONOMICS_QA1_OK checks={checks} books={len(ids)} library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20 precision_corrections=11'); return checks

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: validate_industrial_economics.py SITE_ROOT EXPECTED_LIBRARY')
 main(sys.argv[1],sys.argv[2])
