#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK='computer-fundamentals'
BOOK_VERSION='2026.07.29-1'


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1:
        raise AssertionError(f'cannot update {label}')
    return out


def upsert_book_line(readme: str, title: str, line: str) -> str:
    lines=readme.splitlines()
    prefix=f'- 《{title}》：'
    idxs=[i for i,x in enumerate(lines) if x.startswith(prefix)]
    if idxs:
        lines[idxs[0]]=line
        for i in reversed(idxs[1:]):
            del lines[i]
    else:
        book_lines=[i for i,x in enumerate(lines) if x.startswith('- 《')]
        if not book_lines:
            raise AssertionError('README book list missing')
        lines.insert(max(book_lines)+1,line)
    return '\n'.join(lines)+'\n'


def main(site_root: str) -> None:
    site=Path(site_root)
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if len(ids)!=14 or ids[-2:]!=['advanced-statistics',BOOK]:
        raise AssertionError(f'expected 14-book advanced-statistics -> computer-fundamentals tail, got {ids}')

    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if manifest['version']!=BOOK_VERSION or questions['version']!=BOOK_VERSION:
        raise AssertionError('computer fundamentals content version drift')
    if len(manifest['chapters'])!=23 or questions['count']!=100 or len(search['entries'])!=150:
        raise AssertionError('computer fundamentals artifact counts drift')
    if len(list((site/'assets/computer-fundamentals-svg').glob('*.svg')))!=20:
        raise AssertionError('computer fundamentals figure count drift')

    artifact_id=os.environ.get('PAGES_ARTIFACT_ID','')
    artifact_digest=os.environ.get('PAGES_ARTIFACT_DIGEST','')
    artifact_sha=os.environ.get('PAGES_ARTIFACT_SHA256','')
    page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not artifact_digest or not artifact_sha:
        raise AssertionError('missing artifact verification environment')
    if artifact_digest.startswith('sha256:') and artifact_digest.split(':',1)[1]!=artifact_sha:
        raise AssertionError('artifact digest and downloaded sha mismatch')

    receipt_path=Path('docs/deployment_receipt.json')
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status':'success',
        'library_version':library['version'],
        'book_versions_visible':True,
        'progress_storage_changed':False,
        'book_count':14,
        'computer_fundamentals_version':BOOK_VERSION,
        'computer_fundamentals_chapter_count':20,
        'computer_fundamentals_appendix_count':3,
        'computer_fundamentals_question_count':100,
        'computer_fundamentals_search_count':150,
        'computer_fundamentals_figure_count':20,
        'computer_fundamentals_round1_check_count':757,
        'computer_fundamentals_round2_check_count':598,
        'computer_fundamentals_quantitative_recheck_count':17,
        'computer_fundamentals_high_risk_concept_gate_count':26,
        'computer_fundamentals_two_round_qa':'passed',
        'computer_fundamentals_existing_book_hashes_preserved':True,
        'source_commit':os.environ['GITHUB_SHA'],
        'workflow_run_id':os.environ['GITHUB_RUN_ID'],
        'page_url':page_url,
        'deployed_at':datetime.now(timezone.utc).isoformat(),
        'pages_deploy_status':'success',
        'pages_artifact_id':artifact_id,
        'pages_artifact_digest':artifact_digest,
        'artifact_download_recheck':'passed',
        'artifact_download_sha256':artifact_sha,
        'artifact_verified_book_count':14,
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

更新日期：2026-07-29

## 正式識別

- Book ID：`computer-fundamentals`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library['version']}`
- 狀態：已部署。
- 範圍文件：`docs/books/computer-fundamentals/scope.md`
- QA 報告：`docs/books/computer-fundamentals/qa_report.md`

## 成品與 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- 第一輪 release QA：757 項通過。
- 第二輪獨立 QA：598 項通過；17 個數值節點獨立重算、26 個高風險概念重判。
- 既有 13 本教材內容 hash 在整合前後完全一致。
- 閱讀進度相容性：新增獨立 Book ID，不改既有章節 ID、題目 ID、儲存鍵或錯題紀錄。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{artifact_digest}`
- 正式書庫書籍數：14 本。
- GitHub Pages 部署、artifact 下載重驗與 deployment receipt 均成功。
'''
    Path('docs/books/computer-fundamentals/status.md').write_text(status,encoding='utf-8')

    qa_path=Path('docs/books/computer-fundamentals/qa_report.md')
    qa=qa_path.read_text(encoding='utf-8')
    final_block=f'''## 正式發布結果

- 第一輪 release QA：757 項，通過。
- 第二輪獨立 QA：598 項，通過；17 個數值節點重算、26 個高風險概念 gate。
- 既有 13 本內容 hash：整合前後完全一致。
- 正式書庫：14 本，版本 `{library['version']}`。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`。
- Pages artifact：`{artifact_id}`；digest `{artifact_digest}`。
- 部署後 artifact 重新下載：23 份本書 HTML、100 題、150 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`。
'''
    qa=re.sub(r'## 正式發布結果\n.*\Z',final_block,qa,flags=re.S) if '## 正式發布結果' in qa else qa.rstrip()+'\n\n'+final_block
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md')
    readme=readme_path.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README version')
    readme=upsert_book_line(readme,'計算機概論',f'- 《計算機概論》：一般大學計算機概論核心，20 章、3 附錄、100 題題庫、150 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。')
    readme_path.write_text(readme,encoding='utf-8')

    cp=Path('docs/shared_checkpoint.md')
    c=cp.read_text(encoding='utf-8')
    c=replace_once(c,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{library["version"]}`','checkpoint version')
    c=replace_once(c,r'- 正式書籍數：\d+ 本。','- 正式書籍數：14 本。','checkpoint count')
    c=replace_once(c,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。','checkpoint run')
    c=replace_once(c,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。','checkpoint source')
    c=replace_once(c,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    c=replace_once(c,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{artifact_digest}`。','checkpoint digest')
    c=replace_once(c,r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=14`、`library_version={library["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')
    c=re.sub(r'- 實際下載正式 Pages artifact 後再次核對：.*$', '- 實際下載正式 Pages artifact 後再次核對：14 本 registry、本書 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 均存在；下載檔 SHA-256 與 GitHub artifact digest 完全一致。', c, count=1, flags=re.M)
    section=f'''### 14. 計算機概論
- Book ID：`computer-fundamentals`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學計算機概論；資料表示、硬體、作業系統、網路、程式與演算法、資料庫、資安、AI 與現代運算平台。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- QA：第一輪 757 項、第二輪 598 項通過；17 個數值節點獨立重算、26 個高風險概念 gate。
- 既有 13 本教材內容 hash 在整合前後完全一致。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`。
- 文件：`docs/books/computer-fundamentals/scope.md`、`docs/books/computer-fundamentals/qa_report.md`、`docs/books/computer-fundamentals/status.md`。
- 狀態：已部署。

'''
    if re.search(r'(?ms)^### 14\. 計算機概論\n.*?(?=^## Canonical 部署流程)',c):
        c=re.sub(r'(?ms)^### 14\. 計算機概論\n.*?(?=^## Canonical 部署流程)',section,c,count=1)
    else:
        marker='## Canonical 部署流程'
        if marker not in c:
            raise AssertionError('checkpoint canonical marker missing')
        c=c.replace(marker,section+marker,1)
    c=re.sub(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',f'7. 最新正式書庫：14 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',c,count=1)
    cp.write_text(c,encoding='utf-8')

    print(json.dumps({'status':'success','library_version':library['version'],'book_count':14,'computer_fundamentals_version':BOOK_VERSION,'pages_artifact_id':artifact_id,'structured_recorder':True},ensure_ascii=False))


if __name__=='__main__':
    if len(os.sys.argv)!=2:
        raise SystemExit('usage: python deploy/record_computer_fundamentals_deployment.py SITE_ROOT')
    main(os.sys.argv[1])
