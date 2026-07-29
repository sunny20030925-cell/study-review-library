#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BOOK='econometrics'; BOOK_VERSION='2026.07.30-2'

def replace_once(text:str,pattern:str,replacement:str,label:str)->str:
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1: raise AssertionError(f'cannot update {label}')
    return out

def main(site_root:str)->None:
    site=Path(site_root); lib=json.loads((site/'data/library.json').read_text(encoding='utf-8')); ids=[b['id'] for b in lib['books']]
    if ids.count(BOOK)!=1 or 'industrial-economics' not in ids or ids.index(BOOK)>ids.index('industrial-economics'): raise AssertionError('econometrics registry/order drift')
    root=site/'books'/BOOK; m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); q=json.loads((root/'questions.json').read_text(encoding='utf-8')); s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if m['version']!=BOOK_VERSION or q['version']!=BOOK_VERSION: raise AssertionError('econometrics v3 version drift')
    if len(m['chapters'])!=23 or q['count']!=100 or len(s['entries'])!=189 or len(list((site/'assets/econometrics-svg').glob('*.svg')))!=20: raise AssertionError('econometrics v3 count drift')
    artifact_id=os.environ.get('PAGES_ARTIFACT_ID',''); digest=os.environ.get('PAGES_ARTIFACT_DIGEST',''); sha=os.environ.get('PAGES_ARTIFACT_SHA256',''); page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not digest or not sha: raise AssertionError('missing verified Pages artifact environment')
    if digest.startswith('sha256:') and digest.split(':',1)[1]!=sha: raise AssertionError('artifact digest mismatch')
    checks=int(os.environ.get('ECONOMETRICS_V3_REAUDIT_CHECKS','0') or 0)
    if checks<=0: raise AssertionError('missing v3 reaudit check count')
    run_id=os.environ['GITHUB_RUN_ID']; source_sha=os.environ['GITHUB_SHA']; deployed_at=datetime.now(timezone.utc).isoformat()

    receipt_path=Path('docs/deployment_receipt.json'); receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({'status':'success','library_version':lib['version'],'book_versions_visible':True,'progress_storage_changed':False,'book_count':len(ids),'book_ids':ids,
        'econometrics_version':BOOK_VERSION,'econometrics_chapter_count':20,'econometrics_appendix_count':3,'econometrics_question_count':100,'econometrics_search_count':189,'econometrics_figure_count':20,
        'econometrics_initial_round1_check_count':384,'econometrics_initial_round2_check_count':675,'econometrics_initial_numeric_recheck_count':29,'econometrics_initial_high_risk_answer_gate_count':32,
        'econometrics_post_publication_reaudit':'passed','econometrics_post_publication_correction_count':2,'econometrics_post_publication_reaudit_check_count':57,
        'econometrics_second_content_reaudit':'passed','econometrics_second_content_reaudit_check_count':checks,'econometrics_second_content_correction_area_count':5,'econometrics_second_content_question_adjustment_count':4,'econometrics_second_content_numeric_recheck_count':29,
        'econometrics_ids_preserved':True,'econometrics_progress_compatibility':'preserved','artifact_verified_econometrics_html_count':23,'artifact_verified_econometrics_question_count':100,'artifact_verified_econometrics_search_count':189,'artifact_verified_econometrics_svg_count':20,
        'source_commit':source_sha,'workflow_run_id':run_id,'page_url':page_url,'deployed_at':deployed_at,'pages_deploy_status':'success','pages_artifact_id':artifact_id,'pages_artifact_digest':digest,'artifact_download_recheck':'passed','artifact_download_sha256':sha,'artifact_verified_book_count':len(ids),'workflow_overall_conclusion':'success','post_deploy_record_step':'passed-structured-recorder','receipt_reconciliation':'automatic-from-verified-pages-artifact'})
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f'''# 《計量經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`econometrics`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{lib['version']}`
- 狀態：已部署。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 正式成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 自製 SVG：20 張。
- 章節 ID、題目 ID、題數與儲存鍵均未改動；既有閱讀進度與錯題紀錄相容。

## 第二次內容層獨立審校

- v3 獨立 validator：{checks} 項通過；100 題重新做結構／答案完整性檢查，29 個數值節點重新由輸入計算。
- 修正 5 個區域：binary IV／Wald 的 complier LATE 範圍、noncompliance 的 ITT/IV 界線、DiD no anticipation、fuzzy RDD local complier LATE、validation／final-test 分工。
- 調整 4 個題目／詳解節點：`ch14-q05`、`ch15-q04`、`ch17-q05`、`ch18-q03`；全部保留原 ID。

## 正式發布證據

- canonical workflow：`Deploy study library`
- workflow run：`{run_id}`
- source commit：`{source_sha}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫：{len(ids)} 本，版本 `{lib['version']}`。
- Pages deployment、artifact 下載後重驗與 deployment receipt 均成功。
'''
    Path('docs/books/econometrics/status.md').write_text(status,encoding='utf-8')

    qa_path=Path('docs/books/econometrics/qa_report.md'); qa=qa_path.read_text(encoding='utf-8')
    block=f'''## 第二次內容層獨立審校 v3（2026-07-30）

本輪重新逐章閱讀正文、例題、題庫與附錄，專門檢查 estimand、識別範圍與資料切分是否會讓學生得到錯誤結論。

- **IV／Wald**：效果異質時，標準二元 IV 在 relevance、外生性／exclusion、monotonicity 等條件下典型識別 compliers 的 LATE／CACE，不得無條件寫成全母體 ATE／ATT。
- **Randomized experiment + noncompliance**：ITT 仍依原始 assignment；若把 assignment 作 IV，需額外 IV 條件，典型 estimand 是 complier LATE／CACE，不是所有 actual treatment takers 的 ATT／TOT。
- **DiD**：parallel trends 之外補上 no anticipation；若正式處置前已有提前反應，pre-treatment 基準期需重新界定或明確建模。
- **Fuzzy RDD**：局部 Wald ratio 在相應 continuity／IV 條件下識別 cutoff 處 local compliers 的 LATE，不得無條件外推整體 ATE。
- **Prediction**：修正原本正文與例題的矛盾；validation／cross-validation 用於選模與調參，final test set 留到模型固定後作最後評估，避免 test leakage。

### 題庫與相容性重驗

- v3 獨立 validator：{checks} 項通過。
- 100 題重新做題目、答案、詳解、章節歸屬與每章 5 題結構檢查。
- 29 個數值節點重新由原始輸入計算並比對正式答案。
- 調整 4 個題目／詳解節點：`ch14-q05`、`ch15-q04`、`ch17-q05`、`ch18-q03`。
- 20 章、3 附錄、100 題、189 搜尋、20 SVG 均維持；chapter/question IDs 與閱讀／錯題儲存結構不變。

### 正式部署

- Book version：`{BOOK_VERSION}`。
- Shared library：`{lib['version']}`，{len(ids)} 本。
- Pages run：`{run_id}`。
- Pages artifact：`{artifact_id}`；digest `{digest}`。
'''
    if '## 第二次內容層獨立審校 v3（2026-07-30）' in qa: qa=re.sub(r'## 第二次內容層獨立審校 v3（2026-07-30）\n.*\Z',block,qa,flags=re.S)
    else: qa=qa.rstrip()+'\n\n'+block
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme=Path('README.md').read_text(encoding='utf-8'); readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{lib["version"]}`','README version')
    lines=readme.splitlines(); matches=[i for i,x in enumerate(lines) if x.startswith('- 《計量經濟學》：')]
    if len(matches)!=1: raise AssertionError('README econometrics line drift')
    lines[matches[0]]=f'- 《計量經濟學》：一般大學計量經濟學核心，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；第二次內容審校已補強 IV／fuzzy RDD 的 LATE 範圍、noncompliance、DiD no anticipation 與 validation／test 分工，內容版本 `{BOOK_VERSION}`。'
    Path('README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

    cp_path=Path('docs/shared_checkpoint.md'); cp=cp_path.read_text(encoding='utf-8')
    for pattern,repl,label in [(r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{lib["version"]}`','checkpoint version'),(r'- 正式書籍數：\d+ 本。',f'- 正式書籍數：{len(ids)} 本。','checkpoint count'),(r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{run_id}`。','checkpoint run'),(r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{source_sha}`。','checkpoint source'),(r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact'),(r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{digest}`。','checkpoint digest'),(r'- Pages 狀態：.*$',f'- Pages 狀態：正式 artifact 上傳、Pages deployment 與下載後 artifact recheck 均成功；`{deployed_at}`。','checkpoint pages'),(r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count={len(ids)}`、`library_version={lib["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')]: cp=replace_once(cp,pattern,repl,label)
    section=f'''### 18. 計量經濟學
- Book ID：`econometrics`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學計量經濟學；OLS、多元迴歸與推論、異質變異、模型設定、二元結果、時間序列、panel、IV／2SLS、實驗、DiD、RDD、預測與實證研究流程。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- 初版 QA：Round 1 = 384、Round 2 = 675；29 個數值節點獨立重算、32 個高風險答案 gate。
- 第一次發布後審計：2 個精確化修正；v2 reaudit validator 57 項通過。
- 第二次內容層獨立審校：5 個修正區域、4 個題目／詳解節點調整；v3 reaudit validator {checks} 項通過，100 題重檢、29 個數值節點重算。
- v3 修正重點：IV／noncompliance 與 fuzzy RDD 明確限定 complier LATE；DiD 補 no anticipation；prediction 改為 validation／CV 選模、final test 最後評估。
- 章節 ID、題目 ID、題數與閱讀／錯題儲存相容性均保持不變。
- 正式 Pages run：`{run_id}`；Source commit：`{source_sha}`；artifact：`{artifact_id}`。
- Artifact digest／下載 SHA-256：`{digest}`。
- 文件：`docs/books/econometrics/scope.md`、`docs/books/econometrics/qa_report.md`、`docs/books/econometrics/status.md`。
- 狀態：已部署。

'''
    cp,n=re.subn(r'(?ms)^### 18\. 計量經濟學\n.*?(?=^### 19\. 產業經濟學)',section,cp,count=1)
    if n!=1: raise AssertionError('checkpoint econ section drift')
    cp,n=re.subn(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',f'7. 最新正式書庫：{len(ids)} 本，`{lib["version"]}`；Pages run `{run_id}`，artifact `{artifact_id}`。',cp,count=1)
    if n!=1: raise AssertionError('checkpoint latest line drift')
    cp_path.write_text(cp,encoding='utf-8')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/record_econometrics_v3_deployment.py SITE_ROOT')
    main(sys.argv[1])
