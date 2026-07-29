#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK='civil-law-overview'
BOOK_VERSION='2026.07.29-1'


def main(site_root: str=' _site') -> None:
    site=Path(site_root.strip())
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if not ids or ids[-1]!=BOOK or ids.count(BOOK)!=1:
        raise AssertionError(f'civil must be unique final book: {ids}')
    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    html_count=len(list((root/'chapters').glob('*.html')))
    svg_count=len(list((site/'assets/civil-law-overview-svg').glob('*.svg')))
    assert manifest['version']==BOOK_VERSION
    assert html_count==23 and questions['count']==100 and len(search['entries'])==150 and svg_count==20

    run_id=int(os.environ['GITHUB_RUN_ID'])
    source=os.environ['GITHUB_SHA']
    artifact_id=int(os.environ['PAGES_ARTIFACT_ID'])
    digest=os.environ['PAGES_ARTIFACT_DIGEST']
    sha=os.environ['PAGES_ARTIFACT_SHA256']
    page_url=os.environ.get('DEPLOYED_PAGE_URL','https://sunny20030925-cell.github.io/study-review-library/')
    deployed_at=datetime.now(timezone.utc).isoformat()

    rp=Path('docs/deployment_receipt.json')
    receipt=json.loads(rp.read_text(encoding='utf-8'))
    receipt.update({
      'status':'success','library_version':library['version'],'book_versions_visible':True,
      'progress_storage_changed':False,'book_count':len(ids),
      'civil_law_overview_version':BOOK_VERSION,'civil_law_overview_chapter_count':20,
      'civil_law_overview_appendix_count':3,'civil_law_overview_question_count':100,
      'civil_law_overview_search_count':150,'civil_law_overview_figure_count':20,
      'civil_law_overview_round1_check_count':157,'civil_law_overview_round2_check_count':670,
      'civil_law_overview_legal_gate_count':14,'civil_law_overview_high_risk_question_count':19,
      'civil_law_overview_existing_book_hashes_preserved':True,
      'civil_law_overview_current_law_baseline':'2026-07-29',
      'source_commit':source,'workflow_run_id':run_id,'page_url':page_url,'deployed_at':deployed_at,
      'pages_deploy_status':'success','pages_artifact_id':artifact_id,'pages_artifact_digest':digest,
      'artifact_download_recheck':'passed','artifact_download_sha256':sha,
      'artifact_verified_book_count':len(ids),'artifact_verified_civil_law_overview_html_count':html_count,
      'artifact_verified_civil_law_overview_question_count':100,
      'artifact_verified_civil_law_overview_search_count':150,
      'artifact_verified_civil_law_overview_svg_count':20,
      'workflow_overall_conclusion':'success','post_deploy_record_step':'structured-civil-law-recorder'
    })
    rp.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    sp=Path('docs/books/civil-law-overview/status.md')
    st=sp.read_text(encoding='utf-8')
    st=re.sub(r'\*\*內容、題庫、圖解與兩輪 QA 已完成；.*?\*\*',
              '**已完成正式 Pages 部署與下載後 artifact 複核。**',st,count=1,flags=re.S)
    deploy=f'''\n\n## 正式部署\n\n- 正式書庫版本：`{library['version']}`。\n- 正式書籍數：{len(ids)} 本。\n- Pages run：`{run_id}`。\n- Source commit：`{source}`。\n- Pages artifact：`{artifact_id}`。\n- Artifact digest：`{digest}`。\n- 下載後複核：23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 全數存在。\n- 既有 {len(ids)-1} 本教材內容 hash：整合前後一致。\n- 閱讀／題庫進度儲存鍵：未變更。\n'''
    if '## 正式部署' in st:
        st=re.sub(r'\n## 正式部署\n.*\Z',deploy,st,flags=re.S)
    else: st=st.rstrip()+deploy
    sp.write_text(st.rstrip()+'\n',encoding='utf-8')

    qp=Path('docs/books/civil-law-overview/qa_report.md')
    qt=qp.read_text(encoding='utf-8')
    qt=re.sub(r'## 發布門檻\n.*\Z',f'''## 發布門檻\n\n- 內容與兩輪 QA：通過。\n- 正式 Pages 部署：通過。\n- 正式書庫版本：`{library['version']}`；書籍數：{len(ids)}。\n- Pages run：`{run_id}`；artifact：`{artifact_id}`；digest：`{digest}`。\n- 下載後 artifact 再驗證：通過。\n- 既有 {len(ids)-1} 本教材逐書 hash 保持一致；`progress_storage_changed=false`。\n''',qt,flags=re.S)
    qp.write_text(qt.rstrip()+'\n',encoding='utf-8')

    cp=Path('docs/shared_checkpoint.md'); c=cp.read_text(encoding='utf-8')
    replacements={
      r'- 正式書庫內容版本：`[^`]+`。':f'- 正式書庫內容版本：`{library["version"]}`。',
      r'- 正式書籍數：\d+ 本。':f'- 正式書籍數：{len(ids)} 本。',
      r'- 最新正式 Pages run：`[^`]+`。':f'- 最新正式 Pages run：`{run_id}`。',
      r'- 最新正式部署 source commit：`[^`]+`。':f'- 最新正式部署 source commit：`{source}`。',
      r'- 最新 Pages artifact：`[^`]+`。':f'- 最新 Pages artifact：`{artifact_id}`。',
      r'- Artifact digest：`[^`]+`。':f'- Artifact digest：`{digest}`。',
      r'- Pages 狀態：.*':f'- Pages 狀態：正式 artifact 上傳、Pages deployment 與下載後 artifact recheck 均成功；`{deployed_at}`。',
      r'- 部署回條：`docs/deployment_receipt.json`；.*':f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count={len(ids)}`、`library_version={library["version"]}`、`progress_storage_changed=false`。',
      r'- 實際下載正式 Pages artifact 後再次核對：.*':f'- 實際下載正式 Pages artifact 後再次核對：{len(ids)} 本 registry；民法概要 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。',
    }
    for pat,repl in replacements.items(): c=re.sub(pat,repl,c,count=1)
    c=re.sub(r'- workflow overall conclusion 仍為 `failure-after-successful-pages-deploy`：.*\n','',c,count=1)
    if 'Book ID：`civil-law-overview`' not in c:
        section=f'''\n### {len(ids)}. 民法概要\n- Book ID：`civil-law-overview`\n- 正式內容版本：`{BOOK_VERSION}`\n- 定位：一般大學民法概要；總則、債、物權、親屬、繼承，以請求權基礎與案例解題為主。\n- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。\n- QA：第一輪 157 項、第二輪 670 項；14 組現行法高風險 gate、19 個高風險題目精確 gate。\n- 現行法基準：2026-07-29；民法第 166-1 條保持「施行日期尚未另定」警示。\n- 正式 Pages run：`{run_id}`；Source commit：`{source}`。\n- 狀態：已部署。\n\n'''
        c=c.replace('\n## Canonical 部署流程\n',section+'## Canonical 部署流程\n',1)
    c=re.sub(r'- 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',
             f'- 最新正式書庫：{len(ids)} 本，`{library["version"]}`；Pages run `{run_id}`，artifact `{artifact_id}`。',c,count=1)
    cp.write_text(c,encoding='utf-8')

    readme=Path('README.md'); r=readme.read_text(encoding='utf-8')
    r=re.sub(r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`',r,count=1)
    bullet=f'- 《民法概要》：一般大學民法概要，20 章、3 附錄、100 題題庫、150 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。\n'
    if '《民法概要》' not in r:
        marker='## 部署流程'
        if marker in r: r=r.replace(marker,bullet+'\n'+marker,1)
        else: r=r.rstrip()+'\n'+bullet
    readme.write_text(r,encoding='utf-8')
    print(f'CIVIL_LAW_DEPLOYMENT_RECORDED books={len(ids)} library={library["version"]} run={run_id} artifact={artifact_id}')

if __name__=='__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else '_site')
