#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

BOOK='macroeconomics'
V1='2026.07.29-1'
V2='2026.07.29-2'

HTML_REPLACEMENTS = {
'ch03.html': [
("自然失業率是通膨穩定時與勞動市場制度相容的失業率，不等於零，也不是永遠固定。人口結構、媒合效率、失業保險與產業變動都可能使它改變。",
 "自然失業率是由搜尋、媒合、人口結構與勞動市場制度等非景氣循環因素決定的長期均衡失業率，不等於零，也不是永遠固定。在簡化的搜尋流量模型中，若每期就業者有 s 比例離職、失業者有 f 比例找到工作，穩態失業率為 \\(u^*=s/(s+f)\\)。在 Phillips curve 分析中，自然失業率常與通膨不加速失業率（NAIRU）近似連結，但兩者概念並非完全同義。"),
],
'ch12.html': [
("也可用國民儲蓄與投資平衡說明：較高所得提高儲蓄，為使儲蓄等於較低投資，需要較低利率。不同推導描述同一商品市場均衡。",
 "也可用國民儲蓄與投資平衡說明：較高所得提高儲蓄；為使投資提高到與較高儲蓄相等，需要較低利率來刺激投資。不同推導描述同一商品市場均衡。"),
],
'ch14.html': [
("若工資或部分價格事先訂定，實際物價高於預期時，企業的實質收益可能上升而增加產出，SRAS 向上。不同微觀機制可導出相似圖形。",
 "在僵固工資模型中，名目工資事先訂定；若實際物價高於原先預期，實質工資 \\(W/P\\) 下降，企業提高勞動需求與產出，因此 SRAS 向上。僵固價格或不完全資訊模型也可導出相似的短期正斜率，但傳導機制不同。"),
],
'ch17.html': [
("簡化規則可寫 \\(i=i^*+\\phi_\\pi(\\pi-\\pi^*)+\\phi_y\\tilde y\\)。若通膨高於目標，央行通常提高名目利率；為使實質利率上升，對通膨反應常需大於一。",
 "令 \\(\\bar i=r^*+\\pi^*\\) 表示通膨在目標時的中性名目利率，一種簡化規則可寫 \\(i=\\bar i+\\phi_\\pi(\\pi-\\pi^*)+\\phi_y\\tilde y\\)。若實際通膨與預期通膨同步上升，名目利率對通膨的反應係數需大於 1，實質政策利率才會上升；這就是 Taylor principle 的核心直覺。不同教材也會把當期通膨本身另外寫進規則，因此解讀係數前要先看公式參數化方式。"),
],
'ch18.html': [
("開放經濟同時交易商品、服務與資產。國民所得帳把淨出口與儲蓄投資差額相連，匯率則是兩種貨幣或兩國商品的相對價格。",
 "開放經濟同時交易商品、服務、所得、移轉與資產。完整國際帳中，經常帳 CA 包含淨出口、國外淨要素所得與淨經常移轉；國民儲蓄與投資的核心恆等式是 \\(CA=S-I\\)。若教材簡化忽略國外所得與移轉，才有 \\(CA\\approx NX\\)，因此可寫 \\(NX\\approx S-I\\)。匯率則是兩種貨幣或兩國商品的相對價格。"),
("<h2 id=\"淨出口與資本流動\">淨出口與資本流動</h2><p>在簡化帳面下 \\(NX=S-I\\)。若國民儲蓄低於國內投資，需由海外融資，常伴隨淨出口為負。這是帳面連結，不表示單一變數永遠單向造成另一變數。</p>",
 "<h2 id=\"淨出口與資本流動\">淨出口、經常帳與資本流動</h2><p>完整帳面以 \\(CA=S-I\\) 為準；若忽略國外淨要素所得與淨經常移轉，才可把經常帳近似為淨出口，寫成 \\(NX\\approx S-I\\)。若國民儲蓄低於國內投資，差額需由海外淨融資對應。這是會計連結，不表示單一變數永遠單向造成另一變數。</p>"),
("絕對 PPP 認為同質可交易品換算後價格相同；相對 PPP 認為匯率變動長期近似兩國通膨差。運輸、關稅、非貿易品與價格僵固使短期偏離常見。",
 "絕對 PPP 認為同質可交易品換算後價格相同。以本書 \\(e=\\text{NT$/US$}\\) 的『本國貨幣／外幣』報價，相對 PPP 的近似式為 \\(\\Delta e/e\\approx\\pi_{TW}-\\pi_{US}\\)：本國通膨高於外國時，本國貨幣傾向貶值。運輸、關稅、非貿易品與價格僵固使短期偏離常見。"),
("經常帳赤字可能反映高投資，也可能反映低儲蓄；品質取決於資金用途、融資結構與償付能力。不能把盈餘或赤字本身直接等同好壞。",
 "由 \\(CA=S-I\\)，經常帳赤字可能反映高投資，也可能反映低儲蓄；品質取決於資金用途、融資結構與償付能力。經常帳不是單純的商品貿易餘額，因此不能把盈餘或赤字本身直接等同好壞。"),
("開放經濟帳把淨出口與儲蓄投資差額相連；匯率方向必須先依報價定義；PPP 與利率平價是附帶條件的基準，不是短期定律。",
 "完整開放經濟帳以 \\(CA=S-I\\) 連結國民儲蓄與投資；簡化忽略所得與移轉時才以 \\(NX\\approx CA\\) 代替。匯率方向必須先依報價定義；PPP 與利率平價是附帶條件的基準，不是短期定律。"),
],
'ch19.html': [
("擴張性貨幣政策壓低利率，引發資本流出與本幣貶值，淨出口增加，強化產出效果。因此在標準完全資本流動、價格固定模型中較有效。",
 "在標準小型開放經濟、完全資本流動、價格固定且浮動匯率的模型中，擴張性貨幣政策使本國利率短暫低於世界利率，引發資本流出與本幣貶值，淨出口增加；利率回到世界利率時，均衡產出高於原先水準。因此貨幣政策在這組嚴格假設下具有明確的產出效果。"),
("財政擴張推高利率，引發資本流入與本幣升值，淨出口下降，抵銷部分甚至大部分擴張。不能把「較弱」誤寫成任何條件下完全無效。",
 "在標準小型開放經濟、完全資本流動、價格固定且浮動匯率的 Mundell–Fleming 模型中，財政擴張使利率出現上升壓力，資本流入推動本幣升值，淨出口下降；匯率調整會把 IS 拉回，使均衡產出在基準模型中不變，也就是財政擴張被完全抵銷。若資本流動不完全、存在風險溢酬、匯率反應有限或央行另有反應，現實效果才可能只被部分抵銷。"),
("若央行承諾固定匯率，利率下降造成貶值壓力時，央行需賣外匯、收回本幣，抵銷原擴張。因此標準模型中獨立貨幣政策空間受限。",
 "若央行承諾固定匯率，獨立貨幣擴張使利率出現下降壓力並造成資本流出與貶值壓力；央行必須賣外匯、收回本幣以維持匯率，因而把原本的貨幣擴張反轉。在標準完全資本流動模型中，獨立貨幣政策對產出沒有持久效果。"),
("財政擴張造成升值壓力時，央行為維持匯率買入外匯、投放本幣，貨幣供給配合增加，可能強化財政效果。結論依完全資本流動與可信固定匯率。",
 "財政擴張造成升值壓力時，央行為維持固定匯率買入外匯、投放本幣，使貨幣供給內生增加並配合 IS 右移；因此在標準完全資本流動、可信固定匯率模型中，財政政策具有明確且較強的產出效果。放寬資本流動與固定匯率假設後，效果大小會改變。"),
],
'appendix-a.html': [
("常用式包括：Y=C+I+G+NX；S=Y-C-G；1+i=(1+r)(1+πᵉ)；Δk=sf(k)-(n+g+δ)k；貨幣乘數 (1+c)/(rr+e+c)；政府支出乘數 1/(1-c)；定額稅乘數 -c/(1-c)；以及債務比近似式 Δb≈(r-g)b-ps。",
 "常用式包括：Y=C+I+G+NX；完整開放經濟帳 CA=S-I（忽略國外所得與移轉時 CA≈NX）；1+i=(1+r)(1+πᵉ)；Δk=sf(k)-(n+g+δ)k；貨幣乘數 (1+c)/(rr+e+c)；政府支出乘數 1/(1-c)；定額稅乘數 -c/(1-c)；以及債務比近似式 Δb≈(r-g)b-ps。"),
],
}

QUESTION_PATCHES = {
'ch00-q03': {
 'answer':'2 個百分點。',
 'explanation':'5%-3%=2 個百分點；百分點用來比較兩個百分率的差，不能寫成「增加 2%」。'
},
'ch03-q04': {
 'question':'若每期就業者離職率 s=2%、失業者找工作率 f=18%，簡化搜尋流量模型的穩態自然失業率 u*=s/(s+f) 為多少？',
 'answer':'10%。',
 'explanation':'0.02/(0.02+0.18)=10%。s 是離職率、f 是失業者找到工作的比率；不能把失業率或職缺率直接代入這個公式。'
},
'ch16-q03': {
 'question':'債務比 b=1、實質利率 r=4%、實質成長率 g=2%，若初級盈餘比率 ps 不變且只看 (r-g)b 這一項，債務比約增加多少？',
 'answer':'約增加 2 個 GDP 百分點。',
 'explanation':'(r-g)b=(0.04-0.02)×1=0.02，也就是債務占 GDP 比率約增加 2 個百分點。'
},
'ch17-q01': {
 'question':'在 i=ī+φπ(π-π*)+φyỹ 的簡化規則中，若通膨與預期通膨都上升 2 個百分點、φπ=1、產出缺口不變，事前實質政策利率約如何變？',
 'answer':'約不變。',
 'explanation':'名目利率上升 2 個百分點，預期通膨也上升 2 個百分點，因此事前實質利率約不變；在這個參數化下，Taylor principle 要求 φπ>1。'
},
'ch18-q01': {
 'question':'若忽略國外淨要素所得與淨經常移轉，國民儲蓄 500、國內投資 420，簡化帳面下淨出口約是多少？',
 'answer':'80。',
 'explanation':'完整關係為 CA=S-I；在忽略國外所得與移轉的簡化下 CA≈NX，所以 NX≈500-420=80。'
},
'ch18-q04': {
 'question':'本書採 e=NT$/US$。相對購買力平價下，若臺灣通膨率高於美國 2 個百分點，長期 e 約往哪個方向變？',
 'answer':'e 約上升 2%，亦即新臺幣傾向貶值。',
 'explanation':'以本國貨幣／外幣報價，Δe/e≈π_TW-π_US；本國通膨較高時，需要更多新臺幣兌換一美元。'
},
'ch19-q02': {
 'question':'在標準小型開放經濟、完全資本流動、價格固定且浮動匯率的 Mundell–Fleming 模型中，財政擴張對均衡產出的基準效果為何？',
 'answer':'均衡產出不變；本幣升值使淨出口下降，完全抵銷財政擴張。',
 'explanation':'財政擴張使利率出現上升壓力，資本流入推動本幣升值；淨出口下降使 IS 回到與世界利率相容的位置。放寬完全資本流動等假設後才可能只有部分抵銷。'
},
}

SEARCH_REPLACEMENTS = []
for reps in HTML_REPLACEMENTS.values():
    for old,new in reps:
        if '<h2' not in old:
            SEARCH_REPLACEMENTS.append((old,new))
SEARCH_REPLACEMENTS.append((
 '在簡化帳面下 \\(NX=S-I\\)。若國民儲蓄低於國內投資，需由海外融資，常伴隨淨出口為負。這是帳面連結，不表示單一變數永遠單向造成另一變數。',
 '完整帳面以 \\(CA=S-I\\) 為準；若忽略國外淨要素所得與淨經常移轉，才可把經常帳近似為淨出口，寫成 \\(NX\\approx S-I\\)。若國民儲蓄低於國內投資，差額需由海外淨融資對應。這是會計連結，不表示單一變數永遠單向造成另一變數。'
))

def replace_once(text, old, new, label):
    count=text.count(old)
    if count!=1:
        raise AssertionError(f'{label}: expected 1 occurrence, got {count}')
    return text.replace(old,new,1)

def main(site_root):
    site=Path(site_root)
    root=site/'books'/BOOK
    for fn,reps in HTML_REPLACEMENTS.items():
        p=root/'chapters'/fn
        text=p.read_text(encoding='utf-8')
        for i,(old,new) in enumerate(reps,1):
            text=replace_once(text,old,new,f'{fn} replacement {i}')
        p.write_text(text,encoding='utf-8')

    qpath=root/'questions.json'
    q=json.loads(qpath.read_text(encoding='utf-8'))
    if q.get('version')!=V1:
        raise AssertionError(f'questions starting version {q.get("version")}')
    qmap={x['id']:x for x in q['items']}
    for qid,changes in QUESTION_PATCHES.items():
        if qid not in qmap: raise AssertionError(qid)
        qmap[qid].update(changes)
    q['version']=V2
    qpath.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    spath=root/'search.json'
    s=json.loads(spath.read_text(encoding='utf-8'))
    for entry in s['entries']:
        text=entry['text']
        for old,new in SEARCH_REPLACEMENTS:
            if old in text:
                text=text.replace(old,new)
        entry['text']=text
        if entry.get('chapterId')=='ch18' and entry.get('title')=='淨出口與資本流動':
            entry['title']='淨出口、經常帳與資本流動'
    spath.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    mpath=root/'manifest.json'
    m=json.loads(mpath.read_text(encoding='utf-8'))
    if m.get('version')!=V1: raise AssertionError(f'manifest starting version {m.get("version")}')
    m['version']=V2
    m['updatedAt']='2026-07-29'
    m['releaseNotes'].insert(0,{
      'version':V2,'date':'2026-07-29','title':'發布後第二次獨立內容複核與糾錯',
      'changes':[
        '修正百分點題目答案，避免把百分點誤寫成百分比',
        '修正自然失業率搜尋流量題的變數定義，區分離職率、找工作率與 NAIRU',
        '修正 IS 儲蓄投資推導方向，並精確化 SRAS 與 Taylor principle 的條件',
        '補正完整經常帳 CA=S-I、相對 PPP 匯率方向與淨出口簡化條件',
        '明確化標準 Mundell–Fleming 在完全資本流動下的浮動／固定匯率政策基準結論',
        '同步修正 7 題題幹、答案或詳解，並重新驗算全書量化題與模型方向',
      ],
      'progressImpact':'章節 ID、題目 ID 與題數均未變；既有閱讀進度與錯題紀錄保留。'
    })
    mpath.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'MACRO_V2_PATCH_OK content_replacements={sum(len(v) for v in HTML_REPLACEMENTS.values())} question_adjustments={len(QUESTION_PATCHES)}')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: patch_macroeconomics_v2.py SITE_ROOT')
    main(sys.argv[1])
