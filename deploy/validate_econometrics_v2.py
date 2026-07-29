#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

BOOK='econometrics'


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def visible_text(raw: str) -> str:
    text=re.sub(r'<[^>]+>',' ',raw)
    return html.unescape(re.sub(r'\s+',' ',text)).strip()


def has(text: str, token: str) -> bool:
    return token.casefold() in text.casefold()


def main(site_root: str) -> None:
    site=Path(site_root)
    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))['items']
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))['entries']
    chapters={m['id']:visible_text((root/m['file']).read_text(encoding='utf-8')) for m in manifest['chapters'] if m['kind']=='chapter'}
    qmap={q['id']:q for q in questions}
    checks=0

    def C(condition: bool, message: str) -> None:
        nonlocal checks
        check(condition,message)
        checks += 1

    C(len(chapters)==20,'20 generated chapters')
    C(len(questions)==100,'100 generated questions')
    C(len(search)==189,'189 search entries')
    C(set(chapters)=={f'ch{i:02d}' for i in range(20)},'chapter id set')

    chapter_requirements={
      'ch00':['描述平均關係、預測未來，還是估計某個政策或行為的因果效果','estimand','Identification','高 R² 是否足以證明因果關係'],
      'ch01':['標準差描述個別觀察值的離散程度；標準誤描述估計量的抽樣不確定性','大數法則','中央極限定理','s/sqrt(n)'],
      'ch02':['殘差平方和最小','R² 只回答樣本內','殘差 hat u_i','含截距 OLS 的殘差加總為 0'],
      'ch03':['Zero conditional mean','Homoskedasticity','Gauss–Markov','線性無偏估計量中具有最小變異數'],
      'ch04':['partialling out','控制變數可以減少混淆，但不是「越多越好」','Adjusted R²','處置後才發生的變數'],
      'ch05':['omitted-variable bias','反向因果','robust SE 不是解法','兩者同號是向上偏'],
      'ch06':['p-value','長期覆蓋率','F 檢定','統計顯著自動等同經濟上重要'],
      'ch07':['log-level','level-log','log-log','Dummy variable trap','beta1+beta3'],
      'ch08':['heteroskedasticity-robust standard errors','不改同一份 OLS 點估計','WLS','遺漏變數、反向因果'],
      'ch09':['Multicollinearity','high leverage','attenuation bias','測量誤差都往 0'],
      'ch10':['Linear Probability Model','百分點','p(1-p)','邊際效果會依當下 X 而變'],
      'ch11':['Weak stationarity','Random walk','spurious regression','高 R² 與顯著 t'],
      'ch12':['AR(1)','serial correlation','HAC','只換標準誤不夠'],
      'ch13':['First Differences','Fixed Effects','Random Effects','個體 FE 中無法單獨估係數'],
      'ch14':['relevance','exogeneity／exclusion','weak instrument','第一階段資料可以支持 relevance，但不能證明 exclusion'],
      'ch15':['Potential outcome','Average Treatment Effect','Intention-to-Treat','原始隨機分派組別比較結果'],
      'ch16':['parallel trends','2×2 DiD','event-study','不顯著」不是數學上的證明','cluster'],
      'ch17':['running variable','cutoff','local effect','精確操弄','Fuzzy RDD'],
      'ch18':['Training set','Test set','Overfitting','RMSE','MAE','Prediction 與 causal estimation'],
      'ch19':['Estimand','Identification','p-hacking','Reproducibility','效果大小、單位、標準誤或信賴區間'],
    }
    for cid,tokens in chapter_requirements.items():
        text=chapters[cid]
        for token in tokens:
            C(has(text,token),f'{cid} concept: {token}')

    correction_pairs={
      'ch00':[('高 R²','不能'),('因果','識別假設')],
      'ch03':[('異質變異','不讓 OLS 係數本身有偏'),('BLUE','線性無偏估計量')],
      'ch05':[('robust SE','不是解法'),('反向因果','內生性')],
      'ch08':[('robust standard errors','不改同一份 OLS 點估計'),('內生性','不能')],
      'ch09':[('多重共線性','精確度'),('測量誤差','特例')],
      'ch10':[('Logit','不再等於固定的百分點效果'),('因果','外生性')],
      'ch12':[('HAC','不是所有時間序列問題的萬靈丹'),('OLS 本身','不一致')],
      'ch13':[('FE','時間不變'),('RE','更強假設')],
      'ch14':[('first stage','不能證明 exclusion'),('weak instrument','不可靠')],
      'ch16':[('parallel trends','反事實假設'),('pre-trend','不是數學上的證明')],
      'ch17':[('local effect','不是整個母體平均效果'),('操弄','不再可比較')],
      'ch18':[('overfitting','未看過資料'),('預測更準','因果效果')],
    }
    for cid,pairs in correction_pairs.items():
        text=chapters[cid]
        for a,b in pairs:
            C(has(text,a) and has(text,b),f'{cid} correction pair: {a} / {b}')

    expected_difficulties={'基礎':1,'標準':2,'綜合':1,'陷阱':1}
    for i in range(20):
        cid=f'ch{i:02d}'
        qs=[q for q in questions if q['chapterId']==cid]
        C(len(qs)==5,f'{cid} five questions')
        C(Counter(q['difficulty'] for q in qs)==expected_difficulties,f'{cid} difficulty balance')
        for q in qs:
            C(bool(q['question'].strip()),f'{q["id"]} question text')
            C(bool(q['answer'].strip()),f'{q["id"]} answer text')
            C(len(q['explanation'].strip())>=18,f'{q["id"]} explanation substance')
            C(q['bookId']==BOOK,f'{q["id"]} book id')

    answer_gates={
      'ch00-q05':['不能','R²','配適'],
      'ch01-q05':['2','t='],
      'ch02-q05':['分母','0'],
      'ch03-q03':['否','同方差不是 OLS 無偏的必要條件'],
      'ch03-q04':['線性且無偏','最小變異數'],
      'ch04-q05':['不一定','處置後控制'],
      'ch05-q02':['向下偏','<0'],
      'ch05-q05':['不能','點估計'],
      'ch06-q05':['不拒絕 H0','不是證明 H0 為真'],
      'ch07-q04':['約 20%','exp'],
      'ch08-q02':['否','外生性'],
      'ch08-q04':['不能','內生性'],
      'ch09-q02':['精確度','不會單靠共線性'],
      'ch09-q05':['不正確','特定結果'],
      'ch10-q01':['7 個百分點','不是自動等於相對增加 7%'],
      'ch10-q05':['否','因果識別'],
      'ch11-q05':['可能','spurious regression'],
      'ch12-q05':['不能','點估計'],
      'ch13-q03':['不能','時間不變'],
      'ch13-q05':['個體效果 alpha_i','不相關'],
      'ch14-q03':['不能','exclusion'],
      'ch14-q04':['Weak instrument','relevance'],
      'ch15-q04':['原始隨機 assignment','保留隨機化'],
      'ch15-q05':['不要求','有限樣本'],
      'ch16-q03':['不是','反事實趨勢'],
      'ch16-q04':['不足以','不能完全證明'],
      'ch17-q03':['local effect','外推'],
      'ch17-q04':['局部可比性','continuity'],
      'ch18-q04':['可以','負值'],
      'ch18-q05':['不足以','Prediction'],
      'ch19-q01':['Estimand','先定義'],
      'ch19-q04':['不是','specification searching'],
    }
    for qid,tokens in answer_gates.items():
        C(qid in qmap,f'answer gate exists {qid}')
        combined=qmap[qid]['answer']+' '+qmap[qid]['explanation']
        for token in tokens:
            C(has(combined,token),f'{qid} answer gate: {token}')

    by_chapter=Counter(e['chapterId'] for e in search)
    for i in range(20):
        cid=f'ch{i:02d}'
        C(by_chapter[cid]==9,f'{cid} search entries')
        title=next(m['title'] for m in manifest['chapters'] if m['id']==cid)
        C(any(e['chapterId']==cid and e['title']==title for e in search),f'{cid} title searchable')
    for aid in ('appendix-a','appendix-b','appendix-c'):
        C(by_chapter[aid]==3,f'{aid} search entries')

    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    entries=[b for b in lib['books'] if b['id']==BOOK]
    C(len(entries)==1,'one library entry')
    C(entries[0]['status']=='available','library availability')
    C((site/'assets/econometrics-svg').is_dir(),'figure directory')
    C(len(list((site/'assets/econometrics-svg').glob('*.svg')))==20,'20 SVG files')

    print(f'ECONOMETRICS_QA_V2_OK checks={checks} chapters=20 questions=100 search=189 high_risk_answer_gates={len(answer_gates)}')


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/validate_econometrics_v2.py SITE_ROOT')
    main(sys.argv[1])
