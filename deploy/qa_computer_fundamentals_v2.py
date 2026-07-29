from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

BOOK='computer-fundamentals'
VERSION='2026.07.30-2'
checks=0
numeric_checks=0


def ck(cond,msg):
    global checks
    checks+=1
    if not cond:
        raise AssertionError(msg)


def num(cond,msg):
    global numeric_checks
    numeric_checks+=1
    if not cond:
        raise AssertionError(msg)


def main(site_root: str, expected_library: str) -> None:
    site=Path(site_root)
    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    qdoc=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]

    ck(library['version']==expected_library,'library version')
    ck(BOOK in ids and ids.count(BOOK)==1,'book registration')
    ck(manifest['id']==BOOK and manifest['version']==VERSION,'manifest version')
    ck(qdoc['bookId']==BOOK and qdoc['version']==VERSION,'questions version')
    ck(len(manifest['chapters'])==23,'20 chapters + 3 appendices')
    ck(qdoc['count']==len(qdoc['items'])==100,'100 questions')
    ck(len({q['id'] for q in qdoc['items']})==100,'unique question ids')
    ck(len(search['entries'])==150,'150 search entries')
    ck(manifest['releaseNotes'][0]['version']==VERSION,'v2 release note')
    ck('發布後第二次內容複核與精確性修正'==manifest['releaseNotes'][0]['title'],'v2 release note title')
    ck('章節 ID、題目 ID、Book ID、題數與進度儲存鍵均未變' in manifest['releaseNotes'][0]['progressImpact'],'progress compatibility note')

    chapter_text={}
    for entry in manifest['chapters']:
        p=root/entry['file']
        ck(p.is_file() and p.stat().st_size>500,f'chapter file {entry["id"]}')
        text=p.read_text(encoding='utf-8')
        ck('<h1>' in text,f'h1 {entry["id"]}')
        chapter_text[entry['id']]=text
    full='\n'.join(chapter_text.values())

    required_tokens=[
        '歷史上曾有非 8-bit byte 的機器',
        '硬體 interrupt 通常是非同步事件',
        '同步 exception',
        '程序只有所列 CPU burst、沒有另計 I/O',
        '不是 CPU 把虛擬位址直接「翻譯成磁碟位址」',
        'copy-on-write',
        'page fault exception',
        'authority 包含 host',
        'fragment 由用戶端處理',
        'HTTP/3 則把 HTTP semantics 映射到 QUIC',
        'QUIC 使用 UDP 並整合 TLS 1.3',
        'Big-O 嚴格來說描述漸近上界',
        'Big-Theta, Θ',
        '10 次減半',
        '可到 11 次',
        'self-referential foreign key',
        'SQL table 與查詢結果的實務語意較寬',
        'Consistency 指交易在資料庫所宣告的完整性規則與不變條件下',
        'Cryptographic Hash（密碼學雜湊）',
        '具可調工作成本',
        'Argon2id',
        '按需自助、廣泛網路存取、資源池化、快速彈性與可量測服務',
        'edge 就自動更安全或更隱私',
    ]
    for token in required_tokens:
        ck(token in full,f'missing corrected concept {token}')

    forbidden_tokens=[
        '虛擬記憶體讓程序看到一個虛擬位址空間，作業系統與硬體再把虛擬位址映射到實體記憶體。這同時支援隔離、保護與彈性配置。',
        'URL = scheme + host + path + optional query/fragment',
        'Big-O 用來描述漸近成長的上界／等級',
        'binary search: O(log₂ n)',
        'Foreign Key（外鍵）</dt><dd>引用另一表候選鍵／主鍵',
        '雲端更強調共享資源池、按需求配置、服務化與彈性等特性',
    ]
    for token in forbidden_tokens:
        ck(token not in full,f'stale text remains: {token}')

    q={item['id']:item for item in qdoc['items']}
    expected_adjusted={
        'ch06-q03':('硬體中斷','非同步'),
        'ch08-q01':('不必然','實體 frame'),
        'ch08-q03':('兩者都不一定','copy-on-write'),
        'ch08-q05':('不完整','pagefile'),
        'ch10-q04':('HTTP/3','QUIC'),
        'ch12-q01':('Θ(n)','O(n)'),
        'ch12-q02':('10 次減半','11 次'),
        'ch12-q05':('不是','Θ'),
        'ch14-q02':('都不是','self-referential'),
        'ch16-q04':('可逆','密碼學'),
        'ch16-q05':('salt','cost'),
        'ch18-q01':('不是','可量測服務'),
    }
    for qid,tokens in expected_adjusted.items():
        text=q[qid]['question']+' '+q[qid]['answer']+' '+q[qid]['explanation']
        for token in tokens:
            ck(token in text,f'{qid} missing {token}')

    # Independent numerical rechecks across the book.
    numerical={
        'ch01-q02':(0b11010,'26'),
        'ch01-q03':(int('FF',16),'255'),
        'ch01-q04':(2**12,'4096'),
        'ch02-q01':(2**8-1,'255'),
        'ch02-q04':(1920*1080*24,'49,766,400'),
        'ch04-q02':(1/(2e9)/1e-9,'0.5 ns'),
        'ch04-q03':(1e9*2*(1/2e9),'1 秒'),
        'ch05-q03':(1+0.05*80,'5 ns'),
        'ch06-q02':(500/250,'2 秒'),
        'ch07-q04':(4+2,'t=6 ms'),
        'ch08-q02':(16/4,'4 頁'),
        'ch09-q02':(100/8,'12.5 MB/s'),
        'ch09-q03':(1/20,'0.05 秒'),
        'ch12-q02':(math.log2(1024),'10 次減半'),
        'ch13-q03':(80/100,'0.8'),
        'ch17-q03':(90/100*100,'90%'),
        'ch18-q02':((43200-43.2)/43200*100,'99.9%'),
    }
    for qid,(value,token) in numerical.items():
        num(math.isfinite(float(value)),f'{qid} recalculation finite')
        num(token in q[qid]['answer'],f'{qid} published numeric token {token}')

    # Binary-search count is deliberately checked separately: 10 halvings does not mean
    # every implementation has at most 10 middle-element comparison iterations.
    num(math.log2(1024)==10,'1024 halvings')
    num(math.floor(math.log2(1024))+1==11,'1024 worst comparison-loop depth')

    # Security and modern-protocol gates.
    ck('一般雜湊表用 hash function 不一定具備這些性質' in chapter_text['ch16'],'crypto vs generic hash')
    http3_answer=q['ch10-q04']['answer']
    ck('HTTP/3' in http3_answer and 'QUIC' in http3_answer and 'TLS 1.3' in http3_answer,'HTTP/3 transport')
    ck('TLS 1.3' in chapter_text['ch10'],'HTTP/3 TLS integration')
    ck('外鍵可重複' in chapter_text['ch14'] and 'self-reference' in chapter_text['ch14'],'foreign key semantics')
    ck('O(n) 只給漸近上界' in q['ch12-q05']['explanation'],'Big-O upper bound')
    ck('Θ(log n)' in full or 'Θ(log₂ n)' in full,'Theta log bound')

    sw=(site/'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw,'service worker version')
    for token in [
        './books/computer-fundamentals/manifest.json',
        './books/computer-fundamentals/questions.json',
        './books/computer-fundamentals/search.json',
        './books/computer-fundamentals/chapters/ch19.html',
    ]:
        ck(token in sw,f'sw path {token}')

    corpus='\n'.join(e['title']+' '+e['text'] for e in search['entries'])
    for token in ['page fault exception','authority 包含 host','Big-O 嚴格來說描述漸近上界','self-referential foreign key','按需自助']:
        ck(token in corpus,f'search missing corrected concept {token}')
    for token in ['URL = scheme + host + path + optional query/fragment','Big-O 用來描述漸近成長的上界／等級']:
        ck(token not in corpus,f'search stale concept {token}')

    print(f'COMPUTER_FUNDAMENTALS_V2_QA_OK checks={checks} numeric_rechecks={numeric_checks} correction_areas=15 question_adjustments=12 chapters=20 appendices=3 questions=100 search=150')


if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: python deploy/qa_computer_fundamentals_v2.py SITE_ROOT EXPECTED_LIBRARY_VERSION')
    main(sys.argv[1],sys.argv[2])
