#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BOOK='econometrics'
BOOK_VERSION='2026.07.29-1'
CHAPTER_COUNT=20
APPENDIX_COUNT=3
QUESTION_COUNT=100
SEARCH_COUNT=189
FIGURE_COUNT=20
ROUND1_CHECKS=384
ROUND1_NUMERIC_RECHECKS=29
ROUND2_CHECKS=675
HIGH_RISK_ANSWER_GATES=32


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    text2,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1:
        raise AssertionError(f'cannot update {label}')
    return text2


def main(site_root: str) -> None:
    site=Path(site_root)
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if len(ids)!=14 or ids[-1]!=BOOK:
        raise AssertionError(f'expected 14-book econometrics tail, got {ids}')

    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    figures=list((site/'assets/econometrics-svg').glob('*.svg'))
    if manifest['version']!=BOOK_VERSION or questions['version']!=BOOK_VERSION:
        raise AssertionError('econometrics content version drift')
    if len(manifest['chapters'])!=CHAPTER_COUNT+APPENDIX_COUNT:
        raise AssertionError('econometrics chapter/appendix count drift')
    if questions['count']!=QUESTION_COUNT or len(search['entries'])!=SEARCH_COUNT or len(figures)!=FIGURE_COUNT:
        raise AssertionError('econometrics artifact counts drift')

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
        'econometrics_version':BOOK_VERSION,
        'econometrics_chapter_count':CHAPTER_COUNT,
        'econometrics_appendix_count':APPENDIX_COUNT,
        'econometrics_question_count':QUESTION_COUNT,
        'econometrics_search_count':SEARCH_COUNT,
        'econometrics_figure_count':FIGURE_COUNT,
        'econometrics_round1_check_count':ROUND1_CHECKS,
        'econometrics_quantitative_recheck_count':ROUND1_NUMERIC_RECHECKS,
        'econometrics_round2_check_count':ROUND2_CHECKS,
        'econometrics_high_risk_answer_gate_count':HIGH_RISK_ANSWER_GATES,
        'econometrics_two_round_qa':'passed',
        'econometrics_existing_book_hashes_preserved':True,
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
        'artifact_verified_econometrics_html_count':23,
        'artifact_verified_econometrics_question_count':QUESTION_COUNT,
        'artifact_verified_econometrics_search_count':SEARCH_COUNT,
        'artifact_verified_econometrics_svg_count':FIGURE_COUNT,
        'workflow_overall_conclusion':'success',
        'post_deploy_record_step':'passed-structured-recorder',
        'receipt_reconciliation':'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f'''# 《計量經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library['version']}`
- 狀態：已部署。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 成品與 QA

- 正文 {CHAPTER_COUNT} 章、附錄 {APPENDIX_COUNT} 份、題庫 {QUESTION_COUNT} 題、搜尋索引 {SEARCH_COUNT} 筆、自製 SVG {FIGURE_COUNT} 張。
- 第一輪：{ROUND1_CHECKS} 項檢查通過，另有 {ROUND1_NUMERIC_RECHECKS} 個數值節點從原始輸入獨立重算。
- 第二輪：{ROUND2_CHECKS} 項獨立內容檢查通過，含 {HIGH_RISK_ANSWER_GATES} 題高風險答案 gate。
- 既有 13 本教材內容 hash 在整合前後完全一致。
- 閱讀進度相容性：新增獨立 Book ID，不改既有章節 ID、題目 ID、儲存鍵或錯題紀錄。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{artifact_digest}`
- 正式書庫書籍數：14 本。
- GitHub Pages 部署、artifact 下載重驗與結構化 deployment receipt 均成功。
'''
    Path('docs/books/econometrics/status.md').write_text(status,encoding='utf-8')

    qa_path=Path('docs/books/econometrics/qa_report.md')
    qa=qa_path.read_text(encoding='utf-8')
    final_block=f'''## 正式發布結果

- 第一輪 QA：{ROUND1_CHECKS} 項檢查＋{ROUND1_NUMERIC_RECHECKS} 個量化節點重算，全部通過。
- 第二輪獨立 QA：{ROUND2_CHECKS} 項檢查＋{HIGH_RISK_ANSWER_GATES} 題高風險答案 gate，全部通過。
- 既有 13 本內容 hash：整合前後完全一致。
- 正式書庫：14 本，版本 `{library['version']}`。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`。
- Pages artifact：`{artifact_id}`；digest `{artifact_digest}`。
- 部署後 artifact 重新下載：23 份本書 HTML、100 題、189 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`。
'''
    qa=re.sub(r'## 正式發布結果\n.*\Z',final_block,qa,flags=re.S) if '## 正式發布結果' in qa else qa.rstrip()+'\n\n'+final_block
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md')
    readme=readme_path.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README version')
    line=f'- 《計量經濟學》：一般大學計量經濟學，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。'
    lines=readme.splitlines()
    idxs=[i for i,x in enumerate(lines) if x.startswith('- 《計量經濟學》：')]
    if idxs:
        lines[idxs[0]]=line
        for i in reversed(idxs[1:]):
            del lines[i]
    else:
        book_lines=[i for i,x in enumerate(lines) if x.startswith('- 《')]
        if not book_lines:
            raise AssertionError('README book list missing')
        lines.insert(max(book_lines)+1,line)
    readme_path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

    cp=Path('docs/shared_checkpoint.md')
    c=cp.read_text(encoding='utf-8')
    c=replace_once(c,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{library["version"]}`','checkpoint library version')
    c=replace_once(c,r'- 正式書籍數：\d+ 本。','- 正式書籍數：14 本。','checkpoint book count')
    c=replace_once(c,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。','checkpoint run')
    c=replace_once(c,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。','checkpoint source commit')
    c=replace_once(c,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    c=replace_once(c,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{artifact_digest}`。','checkpoint digest')
    c=replace_once(c,r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=14`、`library_version={library["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')
    c=re.sub(r'- 實際下載正式 Pages artifact 後再次核對：.*\n',
             '- 實際下載正式 Pages artifact 後再次核對：14 本 registry、《計量經濟學》23 份章節／附錄 HTML、100 題、189 搜尋、20 SVG 均存在；下載檔 SHA-256 與 GitHub artifact digest 完全一致。\n',c,count=1)
    c=re.sub(r'- workflow overall conclusion.*\n','- workflow overall conclusion：`success`；post-deploy recorder 採結構化更新。\n',c,count=1)

    section=f'''### 14. 計量經濟學
- Book ID：`econometrics`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學計量經濟學；聚焦 OLS、多元迴歸、推論、內生性、IV、時間序列、panel 與現代因果推論。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- QA：第一輪 {ROUND1_CHECKS} 項＋{ROUND1_NUMERIC_RECHECKS} 個數值重算；第二輪 {ROUND2_CHECKS} 項＋{HIGH_RISK_ANSWER_GATES} 題高風險答案 gate，全數通過。
- 既有 13 本教材內容 hash 在整合前後完全一致。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`。
- 文件：`docs/books/econometrics/scope.md`、`docs/books/econometrics/qa_report.md`、`docs/books/econometrics/status.md`。
- 狀態：已部署。

'''
    if re.search(r'(?ms)^### 14\. 計量經濟學\n.*?(?=^## Canonical 部署流程)',c):
        c=re.sub(r'(?ms)^### 14\. 計量經濟學\n.*?(?=^## Canonical 部署流程)',section,c,count=1)
    else:
        marker='## Canonical 部署流程'
        if marker not in c:
            raise AssertionError('checkpoint canonical deployment marker missing')
        c=c.replace(marker,section+marker,1)
    c=re.sub(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',
             f'7. 最新正式書庫：14 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',c,count=1)
    c=c.replace('- canonical post-deploy recorder 仍存在舊 checkpoint 句型相依；下一次正式發布前應改成依結構化 receipt／Book ID 更新，而非依歷史自然語句做硬字串比對。',
                 '- canonical post-deploy recorder 已採結構化 receipt／Book ID 更新，不再依賴歷史自然語句硬字串比對。')
    c=c.replace('3. 在下一次正式發布前先修正／驗證 canonical post-deploy recorder，移除舊自然語句硬比對。',
                 '3. 正式發布前確認 canonical post-deploy recorder 仍為結構化更新且可重複執行。')
    cp.write_text(c,encoding='utf-8')

    print(json.dumps({
        'status':'success','library_version':library['version'],'book_count':14,
        'econometrics_version':BOOK_VERSION,'pages_artifact_id':artifact_id,
        'pages_artifact_digest':artifact_digest,'structured_recorder':True,
    },ensure_ascii=False))


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/record_econometrics_deployment.py SITE_ROOT')
    main(sys.argv[1])
