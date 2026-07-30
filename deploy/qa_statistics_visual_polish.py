#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path
BOOK='statistics'; VERSION='2026.07.29-2'; ASSET='assets/statistics-svg/data-process.svg'; MARKER='data-vp-asset="statistics-inference-method-selection-map"'; CANVA='DAHQ3VXu1eY'

def main(site_root:str, expected_library:str)->None:
    site=Path(site_root); root=site/'books'/BOOK
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    checks=0
    def ck(c,msg):
        nonlocal checks; checks+=1
        if not c: raise AssertionError(msg)
    ids=[b['id'] for b in lib['books']]
    ck(lib['version']==expected_library,'library version'); ck(len(ids)==21,'21 books'); ck(len(ids)==len(set(ids)),'unique books'); ck(ids.count(BOOK)==1,'statistics once')
    ck(m.get('id')==BOOK,'book id'); ck(m.get('version')==VERSION,'content version'); ck(len(m.get('chapters',[]))==22,'19 chapters + 3 appendices')
    chapter_ids=[x.get('id') for x in m['chapters']]; ck(len(set(chapter_ids))==22,'unique chapter ids'); ck(all(f'ch{i:02d}' in chapter_ids for i in range(19)),'ch00-ch18'); ck(all(x in chapter_ids for x in ['appendix-a','appendix-b','appendix-c']),'appendices')
    items=q.get('items',[]); ck(q.get('count')==95 and len(items)==95,'95 questions'); ck(len({x.get('id') for x in items})==95,'unique question ids'); ck(len(s.get('entries',[]))==169,'169 search entries')
    svgs=sorted((site/'assets/statistics-svg').glob('*.svg')); ck(len(svgs)==19,'19 svgs'); ck((site/ASSET).exists(),'vp asset exists')
    vp=m.get('visualPolish',{}); ck(vp.get('status')=='passed','vp passed'); ck(vp.get('asset')==ASSET,'vp asset'); ck(vp.get('canvaDesignId')==CANVA,'canva id'); ck(vp.get('placement')=='ch00 and appendix-b','placement'); ck(vp.get('tabletReadable') is True,'tablet'); ck(vp.get('zoomable') is True,'zoom'); ck(vp.get('offlineCachedViaExistingAssetPath') is True,'cache path')
    ch0=(root/'chapters/ch00.html').read_text(encoding='utf-8'); ap=(root/'chapters/appendix-b.html').read_text(encoding='utf-8')
    ck(ch0.count(MARKER)==1,'ch00 marker once'); ck(ap.count(MARKER)==1,'appendix marker once'); ck(ASSET in ch0 and ASSET in ap,'asset placements'); ck('target="_blank"' in ch0 and 'target="_blank"' in ap,'zoom links')
    svg=(site/ASSET).read_text(encoding='utf-8')
    for token in ['<title','<desc','viewBox="0 0 900 1280"','一個母數','母體 σ 未知通常用 t','p̂','p₀','Welch t','pooled p','ANOVA','χ²','R²=r²','含截距','隨機抽樣','隨機分派','觀察值獨立','同等或更極端','統計顯著 ≠ 實質重要','關聯 ≠ 因果','未拒絕 H₀ ≠ 證明相等']:
        ck(token in svg,'svg token '+token)
    ck(not re.search(r'(?:href|src)=\"https?://',svg),'no remote svg links')
    sw=(site/'sw.js').read_text(encoding='utf-8'); ck(f"const VERSION = 'study-library-{expected_library}';" in sw,'sw version'); ck(ASSET in sw,'asset remains offline cached')
    for p in svgs:
        t=p.read_text(encoding='utf-8'); ck('<title' in t,p.name+' title'); ck('<desc' in t,p.name+' desc'); ck('viewBox=' in t,p.name+' viewBox')
    ck(all((root/'chapters'/f'ch{i:02d}.html').exists() for i in range(19)),'chapter htmls'); ck(all((root/'chapters'/f'appendix-{x}.html').exists() for x in 'abc'),'appendix htmls')
    print(f'STATISTICS_VP_QA_OK checks={checks} books=21 library={expected_library} chapters=19 appendices=3 questions=95 search=169 figures=19 visual_polish=passed')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: qa_statistics_visual_polish.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1],sys.argv[2])
