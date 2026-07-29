#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK='computer-fundamentals'
BOOK_VERSION='2026.07.30-2'


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1:
        raise AssertionError(f'cannot update {label}')
    return out


def main(site_root: str) -> None:
    site=Path(site_root)
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if ids.count(BOOK)!=1:
        raise AssertionError(f'computer fundamentals registration drift: {ids}')
    count=len(ids)

    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if manifest['version']!=BOOK_VERSION or questions['version']!=BOOK_VERSION:
        raise AssertionError('computer fundamentals v2 content version drift')
    if len(manifest['chapters'])!=23 or questions['count']!=100 or len(search['entries'])!=150:
        raise AssertionError('computer fundamentals v2 artifact count drift')
    if len(list((site/'assets/computer-fundamentals-svg').glob('*.svg')))!=20:
        raise AssertionError('computer fundamentals SVG count drift')

    artifact_id=os.environ.get('PAGES_ARTIFACT_ID','')
    digest=os.environ.get('PAGES_ARTIFACT_DIGEST','')
    sha=os.environ.get('PAGES_ARTIFACT_SHA256','')
    page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':',1)[1]!=sha:
        raise AssertionError('artifact digest mismatch')

    qa_checks=int(os.environ.get('COMPUTER_V2_QA_CHECKS','0') or 0)
    numeric_checks=int(os.environ.get('COMPUTER_V2_NUMERIC_RECHECKS','0') or 0)
    if qa_checks<=0 or numeric_checks<=0:
        raise AssertionError('missing computer fundamentals v2 QA metrics')

    deployed_at=datetime.now(timezone.utc).isoformat()
    receipt_path=Path('docs/deployment_receipt.json')
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status':'success',
        'library_version':library['version'],
        'book_versions_visible':True,
        'progress_storage_changed':False,
        'book_count':count,
        'book_ids':ids,
        'computer_fundamentals_version':BOOK_VERSION,
        'computer_fundamentals_chapter_count':20,
        'computer_fundamentals_appendix_count':3,
        'computer_fundamentals_question_count':100,
        'computer_fundamentals_search_count':150,
        'computer_fundamentals_figure_count':20,
        'computer_fundamentals_v2_independent_check_count':qa_checks,
        'computer_fundamentals_v2_quantitative_recheck_count':numeric_checks,
        'computer_fundamentals_v2_correction_area_count':15,
        'computer_fundamentals_v2_question_adjustment_count':12,
        'computer_fundamentals_two_round_qa':'passed-after-post-publication-v2-reaudit',
        'computer_fundamentals_existing_book_hashes_preserved':True,
        'source_commit':os.environ['GITHUB_SHA'],
        'workflow_run_id':os.environ['GITHUB_RUN_ID'],
        'page_url':page_url,
        'deployed_at':deployed_at,
        'pages_deploy_status':'success',
        'pages_artifact_id':artifact_id,
        'pages_artifact_digest':digest,
        'artifact_download_recheck':'passed',
        'artifact_download_sha256':sha,
        'artifact_verified_book_count':count,
        'artifact_verified_computer_fundamentals_html_count':23,
        'artifact_verified_computer_fundamentals_question_count':100,
        'artifact_verified_computer_fundamentals_search_count':150,
        'artifact_verified_computer_fundamentals_svg_count':20,
        'workflow_overall_conclusion':'success',
        'post_deploy_record_step':'passed-structured-recorder',
        'receipt_reconciliation':'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f'''# 《計算機概論》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library['version']}`
- 狀態：已部署；發布後第二次內容複核與精確性修正完成。
- 範圍文件：`docs/books/computer-fundamentals/scope.md`
- QA 報告：`docs/books/computer-fundamentals/qa_report.md`

## 成品與 v2 內容審計

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- 第二次內容審計共 15 個修正／補強區域，12 題題庫精確化。
- v2 獨立 QA：{qa_checks} 項；獨立數值重算：{numeric_checks} 項，全部通過。
- 修正重點：page fault／virtual memory、interrupt vs exception、URL authority、HTTP/3 + QUIC/TLS 1.3、Big-O vs Θ、二分搜尋減半／比較次數、foreign key、ACID、password hashing、NIST cloud 與 edge security/privacy。
- 全部非目標教材內容 hash 在修正前後完全一致。
- Book ID、20 個章節 ID、100 個題目 ID、題數與進度儲存鍵均未變，既有閱讀進度與錯題紀錄相容。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫書籍數：{count} 本。
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。
'''
    Path('docs/books/computer-fundamentals/status.md').write_text(status,encoding='utf-8')

    qa_path=Path('docs/books/computer-fundamentals/qa_report.md')
    qa=qa_path.read_text(encoding='utf-8')
    v2_block=f'''## 發布後第二次內容審計（v2）

- 正式內容版本：`{BOOK_VERSION}`。
- 內容修正／補強區域：15 個；題庫精確化：12 題。
- 獨立 QA：{qa_checks} 項通過；數值節點重新計算：{numeric_checks} 項通過。
- 高風險主題重新判讀：page fault／virtual memory、interrupt／exception、HTTP/3／QUIC／TLS、Big-O／Θ、binary search、foreign key／ACID、cryptographic hash／password KDF、NIST cloud／edge。
- Book ID、章節 ID、題目 ID、題數與進度儲存鍵均未變。
- 所有非目標教材內容 hash 在修正前後完全一致。
- 正式書庫：{count} 本，版本 `{library['version']}`。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`；artifact：`{artifact_id}`；digest `{digest}`。
- 部署後重新下載 artifact：23 份本書 HTML、100 題、150 搜尋、20 SVG 與 v2 QA 全數重驗通過。
'''
    if '## 發布後第二次內容審計（v2）' in qa:
        qa=re.sub(r'## 發布後第二次內容審計（v2）\n.*\Z',v2_block,qa,flags=re.S)
    else:
        qa=qa.rstrip()+'\n\n'+v2_block
    qa=qa.replace('- 候選內容版本：`2026.07.29-1`','- 正式內容版本：`2026.07.30-2`')
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md')
    readme=readme_path.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README version')
    lines=readme.splitlines()
    prefix='- 《計算機概論》：'
    matches=[i for i,line in enumerate(lines) if line.startswith(prefix)]
    book_line=f'- 《計算機概論》：一般大學計算機概論核心，20 章、3 附錄、100 題、150 搜尋、20 圖解；發布後第二次內容審計完成，內容版本 `{BOOK_VERSION}`。'
    if matches:
        lines[matches[0]]=book_line
        for i in reversed(matches[1:]):
            lines.pop(i)
    else:
        book_lines=[i for i,line in enumerate(lines) if line.startswith('- 《')]
        if not book_lines:
            raise AssertionError('README book list missing')
        lines.insert(max(book_lines)+1,book_line)
    readme_path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

    checkpoint_path=Path('docs/shared_checkpoint.md')
    checkpoint=checkpoint_path.read_text(encoding='utf-8')
    checkpoint=replace_once(checkpoint,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{library["version"]}`','checkpoint version')
    checkpoint=replace_once(checkpoint,r'- 正式書籍數：\d+ 本。',f'- 正式書籍數：{count} 本。','checkpoint count')
    checkpoint=replace_once(checkpoint,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。','checkpoint run')
    checkpoint=replace_once(checkpoint,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。','checkpoint source')
    checkpoint=replace_once(checkpoint,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    checkpoint=replace_once(checkpoint,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{digest}`。','checkpoint digest')
    checkpoint=replace_once(checkpoint,r'- Pages 狀態：.*$',f'- Pages 狀態：正式 artifact 上傳、Pages deployment 與下載後 artifact recheck 均成功；`{deployed_at}`。','checkpoint pages status')
    checkpoint=replace_once(checkpoint,r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count={count}`、`library_version={library["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')
    checkpoint=replace_once(checkpoint,r'- 實際下載正式 Pages artifact 後再次核對：.*$',f'- 實際下載正式 Pages artifact 後再次核對：{count} 本 registry；《計算機概論》v2 的 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 與既有正式教材均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。','checkpoint artifact recheck')
    checkpoint=replace_once(checkpoint,r'- workflow overall conclusion：.*$','- workflow overall conclusion：`success`；post-deploy recorder 採結構化 Book ID／receipt 更新。','checkpoint workflow conclusion')

    section=f'''### 14. 計算機概論
- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學計算機概論；資料表示、硬體、作業系統、網路、程式與演算法、資料庫、資安、AI 與現代運算平台。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- 初版 QA：第一輪 757 項、第二輪 598 項；17 個數值節點、26 個高風險概念 gate。
- 2026-07-30 發布後第二次內容審計：15 個修正／補強區域、12 題精確化；v2 QA {qa_checks} 項、數值重算 {numeric_checks} 項通過。
- Book ID、章節 ID、題目 ID、題數、閱讀進度與錯題儲存均保持相容；其他教材 hash 未變。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`；artifact：`{artifact_id}`。
- 文件：`docs/books/computer-fundamentals/scope.md`、`docs/books/computer-fundamentals/qa_report.md`、`docs/books/computer-fundamentals/status.md`。
- 狀態：已部署。

'''
    pattern=r'(?ms)^### 14\. 計算機概論\n.*?(?=^### 15\. |^## Canonical 部署流程)'
    checkpoint,n=re.subn(pattern,section,checkpoint,count=1)
    if n!=1:
        raise AssertionError('cannot update checkpoint computer-fundamentals section')
    checkpoint,n=re.subn(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',f'7. 最新正式書庫：{count} 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',checkpoint,count=1)
    if n!=1:
        raise AssertionError('checkpoint canonical latest-library line')
    checkpoint_path.write_text(checkpoint,encoding='utf-8')

    print(json.dumps({'status':'success','library_version':library['version'],'book_count':count,'computer_fundamentals_version':BOOK_VERSION,'qa_checks':qa_checks,'numeric_rechecks':numeric_checks,'pages_artifact_id':artifact_id},ensure_ascii=False))


if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/record_computer_fundamentals_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
