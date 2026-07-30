#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='game-theory'; VERSION='2026.07.30-2'; ASSET='assets/game-theory-svg/game-map.svg'; MARKER='data-vp-asset="game-theory-information-equilibrium-map"'; CANVA='DAHQ3QeJvMk'

def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'game-theory once')
    ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==23,'20 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==23,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(20)),'ch00-ch19'); ck(all(x in chapter_ids for x in ('appendix-a','appendix-b','appendix-c')),'appendices')
    ck(q.get('bookId')==BOOK,'question book'); ck(q.get('version')==VERSION,'question version'); ck(q.get('count')==100,'question declared count'); ck(len(q.get('items',[]))==100,'100 questions')
    qids=[x.get('id') for x in q['items']]; ck(len(qids)==len(set(qids)),'unique question ids')
    for i in range(20): ck(sum(1 for x in qids if x.startswith(f'ch{i:02d}-q'))==5,f'ch{i:02d} five questions')
    ck(len(s.get('entries',[]))==189,'189 search entries')
    svgs=sorted((site/'assets/game-theory-svg').glob('*.svg')); ck(len(svgs)==20,'20 SVGs'); ck((site/ASSET).exists(),'VP SVG exists')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','VP status'); ck(vp.get('asset')==ASSET,'VP asset'); ck(vp.get('placement')=='ch00 and appendix-b','VP placement'); ck(vp.get('canvaDesignId')==CANVA,'Canva id'); ck(vp.get('canvaEditUrl')=='https://www.canva.com/d/qZaqmF_yGFYibV5','Canva URL'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoomable'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'offline cached')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker once'); ck(ap.count(MARKER)==1,'appendix marker once'); ck(f'href="{ASSET}"' in ch0,'ch00 zoom href'); ck(f'href="{ASSET}"' in ap,'appendix zoom href'); ck(f'src="{ASSET}"' in ch0,'ch00 src'); ck(f'src="{ASSET}"' in ap,'appendix src'); ck('target="_blank"' in ch0 and 'rel="noopener"' in ch0,'ch00 safe target'); ck('target="_blank"' in ap and 'rel="noopener"' in ap,'appendix safe target')
    svg=(site/ASSET).read_text(encoding='utf-8')
    for tok in ['<title id="title">','<desc id="desc">','viewBox="0 0 900 1280"','資訊結構 × 均衡概念選擇地圖','同時行動・完整資訊','純策略 Nash','mixed Nash','動態・perfect information','backward induction','SPNE','complete information','perfect information','incomplete information・Bayesian','Bayesian strategy','BNE','belief','sequential rationality','PBE','subgame・belief・off-path','singleton information set','Bayes rule','off-path beliefs','complete information ≠ perfect information','BNE ≠ PBE','均衡之後才談效率']:
        ck(tok in svg,f'svg token {tok}')
    ck('<image' not in svg,'no image tag'); ck('href="http' not in svg and "href='http" not in svg,'no remote href'); ck('javascript:' not in svg.lower(),'no javascript URL'); ck(len(re.findall(r'<rect\b',svg))>=6,'layout cards'); ck(len(re.findall(r'<text\b',svg))>=20,'readable text nodes')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'service worker version')
    expected_names={'applications-networks.svg','auctions.svg','bargaining.svg','bayesian-games.svg','continuous-best-response.svg','cooperative-games.svg','dominance-rationalizability.svg','extensive-backward-induction.svg','game-map.svg','mechanism-design.svg','mixed-nash.svg','modeling-solution-concepts.svg','normal-form-best-response.svg','pbe-beliefs.svg','pure-nash.svg','repeated-games.svg','screening-cheap-talk.svg','signaling.svg','spne-commitment.svg','zero-sum-minimax.svg'}
    ck({x.name for x in svgs}==expected_names,'SVG filename contract')
    for tok in ['complete information','perfect information','mixed Nash','pure Nash','backward induction','SPNE','BNE','PBE','singleton information set','off-path']:
        ck(tok in (ch0+ap+svg),f'high-risk concept {tok}')
    print(f'GAME_THEORY_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=20 appendices=3 questions=100 search=189 figures=20 visual_polish=passed')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_game_theory_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
