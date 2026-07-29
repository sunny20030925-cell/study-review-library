#!/usr/bin/env python3
from __future__ import annotations
import json,sys,re
from pathlib import Path

BOOK='civil-law-overview'; VERSION='2026.07.29-1'
checks=0

def ck(cond,msg):
    global checks; checks+=1
    if not cond: raise AssertionError(msg)

def main(site_root, expected_library='2026.07.29-18'):
    site=Path(site_root); root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ck(lib['version']==expected_library,'library version')
    ck(len(lib['books'])==13 and lib['books'][-1]['id']==BOOK,'book tail')
    qmap={x['id']:x for x in q['items']}
    ck(q.get('count')==100 and len(q['items'])==100,'100 questions present')
    ck(len(qmap)==100,'100 unique question ids')
    expected_qids={f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)}
    ck(set(qmap)==expected_qids,'complete question id grid')
    for qid,item in sorted(qmap.items()):
        ck(item.get('bookId')==BOOK,f'{qid} book id')
        ck(item.get('chapterId')==qid[:4],f'{qid} chapter id')
        ck(bool(item.get('question','').strip()),f'{qid} question text')
        ck(bool(item.get('answer','').strip()),f'{qid} answer text')
        ck(bool(item.get('explanation','').strip()),f'{qid} explanation text')
        ck(item.get('source')=='本書自編標準題型',f'{qid} source')
    exact={
      'ch01-q01':'滿 18 歲為成年；新制自 2023 年 1 月 1 日施行。',
      'ch05-q01':'15 年。',
      'ch05-q02':'5 年。',
      'ch09-q01':'視為要約。',
      'ch12-q04':'自知悉損害及賠償義務人起 2 年；自侵權行為時起逾 10 年亦同。',
      'ch17-q01':'18 歲。',
      'ch19-q02':'配偶、子女甲、子女乙各三分之一。',
      'ch19-q03':'自知悉其得繼承之時起 3 個月內，以書面向法院為之。',
    }
    for qid,ans in exact.items(): ck(qmap[qid]['answer']==ans,f'{qid} exact answer')
    ck('效力未定' in qmap['ch01-q02']['answer'] and '永久無效' in qmap['ch01-q02']['answer'],'minor contract effect')
    ck('發見詐欺後 1 年內' in qmap['ch03-q03']['answer'] and '10 年' in qmap['ch03-q03']['answer'],'fraud period')
    ck('通知後 6 個月' in qmap['ch10-q04']['answer'] and '5 年' in qmap['ch10-q04']['answer'],'sale defect period')
    ck('第 758 條' in qmap['ch13-q01']['answer'] and '登記' in qmap['ch13-q01']['answer'],'immovable registration')
    ck('尚未施行' in qmap['ch13-q05']['answer'],'166-1 gate')
    ck('共有人過半數' in qmap['ch14-q02']['answer'] and '逾三分之二' in qmap['ch14-q02']['answer'],'coownership threshold')
    ck('二人以上證人' in qmap['ch17-q02']['answer'] and '戶政機關' in qmap['ch17-q02']['answer'],'marriage form')
    ck('司法院釋字第七四八號解釋施行法' in qmap['ch17-q05']['answer'],'same-sex special act')
    ck('直系血親卑親屬、父母、兄弟姊妹、祖父母' in qmap['ch19-q01']['answer'],'inheritance order')
    ck('不是' in qmap['ch19-q04']['answer'] and '拋棄繼承' in qmap['ch19-q04']['answer'],'representation vs renunciation')
    ck('未滿 16 歲不得為遺囑' in qmap['ch19-q05']['answer'],'will age')

    text='\n'.join((root/x['file']).read_text(encoding='utf-8') for x in m['chapters'])
    gates={
      'adult_18':['滿 18 歲為成年','2023 年 1 月 1 日'],
      'minor_7':['未滿 7 歲','限制行為能力'],
      'general_limitation':['民法第 125 條','15 年'],
      'interest_cap':['週年利率超過 16%'],
      'tort':['民法第 184 條','民法第 197 條'],
      'immovable':['民法第 758 條','非經登記不生效力'],
      'article_166_1':['民法第 166-1 條','施行日期尚未另定'],
      'lease_20_year':['民法第 449 條','租用基地建築房屋'],
      'coownership':['民法第 820 條','共有人過半數','逾三分之二'],
      'marriage':['民法第 980、982 條','未滿 18 歲不得結婚','二人以上證人','戶政機關'],
      'same_sex':['司法院釋字第七四八號解釋施行法'],
      'inheritance':['民法第 1138、1139 條','民法第 1140 條','拋棄繼承不是第 1140 條'],
      'renunciation':['民法第 1174 條','三個月內','以書面向法院'],
      'will':['民法第 1186、1189、1223 條','未滿 16 歲不得為遺囑','特留分'],
    }
    compact=' '.join(text.split())
    for name,tokens in gates.items():
        for token in tokens: ck(token in compact,f'{name} missing {token}')
    stale=[
      r'滿\s*20\s*歲為成年',r'滿二十歲為成年',r'未成年人已結婚者，有行為能力',r'禁治產人',
      r'男未滿十八歲.*女未滿十六歲',r'不動產負擔契約一律必須公證才有效',r'拋棄繼承.*代位繼承其應繼分'
    ]
    for pat in stale: ck(re.search(pat,compact) is None,f'stale law pattern {pat}')
    corpus='\n'.join(e['title']+' '+e['text'] for e in s['entries'])
    for token in ['請求權基礎','效力未定','15 年','第 166-1 條','尚未另定','三個月內','司法院釋字第七四八號解釋施行法']:
        ck(token in corpus,f'search token {token}')
    print(f'CIVIL_LAW_OVERVIEW_QA2_OK checks={checks} legal_gates={len(gates)} questions_rechecked=100 high_risk_questions={len(exact)+11} current_law_baseline=2026-07-29')

if __name__=='__main__':
    if len(sys.argv) not in (2,3): raise SystemExit('usage: python deploy/qa_civil_law_overview.py SITE_ROOT [EXPECTED_LIBRARY]')
    main(sys.argv[1],sys.argv[2] if len(sys.argv)==3 else '2026.07.29-18')
