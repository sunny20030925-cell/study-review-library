#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
B='computer-fundamentals';V='2026.07.30-2';A='assets/computer-fundamentals-svg/computing-map.svg';M='data-vp-asset="computer-data-hardware-os-network-program-security-map"';C='DAHQ5HKTq5M';U='https://www.canva.com/d/pgWvtGBlDcRP0Nd'
def main(sr,ev):
 s=Path(sr);r=s/'books'/B;l=json.load(open(s/'data/library.json'));m=json.load(open(r/'manifest.json'));q=json.load(open(r/'questions.json'));se=json.load(open(r/'search.json'));n=0
 def ck(x,z):
  nonlocal n;n+=1
  if not x:raise AssertionError(z)
 ids=[x['id'] for x in l['books']];ck(l['version']==ev,'v');ck(len(ids)==21 and len(set(ids))==21 and ids.count(B)==1,'books');ck(m['id']==B and m['version']==V,'m');ck(len(m['chapters'])==23,'23');
 for x in m['chapters']:ck((r/x['file']).is_file(),x['file'])
 ck(q['count']==100 and len(q['items'])==100,'q');ck(len({x['id'] for x in q['items']})==100,'qid');ck(len(se['entries'])==150,'search');sv=list((s/'assets/computer-fundamentals-svg').glob('*.svg'));ck(len(sv)==20,'svgcount');
 for p in sv:ck(p.stat().st_size>50,p.name)
 ch=(r/'chapters/ch00.html').read_text();ap=(r/'chapters/appendix-b.html').read_text();svg=(s/A).read_text();ck(ch.count(M)==1 and ap.count(M)==1,'mark');ck(A in ch and A in ap,'asset');ck('target="_blank"' in ch and 'target="_blank"' in ap,'zoom');vp=m['visualPolish'];ck(vp['status']=='passed' and vp['asset']==A,'vp');ck(vp['canvaDesignId']==C and vp['canvaEditUrl']==U,'canva');ck(vp['tabletReadable'] and vp['zoomable'] and vp['offlineCachedViaExistingAssetPath'],'flags')
 for t in ['計算機概論｜資料 → 硬體 → OS → 網路 → 程式 → 安全判斷地圖','bit／byte','4 KiB＝4096 bytes','clock、instruction count、CPI','2 GHz 一 cycle＝0.5 ns','virtual memory','process 與 thread','page fault','Big-O','Θ','ACID','switch／router','MAC／IP','TCP：可靠、依序 byte stream','UDP 不保證','HTTP/3 使用 QUIC','TLS 1.3','100 Mb/s 理論值＝12.5 MB/s','authentication ≠ authorization','salted password hashing','essential characteristics','training、inference、evaluation']:ck(t in svg,t)
 ck(not re.search(r'(?:href|xlink:href)=["\']https?://',svg),'remote');ck('javascript:' not in svg.lower(),'js');sw=(s/'sw.js').read_text();ck(f"const VERSION = 'study-library-{ev}';" in sw,'swv');ck(sw.count(A)==1,'cache');
 for t in ['本章要解決的問題','正式定義與核心概念','考試判斷方法']:ck(t in ch,t)
 for t in ['進位與容量題','硬體與作業系統題','網路題','演算法資料題','安全、AI 與現代系統題']:ck(t in ap,t)
 ck('<title' in svg and 'role="img"' in svg,'access');print(f'COMPUTER_FUNDAMENTALS_VP_QA_OK checks={n} books=21 library={ev} chapters=20 appendices=3 questions=100 search=150 figures=20 visual_polish=passed')
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
