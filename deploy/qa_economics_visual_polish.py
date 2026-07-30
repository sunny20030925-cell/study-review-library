#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
BOOK='economics';VERSION='2026.07.27-2';ASSET='assets/economics-svg/ppf.svg';MARKER='data-vp-asset="economics-shock-curves-equilibrium-welfare-policy-map"';CANVA='DAHQ5KUGsYE';URL='https://www.canva.com/d/MugMiO_8aGO0Myb'
def main(rootv,ev):
 site=Path(rootv);root=site/'books'/BOOK;lib=json.load(open(site/'data/library.json'));m=json.load(open(root/'manifest.json'));q=json.load(open(root/'questions.json'));s=json.load(open(root/'search.json'));checks=0
 def ck(c,x):
  nonlocal checks;checks+=1
  if not c: raise AssertionError(x)
 ids=[x['id'] for x in lib['books']];ck(lib['version']==ev,'version');ck(len(ids)==21 and len(set(ids))==21 and ids.count(BOOK)==1,'books');ck(m['id']==BOOK and m['version']==VERSION,'manifest');ck(len(m['chapters'])==23,'20+3 chapters');
 for x in m['chapters']: ck((root/x['file']).is_file(),x['file'])
 ck(q['count']==100 and len(q['items'])==100,'questions');ck(len({x['id'] for x in q['items']})==100,'qids');ck(len(s['entries'])==144,'search');svgs=list((site/'assets/economics-svg').glob('*.svg'));ck(len(svgs)==20,'svgs');
 for p in svgs: ck(p.stat().st_size>50,p.name)
 ch=(root/'chapters/ch00.html').read_text();ap=(root/'chapters/appendix-b.html').read_text();svg=(site/ASSET).read_text();ck(ch.count(MARKER)==1 and ap.count(MARKER)==1,'markers');ck(ASSET in ch and ASSET in ap,'asset placements');ck('target="_blank"' in ch and 'target="_blank"' in ap,'zoom');vp=m['visualPolish'];ck(vp['status']=='passed' and vp['asset']==ASSET,'vp');ck(vp['canvaDesignId']==CANVA and vp['canvaEditUrl']==URL,'canva');ck(vp['tabletReadable'] and vp['zoomable'] and vp['offlineCachedViaExistingAssetPath'],'flags')
 for t in ['經濟學原理｜衝擊 → 曲線 → 均衡 → 福利 → 政策判斷地圖','PPF','機會成本','沿需求／供給曲線移動','曲線位移','Qd＝Qs','彈性是比例反應','wedge','比較利益','正外部性','預算限制＋偏好','完全競爭、獨占','GDP、物價、失業','財政／貨幣政策','條件式模型','國際收支基本恆等關係','假設一起寫']:ck(t in svg,t)
 ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'remote');ck('javascript:' not in svg.lower(),'js');sw=(site/'sw.js').read_text();ck(f"const VERSION = 'study-library-{ev}';" in sw,'swv');ck(sw.count(ASSET)==1,'cache')
 for t in ['稀少性','機會成本與沉沒成本','邊際分析與誘因']:ck(t in ch,t)
 for t in ['圖形題六步驟','計算題五步驟']:ck(t in ap,t)
 ck('<title' in svg and 'role="img"' in svg,'access')
 print(f'ECONOMICS_VP_QA_OK checks={checks} books=21 library={ev} chapters=20 appendices=3 questions=100 search=144 figures=20 visual_polish=passed')
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
