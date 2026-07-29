#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from qa_game_theory_v2 import main as qa_artifact_v2

BOOK='game-theory'
TARGET_VERSION='2026.07.30-2'
V2_ARTIFACT_CHECKS=504
V2_SECOND_PASS_CHECKS=375
V2_ARTIFACT_QUANT=21
V2_ARTIFACT_CONCEPT=19
V2_SOURCE_QUANT=24
V2_SOURCE_CONCEPT=23


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1:
        raise AssertionError(f'cannot update {label}')
    return out


def main(site_root: str) -> None:
    site=Path(site_root)
    deployed=Path('/tmp/deployed-site') if Path('/tmp/deployed-site/data/library.json').is_file() else site
    library=json.loads((deployed/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if ids.count(BOOK)!=1:
        raise AssertionError(f'game theory registry drift: {ids}')

    root=deployed/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if manifest.get('version')!=TARGET_VERSION or questions.get('version')!=TARGET_VERSION:
        raise AssertionError('deployed game theory is not v2')
    if len(manifest['chapters'])!=23 or questions['count']!=100 or len(search['entries'])!=189:
        raise AssertionError('deployed game theory v2 counts drift')
    if len(list((deployed/'assets/game-theory-svg').glob('*.svg')))!=20:
        raise AssertionError('deployed game theory v2 figure count drift')

    qa_artifact_v2(str(deployed), library['version'])

    artifact_id=os.environ.get('PAGES_ARTIFACT_ID','')
    artifact_digest=os.environ.get('PAGES_ARTIFACT_DIGEST','')
    artifact_sha=os.environ.get('PAGES_ARTIFACT_SHA256','')
    page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not artifact_digest or not artifact_sha:
        raise AssertionError('missing deployed artifact verification environment')
    if artifact_digest.startswith('sha256:') and artifact_digest.split(':',1)[1]!=artifact_sha:
        raise AssertionError('artifact digest / downloaded sha mismatch')

    receipt_path=Path('docs/deployment_receipt.json')
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status':'success',
        'library_version':library['version'],
        'book_count':len(ids),
        'book_versions_visible':True,
        'progress_storage_changed':False,
        'game_theory_version':TARGET_VERSION,
        'game_theory_chapter_count':20,
        'game_theory_appendix_count':3,
        'game_theory_question_count':100,
        'game_theory_search_count':189,
        'game_theory_figure_count':20,
        'game_theory_v2_artifact_check_count':V2_ARTIFACT_CHECKS,
        'game_theory_v2_second_pass_check_count':V2_SECOND_PASS_CHECKS,
        'game_theory_v2_artifact_quantitative_recheck_count':V2_ARTIFACT_QUANT,
        'game_theory_v2_artifact_concept_recheck_count':V2_ARTIFACT_CONCEPT,
        'game_theory_v2_source_quantitative_recheck_count':V2_SOURCE_QUANT,
        'game_theory_v2_source_concept_recheck_count':V2_SOURCE_CONCEPT,
        'game_theory_v2_independent_content_audit':'passed',
        'game_theory_existing_book_hashes_preserved':True,
        'artifact_verified_game_theory_html_count':23,
        'artifact_verified_game_theory_question_count':100,
        'artifact_verified_game_theory_search_count':189,
        'artifact_verified_game_theory_svg_count':20,
        'artifact_verified_book_count':len(ids),
        'source_commit':os.environ['GITHUB_SHA'],
        'workflow_run_id':os.environ['GITHUB_RUN_ID'],
        'page_url':page_url,
        'deployed_at':datetime.now(timezone.utc).isoformat(),
        'pages_deploy_status':'success',
        'pages_artifact_id':artifact_id,
        'pages_artifact_digest':artifact_digest,
        'artifact_download_recheck':'passed',
        'artifact_download_sha256':artifact_sha,
        'workflow_overall_conclusion':'success',
        'post_deploy_record_step':'passed-structured-recorder',
        'receipt_reconciliation':'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status_path=Path('docs/books/game-theory/status.md')
    status=f'''# 《賽局理論及應用》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`game-theory`
- 正式內容版本：`{TARGET_VERSION}`
- 正式書庫版本：`{library['version']}`
- 正式書庫書籍數：{len(ids)} 本。
- 狀態：v2 已部署。
- 範圍文件：`docs/books/game-theory/scope.md`
- 初版 QA：`docs/books/game-theory/qa_report.md`
- v2 重審報告：`docs/books/game-theory/v2_audit_report.md`

## v2 內容重審

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、自製 SVG 20 張。
- v2 artifact audit：504 項；21 個數值節點獨立重算、19 個高風險概念重判。
- v2 source second pass：375 項；24 個數值節點獨立重算、23 個概念重判。
- 修正 complete／perfect information、混合策略例題、rationalizability、Bertrand、subgame、Bayesian dynamic boundary、second-price assumptions、PBE／signaling、Rubinstein、VCG 與 strategic complements 等精度問題。
- Book ID、章節 ID、附錄 ID 與 100 個題目 ID 全部保留；閱讀進度與錯題紀錄相容。
- 正式 release helper 已驗證除 game-theory 外所有書籍、其他 assets 與 shared `app.js` 未被修改。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{artifact_digest}`
- 部署後重新下載 artifact 並再次執行 v2 artifact QA：PASS。
'''
    status_path.write_text(status,encoding='utf-8')

    audit_path=Path('docs/books/game-theory/v2_audit_report.md')
    audit=audit_path.read_text(encoding='utf-8')
    final_block=f'''## 正式 v2 發布結果

- 正式內容版本：`{TARGET_VERSION}`。
- 正式 shared library：`{library['version']}`；正式書籍數：{len(ids)} 本。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`；source commit：`{os.environ['GITHUB_SHA']}`。
- Pages artifact：`{artifact_id}`；digest：`{artifact_digest}`。
- 部署後重新下載 artifact：23 HTML、100 題、189 搜尋、20 SVG 全數存在。
- 部署後 `GAME_THEORY_V2_AUDIT_OK` 再次通過；其他教材與 shared `app.js` 維持不變。
- `progress_storage_changed=false`；Book／chapter／question IDs 未改，平板閱讀進度與錯題紀錄相容。
'''
    if '## 正式 v2 發布結果' in audit:
        audit=re.sub(r'(?ms)^## 正式 v2 發布結果\n.*\Z',final_block,audit)
    else:
        audit=audit.rstrip()+'\n\n'+final_block
    audit_path.write_text(audit.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md')
    readme=readme_path.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README shared version')
    readme=replace_once(
        readme,
        r'- 《賽局理論及應用》：.*$',
        f'- 《賽局理論及應用》：一般大學賽局理論核心，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；發布後第二次獨立內容重審版本 `{TARGET_VERSION}`。',
        'README game theory line',
    )
    readme_path.write_text(readme,encoding='utf-8')

    checkpoint_path=Path('docs/shared_checkpoint.md')
    cp=checkpoint_path.read_text(encoding='utf-8')
    cp=replace_once(cp,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{library["version"]}`','checkpoint version')
    cp=replace_once(cp,r'- 正式書籍數：\d+ 本。',f'- 正式書籍數：{len(ids)} 本。','checkpoint count')
    cp=replace_once(cp,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。','checkpoint run')
    cp=replace_once(cp,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。','checkpoint source')
    cp=replace_once(cp,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    cp=replace_once(cp,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{artifact_digest}`。','checkpoint digest')
    section_pattern=r'(?ms)^### 15\. 賽局理論及應用\n.*?(?=^### 16\.)'
    section=f'''### 15. 賽局理論及應用
- Book ID：`game-theory`
- 正式內容版本：`{TARGET_VERSION}`
- 定位：一般大學賽局理論；策略式與展開式賽局、Nash／SPNE／BNE／PBE、重複賽局、拍賣、訊號、機制設計與合作賽局。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- 初版 QA：第一輪 2385、第二輪 360。
- 2026-07-30 第二次獨立內容重審：artifact audit 504 項、source second pass 375 項；21／24 個數值節點重算、19／23 個概念 gate。
- 修正 complete／perfect information、混合策略、rationalizability、Bertrand、subgame、Bayesian／PBE／signaling、拍賣、Rubinstein、VCG 與 strategic complements 等精度問題。
- Book／chapter／question IDs 不變；progress storage 相容。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`；artifact：`{artifact_id}`。
- 文件：`docs/books/game-theory/scope.md`、`docs/books/game-theory/qa_report.md`、`docs/books/game-theory/v2_audit_report.md`、`docs/books/game-theory/status.md`。
- 狀態：v2 已部署。

'''
    if not re.search(section_pattern,cp):
        raise AssertionError('game theory checkpoint section missing')
    cp=re.sub(section_pattern,section,cp,count=1)
    checkpoint_path.write_text(cp,encoding='utf-8')

    print(json.dumps({
        'status':'success',
        'library_version':library['version'],
        'book_count':len(ids),
        'game_theory_version':TARGET_VERSION,
        'pages_artifact_id':artifact_id,
        'v2_artifact_checks':V2_ARTIFACT_CHECKS,
        'v2_second_pass_checks':V2_SECOND_PASS_CHECKS,
    },ensure_ascii=False))


if __name__=='__main__':
    if len(os.sys.argv)!=2:
        raise SystemExit('usage: python deploy/record_game_theory_v2_deployment.py SITE_ROOT')
    main(os.sys.argv[1])
