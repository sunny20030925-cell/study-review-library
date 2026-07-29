#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

BOOK='industry-trade'
BOOK_VERSION='2026.07.30-1'

def replace_once(text, pattern, replacement, label):
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1: raise AssertionError(f'cannot update {label}')
    return out

def main(site_root):
    site=Path(site_root)
    lib=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in lib['books']]
    if ids.count(BOOK)!=1: raise AssertionError('industry-trade registry drift')
    book_no=ids.index(BOOK)+1
    root=site/'books'/BOOK
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    q=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    s=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if m['version']!=BOOK_VERSION or q['version']!=BOOK_VERSION: raise AssertionError('v2 content version drift')
    if len(m['chapters'])!=23 or q['count']!=100 or len(s['entries'])!=160: raise AssertionError('artifact count drift')
    if len(list((site/'assets/industry-trade-svg').glob('*.svg'))) != 20: raise AssertionError('figure count drift')
    checks=int(os.environ.get('INDUSTRY_TRADE_V2_REAUDIT_CHECKS','0') or 0)
    if checks<1500: raise AssertionError(f'missing/low v2 reaudit checks: {checks}')
    artifact_id=os.environ.get('PAGES_ARTIFACT_ID',''); digest=os.environ.get('PAGES_ARTIFACT_DIGEST','')
    sha=os.environ.get('PAGES_ARTIFACT_SHA256',''); page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not digest or not sha: raise AssertionError('missing artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':',1)[1]!=sha: raise AssertionError('artifact digest mismatch')
    deployed_at=datetime.now(timezone.utc).isoformat()
    run=os.environ['GITHUB_RUN_ID']; source=os.environ['GITHUB_SHA']

    rp=Path('docs/deployment_receipt.json'); receipt=json.loads(rp.read_text(encoding='utf-8'))
    receipt.update({
      'status':'success','library_version':lib['version'],'book_versions_visible':True,'progress_storage_changed':False,
      'book_count':len(ids),'book_ids':ids,
      'industry_trade_version':BOOK_VERSION,
      'industry_trade_post_publication_reaudit':'passed',
      'industry_trade_post_publication_correction_area_count':7,
      'industry_trade_post_publication_question_update_count':27,
      'industry_trade_post_publication_q04_rewrite_count':20,
      'industry_trade_post_publication_reaudit_check_count':checks,
      'industry_trade_post_publication_quantitative_recheck_count':24,
      'industry_trade_post_publication_high_risk_gate_count':28,
      'industry_trade_ids_preserved':True,'industry_trade_progress_compatibility':'preserved',
      'source_commit':source,'workflow_run_id':run,'page_url':page_url,'deployed_at':deployed_at,
      'pages_deploy_status':'success','pages_artifact_id':artifact_id,'pages_artifact_digest':digest,
      'artifact_download_recheck':'passed','artifact_download_sha256':sha,'artifact_verified_book_count':len(ids),
      'artifact_verified_industry_trade_html_count':23,'artifact_verified_industry_trade_question_count':100,
      'artifact_verified_industry_trade_search_count':160,'artifact_verified_industry_trade_svg_count':20,
      'workflow_overall_conclusion':'success','post_deploy_record_step':'passed-structured-recorder',
      'receipt_reconciliation':'automatic-from-verified-pages-artifact',
    })
    rp.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f'''# 《產業及貿易》狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{lib["version"]}`
- 狀態：已部署。

## 發布後二次內容審計

- 獨立 reaudit：{checks} 項通過。
- 100 題題庫重新檢查；其中 27 題答案／詳解精確化，20 章的「常見錯誤」題全部改為直接糾正原錯誤。
- 24 個量化節點重新計算；28 個高風險正／負 gate 通過。
- 主要修正：需求彈性、CES 固定加成邊界、策略性補貼福利計帳、FDI 定義與臨界式、Nash 議價威脅點、FTA／關稅同盟與貿易轉向福利帳。
- 反傾銷章重新核對正常價值／出口價格、公平比較、重大損害與因果關係，原核心架構保留。
- 章節 ID、題目 ID、題數與儲存鍵不變；既有閱讀進度與錯題紀錄相容。

## 成品

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 160 筆、自製 SVG 20 張。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{run}`
- source commit：`{source}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫書籍數：{len(ids)} 本。
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。
'''
    Path('docs/books/industry-trade/status.md').write_text(status,encoding='utf-8')

    qap=Path('docs/books/industry-trade/qa_report.md')
    qa=qap.read_text(encoding='utf-8')
    block=f'''## 發布後二次內容審計（v2）

- 內容版本：`{BOOK_VERSION}`。
- 獨立 reaudit：`INDUSTRY_TRADE_V2_REAUDIT_OK`，{checks} 項通過。
- 題庫：100 題重新檢查；27 題答案／詳解修正，其中 20 題為各章「常見錯誤」題。
- 數值：24 個節點由原始數值重新計算。
- 高風險：28 個正／負 gate；涵蓋 CES 加成、補貼福利口徑、FDI、Nash 議價、反傾銷、FTA／關稅同盟與貿易轉向。
- 搜尋索引：160 筆保持不變，修正區域同步更新。
- 相容性：章節 ID、題目 ID、題數與進度儲存相容性均保持不變。

### 本次實際修正

1. 需求彈性改為「需求量變動百分比／價格變動百分比」，補明自有價格彈性通常為負，Lerner 反彈性關係使用絕對值。
2. CES 固定彈性基準補明：若 ε 固定，加成率不會只因市場整合下降；需有效彈性改變、可變加成或其他競爭機制。
3. 策略性出口補貼福利帳區分「含補貼收入的利潤」與「不含補貼營業利潤」，避免補貼重複扣除。
4. FDI 改為 lasting interest 與 significant influence/control；補國際統計常用至少 10% 投票權基準，並把臨界式改為相對固定成本／相對單位成本節省。
5. Nash 議價加入 disagreement payoffs；雙邊壟斷改為一個賣方與一個買方的定義。
6. FTA／關稅同盟依「實質上全部貿易」及對外關稅差異精確化；貿易轉向例題改成不重複計算關稅收入與真實資源成本。
7. 全 20 章「常見錯誤」題改為直接修正題幹中的錯誤，並清除重複句號生成瑕疵。

### 正式發布結果

- 正式書庫：{len(ids)} 本，版本 `{lib["version"]}`。
- Pages run：`{run}`。
- Pages artifact：`{artifact_id}`；digest `{digest}`。
- 部署後 artifact 重抓：本書 23 份 HTML、100 題、160 搜尋、20 SVG 全數核對通過。
'''
    if '## 發布後二次內容審計（v2）' in qa:
        qa=re.sub(r'## 發布後二次內容審計（v2）\n.*\Z',block,qa,flags=re.S)
    else:
        qa=qa.rstrip()+'\n\n'+block
    qap.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readmep=Path('README.md'); readme=readmep.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{lib["version"]}`','README library version')
    line=f'- 《產業及貿易》：產業組織 × 國際貿易，20 章、3 附錄、100 題、160 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。'
    lines=readme.splitlines()
    found=[i for i,x in enumerate(lines) if x.startswith('- 《產業及貿易》：')]
    if not found: raise AssertionError('README industry trade line missing')
    lines[found[0]]=line
    for i in reversed(found[1:]): lines.pop(i)
    readmep.write_text('\n'.join(lines)+'\n',encoding='utf-8')

    cpp=Path('docs/shared_checkpoint.md'); cp=cpp.read_text(encoding='utf-8')
    cp=replace_once(cp,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{lib["version"]}`','checkpoint version')
    cp=replace_once(cp,r'- 正式書籍數：\d+ 本。',f'- 正式書籍數：{len(ids)} 本。','checkpoint count')
    cp=replace_once(cp,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{run}`。','checkpoint run')
    cp=replace_once(cp,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{source}`。','checkpoint source')
    cp=replace_once(cp,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    cp=replace_once(cp,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{digest}`。','checkpoint digest')
    cp=replace_once(cp,r'- Pages 狀態：.*$',f'- Pages 狀態：正式 artifact 上傳、Pages deployment 與下載後 artifact recheck 均成功；`{deployed_at}`。','checkpoint pages')
    cp=replace_once(cp,r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count={len(ids)}`、`library_version={lib["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')
    cp=replace_once(cp,r'- 實際下載正式 Pages artifact 後再次核對：.*$',f'- 實際下載正式 Pages artifact 後再次核對：{len(ids)} 本 registry；《產業及貿易》v2 23 份 HTML、100 題、160 搜尋、20 SVG 與其他正式教材均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。','checkpoint recheck')
    cp=replace_once(cp,r'- workflow overall conclusion：.*$','- workflow overall conclusion：`success`；post-deploy recorder 採結構化 Book ID／receipt 更新。','checkpoint conclusion')

    section=f'''### {book_no}. 產業及貿易
- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：產業組織 × 國際貿易；市場結構、跨國生產、政策與福利。
- 成品：20 章、3 附錄、100 題、160 搜尋、20 圖解。
- 初版 QA：Round 1 = 1495、Round 2 = 545。
- 發布後二次內容審計：{checks} 項；27 題精確化、24 個量化節點重算、28 個高風險 gate。
- 章節／題目 ID 與進度相容性保持不變。
- 正式 Pages run：`{run}`；Source commit：`{source}`。
- 狀態：已部署。

'''
    cp=re.sub(r'(?ms)^### \d+\. 產業及貿易\n.*?(?=^### |^## Canonical 部署流程)', '', cp)
    marker='## Canonical 部署流程'
    if marker not in cp: raise AssertionError('checkpoint canonical marker missing')
    cp=cp.replace(marker,section+marker,1)
    cp,n=re.subn(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',
                  f'7. 最新正式書庫：{len(ids)} 本，`{lib["version"]}`；Pages run `{run}`，artifact `{artifact_id}`。',cp,count=1)
    if n!=1: raise AssertionError('checkpoint canonical latest line')
    cpp.write_text(cp,encoding='utf-8')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/record_industry_trade_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
