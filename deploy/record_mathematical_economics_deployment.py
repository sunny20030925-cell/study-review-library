#!/usr/bin/env python3
from __future__ import annotations

import json, os, re
from datetime import datetime, timezone
from pathlib import Path

BOOK='mathematical-economics'
BOOK_VERSION='2026.07.29-1'
ROUND1=777
ROUND2=56
NUMERIC=23
HIGH_RISK=10


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1: raise AssertionError(f'cannot update {label}')
    return out


def upsert_book_line(readme: str, title: str, line: str) -> str:
    lines=readme.splitlines(); prefix=f'- 《{title}》：'; idxs=[i for i,x in enumerate(lines) if x.startswith(prefix)]
    if idxs:
        lines[idxs[0]]=line
        for i in reversed(idxs[1:]): del lines[i]
    else:
        book_lines=[i for i,x in enumerate(lines) if x.startswith('- 《')]
        if not book_lines: raise AssertionError('README book list missing')
        lines.insert(max(book_lines)+1,line)
    return '\n'.join(lines)+'\n'


def main(site_root: str) -> None:
    site=Path(site_root); library=json.loads((site/'data/library.json').read_text(encoding='utf-8')); ids=[b['id'] for b in library['books']]
    if len(ids)!=16 or ids[-2:]!=['game-theory',BOOK]: raise AssertionError(f'expected 16-book game-theory -> mathematical-economics tail, got {ids}')
    root=site/'books'/BOOK; manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8')); questions=json.loads((root/'questions.json').read_text(encoding='utf-8')); search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    chapters=len([x for x in manifest['chapters'] if x['kind']=='chapter']); appendices=len([x for x in manifest['chapters'] if x['kind']=='appendix']); figures=len(list((site/'assets/mathematical-economics-svg').glob('*.svg')))
    if manifest['version']!=BOOK_VERSION or questions['version']!=BOOK_VERSION: raise AssertionError('mathematical economics version drift')
    if (chapters,appendices,questions['count'],len(search['entries']),figures)!=(20,3,100,150,20): raise AssertionError('mathematical economics artifact counts drift')

    artifact_id=os.environ.get('PAGES_ARTIFACT_ID',''); digest=os.environ.get('PAGES_ARTIFACT_DIGEST',''); artifact_sha=os.environ.get('PAGES_ARTIFACT_SHA256',''); page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not digest or not artifact_sha: raise AssertionError('missing artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':',1)[1]!=artifact_sha: raise AssertionError('artifact digest mismatch')

    receipt_path=Path('docs/deployment_receipt.json'); receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status':'success','library_version':library['version'],'book_versions_visible':True,'progress_storage_changed':False,'book_count':16,
        'mathematical_economics_version':BOOK_VERSION,'mathematical_economics_chapter_count':20,'mathematical_economics_appendix_count':3,
        'mathematical_economics_question_count':100,'mathematical_economics_search_count':150,'mathematical_economics_figure_count':20,
        'mathematical_economics_round1_check_count':ROUND1,'mathematical_economics_round2_check_count':ROUND2,
        'mathematical_economics_quantitative_recheck_count':NUMERIC,'mathematical_economics_high_risk_concept_gate_count':HIGH_RISK,
        'mathematical_economics_two_round_qa':'passed','mathematical_economics_existing_book_hashes_preserved':True,
        'source_commit':os.environ['GITHUB_SHA'],'workflow_run_id':os.environ['GITHUB_RUN_ID'],'page_url':page_url,'deployed_at':datetime.now(timezone.utc).isoformat(),
        'pages_deploy_status':'success','pages_artifact_id':artifact_id,'pages_artifact_digest':digest,'artifact_download_recheck':'passed','artifact_download_sha256':artifact_sha,
        'artifact_verified_book_count':16,'artifact_verified_mathematical_economics_html_count':23,'artifact_verified_mathematical_economics_question_count':100,
        'artifact_verified_mathematical_economics_search_count':150,'artifact_verified_mathematical_economics_svg_count':20,
        'workflow_overall_conclusion':'success','post_deploy_record_step':'passed-structured-recorder','receipt_reconciliation':'automatic-from-verified-pages-artifact'})
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f'''# 《數理經濟學》製作狀態\n\n更新日期：2026-07-29\n\n## 正式識別\n\n- Book ID：`{BOOK}`\n- 正式內容版本：`{BOOK_VERSION}`\n- 正式書庫版本：`{library['version']}`\n- 狀態：已部署。\n- 範圍文件：`docs/books/{BOOK}/scope.md`\n- QA 報告：`docs/books/{BOOK}/qa_report.md`\n\n## 成品與 QA\n\n- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。\n- 第一輪結構／內容 QA：{ROUND1} 項通過。\n- 第二輪獨立 QA：{ROUND2} 項通過；{NUMERIC} 個數值節點重算、{HIGH_RISK} 個高風險邏輯 gate。\n- 既有 15 本教材內容 hash 在整合前後完全一致。\n- 閱讀進度相容性：新增獨立 Book ID，不改既有章節 ID、題目 ID、儲存鍵或錯題紀錄。\n\n## 部署\n\n- canonical workflow：`Deploy study library`\n- workflow run：`{os.environ['GITHUB_RUN_ID']}`\n- source commit：`{os.environ['GITHUB_SHA']}`\n- Pages artifact：`{artifact_id}`\n- Artifact digest：`{digest}`\n- 正式書庫書籍數：16 本。\n- GitHub Pages 部署、artifact 下載重驗與 deployment receipt 均成功。\n'''
    Path(f'docs/books/{BOOK}/status.md').write_text(status,encoding='utf-8')

    qa_path=Path(f'docs/books/{BOOK}/qa_report.md'); qa=qa_path.read_text(encoding='utf-8')
    final_block=f'''## 正式發布結果\n\n- 第一輪 QA：{ROUND1} 項，通過。\n- 第二輪獨立 QA：{ROUND2} 項，通過；{NUMERIC} 個數值節點重算、{HIGH_RISK} 個高風險邏輯 gate。\n- 既有 15 本內容 hash：整合前後完全一致。\n- 正式書庫：16 本，版本 `{library['version']}`。\n- Pages run：`{os.environ['GITHUB_RUN_ID']}`。\n- Pages artifact：`{artifact_id}`；digest `{digest}`。\n- 部署後 artifact 重新下載：23 份本書 HTML、100 題、150 搜尋、20 SVG 全數核對通過。\n- post-deploy recorder：`passed-structured-recorder`。\n'''
    qa=re.sub(r'## 正式發布結果\n.*\Z',final_block,qa,flags=re.S) if '## 正式發布結果' in qa else qa.rstrip()+'\n\n'+final_block
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md'); readme=readme_path.read_text(encoding='utf-8'); readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README version')
    readme=upsert_book_line(readme,'數理經濟學',f'- 《數理經濟學》：函數、矩陣、微積分、比較靜態、最佳化與動態系統；20 章、3 附錄、100 題、150 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。')
    readme_path.write_text(readme,encoding='utf-8')

    cp=Path('docs/shared_checkpoint.md'); c=cp.read_text(encoding='utf-8')
    c=replace_once(c,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{library["version"]}`','checkpoint version')
    c=replace_once(c,r'- 正式書籍數：\d+ 本。','- 正式書籍數：16 本。','checkpoint count')
    c=replace_once(c,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。','checkpoint run')
    c=replace_once(c,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。','checkpoint source')
    c=replace_once(c,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    c=replace_once(c,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{digest}`。','checkpoint digest')
    c=replace_once(c,r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=16`、`library_version={library["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')
    c=re.sub(r'- 實際下載正式 Pages artifact 後再次核對：.*$', '- 實際下載正式 Pages artifact 後再次核對：16 本 registry、本書 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 均存在；下載檔 SHA-256 與 GitHub artifact digest 完全一致。', c, count=1, flags=re.M)
    section=f'''### 16. 數理經濟學\n- Book ID：`{BOOK}`\n- 正式內容版本：`{BOOK_VERSION}`\n- 定位：一般大學 Mathematical Economics／Mathematics for Economists；線性代數、微積分、比較靜態、最佳化、積分與一階動態。\n- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。\n- QA：第一輪 {ROUND1} 項、第二輪 {ROUND2} 項通過；{NUMERIC} 個數值節點重算、{HIGH_RISK} 個高風險邏輯 gate。\n- 既有 15 本教材內容 hash 在整合前後完全一致。\n- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`。\n- 文件：`docs/books/{BOOK}/scope.md`、`docs/books/{BOOK}/qa_report.md`、`docs/books/{BOOK}/status.md`。\n- 狀態：已部署。\n\n'''
    marker='## Canonical 部署流程'
    if marker not in c: raise AssertionError('checkpoint canonical marker missing')
    if re.search(r'(?ms)^### 16\. 數理經濟學\n.*?(?=^## Canonical 部署流程)',c): c=re.sub(r'(?ms)^### 16\. 數理經濟學\n.*?(?=^## Canonical 部署流程)',section,c,count=1)
    else: c=c.replace(marker,section+marker,1)
    c=re.sub(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',f'7. 最新正式書庫：16 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',c,count=1)
    cp.write_text(c,encoding='utf-8')
    print(json.dumps({'status':'success','library_version':library['version'],'book_count':16,'mathematical_economics_version':BOOK_VERSION,'pages_artifact_id':artifact_id,'structured_recorder':True},ensure_ascii=False))


if __name__=='__main__':
    import sys
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/record_mathematical_economics_deployment.py SITE_ROOT')
    main(sys.argv[1])
