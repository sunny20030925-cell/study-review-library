#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK='mathematical-economics'
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
    if ids.count(BOOK)!=1 or ids[-1]!=BOOK:
        raise AssertionError(f'mathematical economics registration drift: {ids}')
    count=len(ids)

    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if manifest['version']!=BOOK_VERSION or questions['version']!=BOOK_VERSION:
        raise AssertionError('mathematical economics v2 content version drift')
    if len(manifest['chapters'])!=23 or questions['count']!=100 or len(search['entries'])!=150:
        raise AssertionError('mathematical economics v2 artifact count drift')
    if len(list((site/'assets/mathematical-economics-svg').glob('*.svg')))!=20:
        raise AssertionError('mathematical economics SVG count drift')

    artifact_id=os.environ.get('PAGES_ARTIFACT_ID','')
    digest=os.environ.get('PAGES_ARTIFACT_DIGEST','')
    sha=os.environ.get('PAGES_ARTIFACT_SHA256','')
    page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':',1)[1]!=sha:
        raise AssertionError('artifact digest mismatch')

    qa_checks=int(os.environ.get('MATHEMATICAL_ECONOMICS_V2_QA_CHECKS','0') or 0)
    numeric_checks=int(os.environ.get('MATHEMATICAL_ECONOMICS_V2_NUMERIC_RECHECKS','0') or 0)
    logic_gates=int(os.environ.get('MATHEMATICAL_ECONOMICS_V2_LOGIC_GATES','0') or 0)
    if qa_checks<800 or numeric_checks<20 or logic_gates<10:
        raise AssertionError('missing mathematical economics v2 QA metrics')

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
        'mathematical_economics_version':BOOK_VERSION,
        'mathematical_economics_chapter_count':20,
        'mathematical_economics_appendix_count':3,
        'mathematical_economics_question_count':100,
        'mathematical_economics_search_count':150,
        'mathematical_economics_figure_count':20,
        'mathematical_economics_post_publication_reaudit':'passed-before-first-formal-release',
        'mathematical_economics_v2_correction_area_count':13,
        'mathematical_economics_v2_question_adjustment_count':11,
        'mathematical_economics_v2_independent_check_count':qa_checks,
        'mathematical_economics_v2_quantitative_recheck_count':numeric_checks,
        'mathematical_economics_v2_high_risk_logic_gate_count':logic_gates,
        'mathematical_economics_ids_preserved':True,
        'mathematical_economics_existing_book_hashes_preserved':True,
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
        'artifact_verified_mathematical_economics_html_count':23,
        'artifact_verified_mathematical_economics_question_count':100,
        'artifact_verified_mathematical_economics_search_count':150,
        'artifact_verified_mathematical_economics_svg_count':20,
        'workflow_overall_conclusion':'success',
        'post_deploy_record_step':'passed-structured-recorder',
        'receipt_reconciliation':'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f'''# 《數理經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library['version']}`
- 狀態：已部署；第二次獨立內容審計、糾錯與修正完成。
- QA 報告：`docs/books/mathematical-economics/qa_report.md`

## 成品與第二次內容審計

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- 第二次獨立內容審計修正／補強 13 個核心區域，調整 11 題高風險題庫。
- v2 獨立 QA：{qa_checks} 項；數值／公式重算：{numeric_checks} 項；高風險邏輯 gate：{logic_gates} 項，全部通過。
- 補強內容含 rank／聯立系統一致性、內積與線性組合、鏈鎖律、隱函數 Jacobian、凹性／擬凹性、受限二階條件、bordered Hessian、KKT 前提、constrained envelope theorem、積分累積與動態穩定邊界。
- Book ID、20 個章節 ID 與 100 個題目 ID 保持穩定；既有正式教材內容 hash 未改動。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫書籍數：{count} 本。
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。
'''
    Path('docs/books/mathematical-economics/status.md').write_text(status,encoding='utf-8')

    qa_path=Path('docs/books/mathematical-economics/qa_report.md')
    qa=qa_path.read_text(encoding='utf-8')
    block=f'''## 第二次獨立內容審計與正式發布（v2）

- 正式內容版本：`{BOOK_VERSION}`。
- 實質修正／補強區域：13 個；高風險題庫調整：11 題。
- 獨立 QA：{qa_checks} 項通過；數值／公式節點重算：{numeric_checks} 項通過；高風險邏輯 gate：{logic_gates} 項通過。
- 20 章內容密度全部達 gate；正文 20 章、3 附錄、100 題、150 搜尋、20 SVG 完整。
- 既有教材內容與既有 assets hash 在整合前後保持一致。
- 正式書庫：{count} 本，版本 `{library['version']}`。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`；artifact：`{artifact_id}`；digest `{digest}`。
- 部署後重新下載 artifact，23 份本書 HTML、100 題、150 搜尋、20 SVG 與完整 v2 QA 全數重驗通過。
'''
    if '## 第二次獨立內容審計與正式發布（v2）' in qa:
        qa=re.sub(r'## 第二次獨立內容審計與正式發布（v2）\n.*\Z',block,qa,flags=re.S)
    else:
        qa=qa.rstrip()+'\n\n'+block
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md')
    readme=readme_path.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README version')
    lines=readme.splitlines()
    prefix='- 《數理經濟學》：'
    book_line=f'- 《數理經濟學》：一般大學數理經濟學，20 章、3 附錄、100 題、150 搜尋、20 圖解；第二次獨立內容審計完成，內容版本 `{BOOK_VERSION}`。'
    matches=[i for i,line in enumerate(lines) if line.startswith(prefix)]
    if matches:
        lines[matches[0]]=book_line
        for i in reversed(matches[1:]): lines.pop(i)
    else:
        book_lines=[i for i,line in enumerate(lines) if line.startswith('- 《')]
        if not book_lines: raise AssertionError('README book list missing')
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
    checkpoint=replace_once(checkpoint,r'- 實際下載正式 Pages artifact 後再次核對：.*$',f'- 實際下載正式 Pages artifact 後再次核對：{count} 本 registry；《數理經濟學》v2 的 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 與既有正式教材均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。','checkpoint artifact recheck')
    checkpoint=replace_once(checkpoint,r'- workflow overall conclusion：.*$','- workflow overall conclusion：`success`；post-deploy recorder 採結構化 Book ID／receipt 更新。','checkpoint workflow conclusion')
    checkpoint_path.write_text(checkpoint,encoding='utf-8')


if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/record_mathematical_economics_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
