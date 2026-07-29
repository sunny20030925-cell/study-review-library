from __future__ import annotations
import json, os, re, sys
from collections import Counter
from pathlib import Path

BOOK='international-economics'; VERSION='2026.07.29-1'
REQUIRED_PRE_IDS={'calculus','accounting','economics','statistics','commercial-law','cost-accounting','microeconomics','intermediate-accounting','macroeconomics'}
checks=0

def ck(cond,msg):
    global checks; checks+=1
    if not cond: raise AssertionError(msg)

def main(arg):
    site=Path(arg)
    expected=os.environ.get('EXPECTED_LIBRARY_VERSION'); pre_path=os.environ.get('PRE_LIBRARY_JSON')
    if not expected or not pre_path: raise SystemExit('EXPECTED_LIBRARY_VERSION and PRE_LIBRARY_JSON are required')
    pre=json.loads(Path(pre_path).read_text(encoding='utf-8')); lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    pre_ids=[b['id'] for b in pre['books']]; post_ids=[b['id'] for b in lib['books']]
    ck(REQUIRED_PRE_IDS.issubset(pre_ids),f'missing prerequisite books: {pre_ids}')
    ck(BOOK not in pre_ids,'book existed before generation'); ck(post_ids==pre_ids+[BOOK],f'book order drift {post_ids}')
    ck(lib['version']==expected,'library version')
    for bid in pre_ids:
        r=site/'books'/bid
        m=json.loads((r/'manifest.json').read_text(encoding='utf-8')); q=json.loads((r/'questions.json').read_text(encoding='utf-8')); s=json.loads((r/'search.json').read_text(encoding='utf-8'))
        ck(m['id']==bid,f'existing manifest {bid}'); ck(q['count']==len(q['items'])>0,f'existing questions {bid}'); ck(bool(s['entries']),f'existing search {bid}')
    r=site/'books'/BOOK
    m=json.loads((r/'manifest.json').read_text(encoding='utf-8')); q=json.loads((r/'questions.json').read_text(encoding='utf-8')); s=json.loads((r/'search.json').read_text(encoding='utf-8'))
    ck(m['id']==BOOK,'manifest id'); ck(m['version']==q['version']==VERSION,'book version')
    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'chapter count'); ck(len(apps)==3,'appendix count'); ck(q['count']==100==len(q['items']),'question count')
    ck(Counter(x['chapterId'] for x in q['items'])=={f'ch{i:02d}':5 for i in range(20)},'five questions/chapter'); ck(len({x['id'] for x in q['items']})==100,'unique q ids')
    ck(len(s['entries'])==144,'search count')
    qmap={x['id']:x for x in q['items']}
    expected_answers={
      'ch00-q03':'1.5。','ch01-q01':'0.5 單位小麥。','ch02-q01':'NT$200。','ch04-q01':'120。',
      'ch07-q01':'NT$120。','ch07-q02':'30。','ch07-q03':'NT$600。','ch08-q01':'NT$1,000。',
      'ch11-q02':'80。','ch11-q04':'-120。','ch12-q02':'35.2。','ch12-q04':'1。',
      'ch13-q01':'約 32.63 NT$/US$。','ch13-q03':'約 3%。','ch14-q01':'30 NT$/US$。','ch14-q02':'約 3%。','ch14-q03':'1。'
    }
    for qid,ans in expected_answers.items(): ck(qmap[qid]['answer']==ans,f'{qid} answer {qmap[qid]["answer"]!r}')
    full=[]
    for ch in m['chapters']:
        p=r/ch['file']; ck(p.is_file() and p.stat().st_size>1000,f'chapter file {ch["id"]}')
        text=p.read_text(encoding='utf-8'); full.append(text)
        ck('\f' not in text and '\t' not in text,f'control chars {ch["id"]}'); ck('<script' not in text.lower(),f'inline script {ch["id"]}')
        if ch['kind']=='chapter': ck('本章理解檢查' in text,f'practice {ch["id"]}')
    full='\n'.join(full)
    core=['比較利益','Ricardo','特定要素','Heckscher–Ohlin','Stolper–Samuelson','Rybczynski','貿易條件','規模經濟','產業內貿易','傾銷','水平 FDI','全球價值鏈','關稅','配額租','出口補貼','最惠國待遇','國民待遇','WTO','貿易創造','貿易轉向','市場失靈','國際收支','國際投資部位','FA_{in}','CA=S-I','S=NT$/US$','q=SP^*/P','拋補利率平價','未拋補利率平價','購買力平價','匯率超調','DD–AA','Marshall–Lerner','J 曲線','沖銷','不可能三角','最適通貨區','sudden stop','貨幣錯配','期限錯配']
    for t in core: ck(t in full,f'missing core token {t}')
    forbidden=['自由貿易保證每個人受益','關稅一定提高福利','金融帳正號只有一種','PPP 每天必須成立','固定匯率可同時完全保有資本自由與獨立貨幣政策','所有金融危機只要流動性']
    for t in forbidden: ck(t not in full,f'forbidden overclaim {t}')
    ck('淨金融流入' in full and '官方統計' in full,'BOP sign caveat')
    ck('S 上升代表' in full and '新臺幣貶值' in full,'FX sign convention')
    ck('1+i_{TW}=(F/S)(1+i_{US})' in full,'CIP exact formula')
    ck('i_{TW}≈ i_{US}+E(Δ S/S)' in full,'UIP approx formula')
    ck('Δ S/S≈π_{TW}-π_{US}' in full,'relative PPP formula')
    ck('q=SP^*/P' in full and '實質貶值' in full,'real exchange rate convention')
    figures=sorted((site/'assets/international-economics-svg').glob('*.svg')); ck(len(figures)==20,'figure count')
    for f in figures:
        svg=f.read_text(encoding='utf-8'); ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg,f'svg accessibility {f.name}'); ck('href="http' not in svg and "href='http" not in svg,f'no remote svg {f.name}')
    ids={x['id'] for x in m['chapters']}
    for e in s['entries']:
        ck(e['chapterId'] in ids,'search chapter id'); ck(bool(e['title'].strip()) and bool(e['text'].strip()),'search nonempty'); ck(isinstance(e['page'],int) and e['page']>=0,'search page')
    sw=(site/'sw.js').read_text(encoding='utf-8')
    for t in [f"study-library-{expected}",'./books/international-economics/manifest.json','./books/international-economics/questions.json','./books/international-economics/search.json','./books/international-economics/chapters/ch19.html','./books/international-economics/chapters/appendix-c.html']:
        ck(t in sw,f'sw cache {t}')
    for f in figures: ck(f'./assets/international-economics-svg/{f.name}' in sw,f'sw figure {f.name}')
    print(f'INTERNATIONAL_ECONOMICS_QA1_OK checks={checks} books={len(post_ids)} library={expected} chapters=20 appendices=3 questions=100 search=144 figures=20 numeric_rechecks={len(expected_answers)}')
if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python validate_international_economics.py SITE_ROOT')
    main(sys.argv[1])
