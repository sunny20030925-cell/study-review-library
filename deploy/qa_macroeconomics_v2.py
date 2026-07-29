#!/usr/bin/env python3
from __future__ import annotations
import json, sys, re
from pathlib import Path
from collections import Counter
BOOK="macroeconomics"; VERSION="2026.07.29-2"
checks=0
def ck(c,msg):
 global checks; checks+=1
 if not c: raise AssertionError(msg)
def main(site_root, expected_library="2026.07.29-15"):
 site=Path(site_root); root=site/"books"/BOOK
 m=json.loads((root/"manifest.json").read_text()); q=json.loads((root/"questions.json").read_text()); s=json.loads((root/"search.json").read_text()); lib=json.loads((site/"data/library.json").read_text())
 ck(m["version"]==q["version"]==VERSION,"book version"); ck(lib["version"]==expected_library,"library version")
 ids=[x["id"] for x in lib["books"]]
 legacy_order=(len(ids)==11 and ids[-3:]==["macroeconomics","international-economics","public-finance"])
 money_order=(len(ids)==12 and ids[-4:]==["macroeconomics","international-economics","public-finance","money-banking"])
 civil_order=(len(ids)==13 and ids[-5:]==["macroeconomics","international-economics","public-finance","money-banking","civil-law-overview"])
 ck(legacy_order or money_order or civil_order,"canonical book order")
 chapters=[x for x in m["chapters"] if x["kind"]=="chapter"]; apps=[x for x in m["chapters"] if x["kind"]=="appendix"]
 ck(len(chapters)==20,"chapters"); ck(len(apps)==3,"appendices"); ck(q["count"]==len(q["items"])==100,"questions"); ck(len(s["entries"])==143,"search"); ck(len({x["id"] for x in q["items"]})==100,"unique qids"); ck(Counter(x["chapterId"] for x in q["items"])=={f"ch{i:02d}":5 for i in range(20)},"five each")
 qmap={x["id"]:x for x in q["items"]}
 expected={"ch00-q03":("2 個百分點。","百分點"),"ch00-q04":("約 4%。","名目成長"),"ch01-q04":("S=150，I=150。","S=Y-C-G"),"ch01-q05":("NX=-80。","300-380"),"ch02-q01":("5%。","(126-120)/120"),"ch02-q03":("120。","2.4/2.0"),"ch02-q04":("約 4%。","i-π"),"ch03-q01":("約 5.26%。","50/950"),"ch03-q04":("10%。","0.02/(0.02+0.18)"),"ch04-q02":("0.7。","份額"),"ch04-q03":("約 3.9%。","0.3×4"),"ch06-q01":("私人儲蓄 250、政府儲蓄 -50、國民儲蓄 200。","Sp=1200"),"ch07-q01":("0.7。","700/1000"),"ch07-q02":("NT$80。","0.8×100"),"ch09-q03":("10。","1/0.1"),"ch10-q03":("約由 3% 升到 6%。","i≈r+π"),"ch11-q02":("NT$40 億。","1/(1-0.75)"),"ch11-q03":("-3。","-0.75/(1-0.75)"),"ch16-q03":("約增加 2 個 GDP 百分點。","0.04-0.02"),"ch18-q01":("80。","CA=S-I")}
 for qid,(ans,exp_token) in expected.items(): ck(qmap[qid]["answer"]==ans,f"{qid} answer"); ck(exp_token in qmap[qid]["explanation"],f"{qid} explanation")
 ck("離職率 s=2%" in qmap["ch03-q04"]["question"] and "找工作率 f=18%" in qmap["ch03-q04"]["question"],"search-flow variables")
 ck("不能把失業率或職缺率直接代入" in qmap["ch03-q04"]["explanation"],"search-flow negative gate")
 ck("通膨與預期通膨都上升 2 個百分點" in qmap["ch17-q01"]["question"],"taylor assumption")
 ck("Taylor principle" in qmap["ch17-q01"]["explanation"],"taylor explanation")
 ck(qmap["ch18-q04"]["answer"].startswith("e 約上升 2%") and "新臺幣傾向貶值" in qmap["ch18-q04"]["answer"],"PPP direction")
 ck("均衡產出不變" in qmap["ch19-q02"]["answer"] and "完全抵銷" in qmap["ch19-q02"]["answer"],"MF fiscal result")
 text="\n".join((root/x["file"]).read_text(encoding="utf-8") for x in m["chapters"])
 required=["穩態失業率為 \\(u^*=s/(s+f)\\)","NAIRU","兩者概念並非完全同義","為使投資提高到與較高儲蓄相等，需要較低利率","實質工資 \\(W/P\\) 下降","Taylor principle","不同教材也會把當期通膨本身另外寫進規則","經常帳 CA 包含淨出口、國外淨要素所得與淨經常移轉","\\(CA=S-I\\)","\\(CA\\approx NX\\)","\\(\\Delta e/e\\approx\\pi_{TW}-\\pi_{US}\\)","本國貨幣傾向貶值","均衡產出在基準模型中不變","財政擴張被完全抵銷","獨立貨幣政策對產出沒有持久效果"]
 for token in required: ck(token in text,f"missing corrected token {token}")
 forbidden=["為使儲蓄等於較低投資，需要較低利率","企業的實質收益可能上升而增加產出","抵銷部分甚至大部分擴張","自然失業率是通膨穩定時與勞動市場制度相容的失業率"]
 for token in forbidden: ck(token not in text,f"forbidden stale text {token}")
 ck(qmap["ch00-q03"]["answer"]!="約 2%。","percentage point stale answer"); ck("職缺率 2%、失業率 18%" not in qmap["ch03-q04"]["question"],"bad flow rates removed")
 for ch in m["chapters"]:
  p=root/ch["file"]; ck(p.is_file() and p.stat().st_size>500,f"file {ch['id']}"); h=p.read_text(encoding="utf-8"); ck("\f" not in h and "\t" not in h,f"controls {ch['id']}"); ck("<script" not in h.lower(),f"inline script {ch['id']}")
 figs=list((site/"assets/macroeconomics-svg").glob("*.svg")); ck(len(figs)==20,"figures")
 for f in figs:
  x=f.read_text(); ck("<title" in x and "<desc" in x and "viewBox=" in x,f"figure accessibility {f.name}"); ck("href=\"http" not in x and "href='http" not in x,f"remote {f.name}")
 ck(m["releaseNotes"][0]["version"]==VERSION,"release note v2"); ck("發布後第二次獨立內容複核與糾錯"==m["releaseNotes"][0]["title"],"release note title"); ck("章節 ID、題目 ID 與題數均未變" in m["releaseNotes"][0]["progressImpact"],"progress note")
 sw=(site/"sw.js").read_text(); ck(f"study-library-{expected_library}" in sw,"sw version")
 for token in ["./books/macroeconomics/manifest.json","./books/macroeconomics/questions.json","./books/macroeconomics/search.json","./books/macroeconomics/chapters/ch19.html","./assets/macroeconomics-svg/mundell-fleming.svg"]: ck(token in sw,f"sw path {token}")
 corpus="\n".join(e["title"]+" "+e["text"] for e in s["entries"])
 for token in ["CA=S-I","NAIRU","Taylor principle","完全抵銷"]: ck(token in corpus,f"search corrected concept {token}")
 for token in ["職缺率 2%、失業率 18%","為使儲蓄等於較低投資"]: ck(token not in corpus,f"search stale token {token}")
 print(f"MACROECONOMICS_V2_QA_OK checks={checks} books={len(ids)} library={expected_library} chapters=20 appendices=3 questions=100 search=143 figures=20 quantitative_rechecks={len(expected)} content_corrections=14 question_adjustments=7")
if __name__=="__main__":
 if len(sys.argv) not in (2,3): raise SystemExit("usage: qa_macroeconomics_v2.py SITE_ROOT [EXPECTED_LIBRARY]")
 main(sys.argv[1],sys.argv[2] if len(sys.argv)==3 else "2026.07.29-15")
