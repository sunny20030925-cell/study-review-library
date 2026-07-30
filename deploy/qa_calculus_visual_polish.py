#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
B='calculus';V='2026.07.27-3';A='assets/calculus-svg/calculus-map.svg';M='data-vp-asset="calculus-limits-derivatives-integrals-series-multivariable-map"';C='DAHQ5AiFZNo';U='https://www.canva.com/d/J7WcMqzKE9zH_Cf'
def main(sr,ev):
 s=Path(sr);r=s/'books'/B;l=json.load(open(s/'data/library.json'));m=json.load(open(r/'manifest.json'));q=json.load(open(r/'questions.json'));se=json.load(open(r/'search.json'));n=0
 def ck(x,z):
  nonlocal n;n+=1
  if not x:raise AssertionError(z)
 ids=[x['id'] for x in l['books']];ck(l['version']==ev,'v');ck(len(ids)==21 and len(set(ids))==21 and ids.count(B)==1,'books');ck(m['id']==B and m['version']==V,'m');ck(len(m['chapters'])==17,'14+3');
 for x in m['chapters']:ck((r/x['file']).is_file(),x['file'])
 ck(q['count']==73 and len(q['items'])==73,'q');ck(len({x['id'] for x in q['items']})==73,'qid');ck(len(se['entries'])==150,'search');sv=list((s/'assets/calculus-svg').glob('*.svg'));ck(len(sv)==1,'svgcount');ck(sv[0].stat().st_size>50,'svgsize')
 ch=(r/'chapters/ch00.html').read_text();ap=(r/'chapters/appendix-b.html').read_text();svg=(s/A).read_text();ck(ch.count(M)==1 and ap.count(M)==1,'mark');ck(A in ch and A in ap,'asset');ck('target="_blank"' in ch and 'target="_blank"' in ap,'zoom');vp=m['visualPolish'];ck(vp['status']=='passed' and vp['asset']==A,'vp');ck(vp['canvaDesignId']==C and vp['canvaEditUrl']==U,'canva');ck(vp['tabletReadable'] and vp['zoomable'],'flags');ck(vp['offlineCachedViaExistingAssetPath'] is True and vp['offlineCachedViaServiceWorker'] is True and vp.get('offlineCacheMode')=='new-service-worker-cached-asset','cache mode')
 for t in ['大一微積分｜極限 → 導數 → 積分 → 級數 → 多變數判斷地圖','極限與連續','0/0','分母→0','連續：函數值存在','導數與最佳化','鏈鎖法則','臨界點＋邊界','MVT、L\'Hôpital','FTC','定積分是帶符號累積','代換','分部積分','瑕積分','級數先問必要條件 aₙ→0','Taylor','gradient','Lagrange multiplier','domain、符號、端點、單位、收斂與成立條件']:ck(t in svg,t)
 ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'remote');ck('javascript:' not in svg.lower(),'js');sw=(s/'sw.js').read_text();ck(f"const VERSION = 'study-library-{ev}';" in sw,'swv');ck(sw.count(A)==1,'cache once');
 for t in ['數、區間與絕對值','函數、輸入與輸出','複合函數與反函數']:ck(t in ch,t)
 for t in ['看到極限題','看到微分題']:ck(t in ap,t)
 ck('<title' in svg and 'role="img"' in svg,'access');print(f'CALCULUS_VP_QA_OK checks={n} books=21 library={ev} chapters=14 appendices=3 questions=73 search=150 figures=1 visual_polish=passed')
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
