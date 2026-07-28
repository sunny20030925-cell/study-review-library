#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, sys
from collections import Counter
from pathlib import Path

BOOK='microeconomics'; VERSION='2026.07.29-1'
R1=R2=0

def ck(cond, msg, round_no=1):
    global R1,R2
    if not cond: raise AssertionError(msg)
    if round_no==1: R1+=1
    else: R2+=1

def main(root):
    site=Path(root); book=site/'books'/BOOK
    m=json.loads((book/'manifest.json').read_text(encoding='utf-8'))
    qj=json.loads((book/'questions.json').read_text(encoding='utf-8'))
    sj=json.loads((book/'search.json').read_text(encoding='utf-8'))
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    sw=(site/'sw.js').read_text(encoding='utf-8')
    qs=qj['items']

    # Round 1: generated-artifact, structure, links, mobile/offline assets.
    ck(m['id']==BOOK,'manifest id'); ck(m['title']=='個體經濟學','title'); ck(m['version']==VERSION,'version')
    chapters=[x for x in m['chapters'] if x['kind']=='chapter']; apps=[x for x in m['chapters'] if x['kind']=='appendix']
    ck(len(chapters)==20,'20 chapters'); ck(len(apps)==3,'3 appendices')
    ck([x['id'] for x in chapters]==[f'ch{i:02d}' for i in range(20)],'chapter ids')
    for x in m['chapters']:
        p=book/x['file']; ck(p.is_file(),f"missing {p}"); text=p.read_text(encoding='utf-8'); ck(len(text)>(800 if x['kind']=='chapter' else 500),f"short {p}")
        ck('<h2' in text,f"no headings {p}"); ck(not any(ord(c)<32 and c not in '\n\r\t' for c in text),f"control char {p}")
    ck(qj['version']==VERSION,'questions version'); ck(qj['count']==100,'question count field'); ck(len(qs)==100,'100 questions')
    ck(len({x['id'] for x in qs})==100,'unique q ids'); ck(Counter(x['chapterId'] for x in qs)=={f'ch{i:02d}':5 for i in range(20)},'5 questions/chapter')
    for x in qs:
        for key in ('id','chapterId','topic','difficulty','question','answer','explanation','source'):
            ck(bool(x.get(key)),f"{x.get('id')} missing {key}")
    entries=sj['entries']; ck(len(entries)==154,'search count 154')
    for e in entries:
        ck(e['chapterId'] in {x['id'] for x in m['chapters']},'search chapter id')
        ck(bool(e['title']) and bool(e['text']),'search content')
    figs=sorted((site/'assets/microeconomics-svg').glob('*.svg')); ck(len(figs)==20,'20 figures')
    for p in figs:
        s=p.read_text(encoding='utf-8'); ck('<title' in s,'svg title'); ck('<desc' in s,'svg desc'); ck('viewBox=' in s,'svg viewBox')
    books=[x['id'] for x in lib['books']]; ck(books.count(BOOK)==1,'library registration')
    expected_library_version=os.environ.get('EXPECTED_LIBRARY_VERSION')
    if expected_library_version:
        ck(lib['version']==expected_library_version,'library version')
    else:
        ck(bool(re.fullmatch(r'\d{4}\.\d{2}\.\d{2}-\d+',lib['version'])),'library version format')
    for path in [f'./books/{BOOK}/manifest.json',f'./books/{BOOK}/questions.json',f'./books/{BOOK}/search.json']:
        ck(path in sw,f'sw core {path}')
    for x in m['chapters']: ck(f'./books/{BOOK}/{x["file"]}' in sw,f'sw {x["file"]}')
    for p in figs: ck(f'./assets/microeconomics-svg/{p.name}' in sw,f'sw fig {p.name}')

    # Round 2: independent content gates after manual re-review of all 100 questions.
    alltext='\n'.join((book/x['file']).read_text(encoding='utf-8') for x in m['chapters'])
    required=[
      '完備性','遞移性','MRS_{xy}','Kuhn–Tucker','Marshallian demand','Roy 恆等式','Hicksian demand','Shephard 引理',
      'Slutsky 方程','WARP','補償變量','等價變量','跨期預算限制','期望效用','Arrow–Pratt','MRTS_{LK}',
      '成本最小化','Hotelling 引理','停業條件','完全競爭','Lerner 指數','Nash equilibrium','Cournot','Bertrand',
      'Stackelberg','MRP_L','買方獨占','Edgeworth box','Walras 法則','第一福利定理','第二福利定理','Pigouvian tax',
      'Samuelson condition','逆選擇','道德風險','signaling','screening','誘因相容限制'
    ]
    for t in required: ck(t in alltext,f'missing core concept {t}',2)
    formulas=[
      r'MRS_{xy}=\frac{p_x}{p_y}', r'x_i(p,m)=-\frac{\partial v/\partial p_i}{\partial v/\partial m}',
      r'h_i(p,\bar u)=\frac{\partial e(p,\bar u)}{\partial p_i}', r'e(p,v(p,m))=m',
      r'\frac{\partial x_i}{\partial p_j}=\frac{\partial h_i}{\partial p_j}-x_j\frac{\partial x_i}{\partial m}',
      r'c_1+\frac{c_2}{1+r}=y_1+\frac{y_2}{1+r}', r'EU=\sum_s \pi_s u(w_s)',
      r'A(w)=-u^{\prime\prime}(w)/u^{\prime}(w)', r'MRTS_{LK}=\frac{w}{r}',
      r'\frac{\partial C}{\partial w}=L^c', r'\partial\pi/\partial p=q^*',
      r'\frac{P-MC}{P}=\frac{1}{|\varepsilon_D|}', r'p\cdot z(p)=0', r'\sum_i MRS_i=MRT'
    ]
    for f in formulas: ck(f in alltext,f'missing formula {f}',2)
    forbidden=['WARP）要求：如果 A 曾在 B 可負擔時被選，就不能在另一個預算下 B 被選且 A 也可負擔，除非兩束其實等價',
               '獨占者不會在需求絕對彈性小於 1 的區段選內點最適，因為降低產量可同時提高營收並降低成本',
               '平滑內點且偏好正常時']
    for t in forbidden: ck(t not in alltext,f'obsolete text {t}',2)

    reviewed_snapshot='4e51b580dcf09d701518461c041d448e9fd551f08f58b422558da39225b16eac'
    canonical='\n'.join(f"{x['id']}|{x['question']}|{x['answer']}|{x['explanation']}" for x in qs)
    ck(hashlib.sha256(canonical.encode()).hexdigest()==reviewed_snapshot,'reviewed 100-question snapshot drift',2)
    numeric={
      'ch00-q02':'\\(x=6\\)。','ch01-q03':'3。','ch02-q02':'\\(x=30,\\ y=15\\)。',
      'ch08-q01':'15。','ch08-q02':'225。','ch08-q03':'25。','ch09-q02':'3。','ch10-q02':'0.5。',
      'ch11-q03':'NT$200。','ch13-q02':'\\(Q=40,\\ P=60\\)。','ch13-q03':'0.25。','ch15-q02':'20。',
      'ch15-q03':'30。','ch16-q02':'NT$240。','ch18-q02':'70。'
    }
    got={x['id']:x['answer'] for x in qs}
    ck(set(got)=={f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)},'all 100 reviewed question ids present',2)
    for qid,ans in numeric.items(): ck(got[qid]==ans,f'numeric recomputation {qid}',2)
    logic={
      'ch03-q05':'不可以。','ch05-q03':'不是。','ch05-q05':'不一定。','ch06-q02':'不符合。',
      'ch08-q05':'不會。','ch09-q05':'不必然。','ch11-q05':'不一定。','ch12-q05':'不能。',
      'ch13-q05':'不會。','ch14-q04':'不一定，典型囚犯困境不是。','ch15-q05':'不一定。','ch16-q05':'不必然。',
      'ch17-q05':'不是。','ch18-q05':'不是。','ch19-q05':'不一定。'
    }
    for qid,ans in logic.items(): ck(got[qid]==ans,f'logic review {qid}',2)

    print(f'MICRO_QA_OK round1={R1} round2={R2} questions=100 search=154 figures=20 library={lib["version"]}')

if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else '.')
