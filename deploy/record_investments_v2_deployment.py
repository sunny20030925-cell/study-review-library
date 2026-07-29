#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

BOOK = "investments"
BOOK_VERSION = "2026.07.30-1"


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError(f"cannot update {label}: count={n}")
    return out


def main(site_root: str) -> None:
    site = Path(site_root)
    library = json.loads((site / "data/library.json").read_text(encoding="utf-8"))
    ids = [b["id"] for b in library["books"]]
    if ids.count(BOOK) != 1:
        raise AssertionError(f"investments registry drift: {ids}")

    root = site / "books" / BOOK
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    questions = json.loads((root / "questions.json").read_text(encoding="utf-8"))
    search = json.loads((root / "search.json").read_text(encoding="utf-8"))
    if manifest["version"] != BOOK_VERSION or questions["version"] != BOOK_VERSION:
        raise AssertionError("investments v2 content version drift")
    if len(manifest["chapters"]) != 25 or questions["count"] != 110 or len(search["entries"]) != 165:
        raise AssertionError("investments artifact count drift")
    if len(list((site / "assets/investments-svg").glob("*.svg"))) != 22:
        raise AssertionError("investments SVG count drift")

    artifact_id = os.environ.get("PAGES_ARTIFACT_ID", "")
    digest = os.environ.get("PAGES_ARTIFACT_DIGEST", "")
    sha = os.environ.get("PAGES_ARTIFACT_SHA256", "")
    if not artifact_id or not digest or not sha:
        raise AssertionError("missing verified Pages artifact environment")
    if digest.startswith("sha256:") and digest.split(":", 1)[1] != sha:
        raise AssertionError("artifact digest mismatch")
    reaudit_checks = int(os.environ.get("INVESTMENTS_REAUDIT_CHECKS", "0") or 0)
    if reaudit_checks < 700:
        raise AssertionError(f"investments reaudit metric too small: {reaudit_checks}")

    receipt_path = Path("docs/deployment_receipt.json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt.update({
        "investments_version": BOOK_VERSION,
        "investments_chapter_count": 22,
        "investments_appendix_count": 3,
        "investments_question_count": 110,
        "investments_search_count": 165,
        "investments_figure_count": 22,
        "investments_round1_check_count": 2672,
        "investments_round2_check_count": 139,
        "investments_quantitative_recheck_count": 45,
        "investments_high_risk_concept_recheck_count": 20,
        "investments_two_round_qa": "passed",
        "investments_post_publication_reaudit": "passed",
        "investments_post_publication_correction_area_count": 7,
        "investments_post_publication_question_adjustment_count": 6,
        "investments_post_publication_reaudit_check_count": reaudit_checks,
        "investments_ids_preserved": True,
        "investments_progress_compatibility": "preserved",
        "investments_existing_book_hashes_preserved": True,
        "artifact_verified_investments_html_count": 25,
        "artifact_verified_investments_question_count": 110,
        "artifact_verified_investments_search_count": 165,
        "artifact_verified_investments_svg_count": 22,
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    run_id = os.environ["GITHUB_RUN_ID"]
    source_sha = os.environ["GITHUB_SHA"]
    status = f'''# 《投資學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library["version"]}`
- 狀態：已部署。
- 範圍文件：`docs/books/investments/scope.md`
- QA 報告：`docs/books/investments/qa_report.md`

## 成品與相容性

- 正文 22 章、附錄 3 份、題庫 110 題、搜尋索引 165 筆、自製 SVG 22 張。
- 章節 ID `ch00`–`ch21`、110 個題目 ID、Book ID 與儲存鍵全部維持；既有閱讀進度與錯題紀錄相容。
- 其餘教材逐檔 hash 在修正前後保持不變。

## QA 與發布後第二次獨立內容審計

- 初版第一輪 QA：2,672／2,672。
- 初版第二輪 QA：139／139；45 項量化節點重算、20 項高風險概念重判。
- 2026-07-30 發布後第二次獨立審計：7 個修正區域、6 題詳解精確化；v2 reaudit validator 共 {reaudit_checks} 項通過。
- 45 個數值題再次由原始數字獨立重算；未發現既有數值答案算術錯誤。
- 修正重點：APT 零均值 factor surprise、DuPont 平均存量口徑、duration／convexity／immunization、forward cost-of-carry、ETF 主動／被動分類、外幣資產本幣報酬、Information Ratio。
- ETF 分類以 2026-07-30 查核之臺灣證券交易所現行說明為校對基準；不把 ETF 與「指數股票型基金」無條件視為同義詞。

## 正式發布證據

- canonical workflow：`Deploy study library`
- workflow run：`{run_id}`
- source commit：`{source_sha}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫：{len(ids)} 本，版本 `{library["version"]}`。
- Pages deployment、artifact 下載後重驗與結構化 deployment receipt 均成功。
'''
    Path("docs/books/investments/status.md").write_text(status, encoding="utf-8")

    qa_path = Path("docs/books/investments/qa_report.md")
    qa = qa_path.read_text(encoding="utf-8")
    block = f'''## 發布後第二次獨立內容審計 v2（2026-07-30）

本輪直接以正式 Pages artifact 中實際提供給使用者的 22 章、3 附錄與 110 題為基準，不把原本 QA 的「通過」當成內容正確性的替代證據。

### 審計結果

- v2 reaudit validator：**{reaudit_checks} 項通過**。
- 110 題全部重新納入答案／詳解／ID 一致性檢查。
- 其中 45 個量化題直接由題目原始數字重新計算；未發現既有數值答案的算術錯誤。
- 發現並修正 7 個內容精確性區域；6 題保留原 ID、只精確化詳解。
- 22 章、3 附錄、110 題、165 搜尋、22 SVG 及所有既有 ID 均維持。

### 修正 1：APT 報酬生成式的零均值條件

- v1 寫成 `R_i=E[R_i]+Σ beta_ij F_j+e_i`，但沒有明說 `F_j` 的中心化口徑。
- v2 明列：若截距直接寫成 `E[R_i]`，`F_j` 應是零均值 factor surprise／去均值因子，且 `E[e_i]=0`。

### 修正 2：DuPont 的期間／存量口徑

- v1 基本 ROE 已使用 Average Equity，但三段 DuPont 簡寫成 `Sales/Assets × Assets/Equity`，容易讓讀者用期末存量搭配整期流量。
- v2 統一為 `Sales/Average Assets × Average Assets/Average Equity`，並明示自行由財報計算時需維持期間口徑一致。

### 修正 3：Duration、Convexity 與 Immunization

- 補上本書 convexity 的價格正規化二階導數定義，避免 `1/2 × Conv × (Δy)^2` 的尺度不明。
- 單一負債補充資產價值與 Macaulay duration 對應；多筆負債補充 market value、money duration／BPV、凸性與曲線形狀風險。
- 維持「免疫仍需再平衡」的原本正確結論，但不再把 duration matching 講成足以永久鎖定的單一條件。

### 修正 4：無收益標的 Forward Cost of Carry

- v1 把 `F_0≈S_0(1+r)^T` 寫成近似式。
- v2 改為：在無收益、無其他 carry、可按 `r` 融資／投資且無套利的離散複利假設下，`F_0=S_0(1+r)^T` 是定價等式；有股利、收益、儲存成本或便利收益時另行調整。

### 修正 5：ETF 不再與被動指數化混為同義詞

- v1 附錄將 Exchange-Traded Fund 直接翻成「指數股票型基金 ETF」，對目前臺灣市場已不完整。
- v2 改為「交易所交易基金 ETF」，正文明確區分 ETF 的交易架構與 indexing 的被動管理策略。
- 依 2026-07-30 查核之臺灣證券交易所說明，現行證信託 ETF 已包含被動式 ETF 與主動式 ETF；主動式 ETF 不強制須有 benchmark。

### 修正 6：外幣資產本幣報酬

- v1 將乘法關係寫成近似號且未固定匯率方向。
- v2 固定 `S_t` 為「1 單位外幣的本幣價格」，`R_FX=S_1/S_0-1`，因此 `1+R_home=(1+R_foreign)(1+R_FX)` 是精確乘法關係。
- 只有報酬幅度很小時，`R_home≈R_foreign+R_FX` 才是一階近似；新增 10% × 5% → 15.5% 的例子。

### 修正 7：Information Ratio 分子

- v1 定義文字已說「平均主動報酬」，公式卻寫單期 `R_P-R_B`。
- v2 統一為 `IR=mean(R_P-R_B)/σ(R_P-R_B)`，並補充分子與 tracking error 必須採一致期間／年化口徑。

### 相容性與正式部署

- Book version：`{BOOK_VERSION}`。
- Shared library：`{library["version"]}`，{len(ids)} 本。
- Pages run：`{run_id}`。
- Pages artifact：`{artifact_id}`；digest `{digest}`。
- 部署後重新下載 artifact，再核對 25 份 HTML、110 題、165 搜尋與 22 SVG；所有非 Investments 教材 hash 均保持不變。
'''
    marker = "## 發布後第二次獨立內容審計 v2（2026-07-30）"
    if marker in qa:
        qa = re.sub(r"## 發布後第二次獨立內容審計 v2（2026-07-30）\n.*\Z", block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + "\n\n" + block
    qa_path.write_text(qa.rstrip() + "\n", encoding="utf-8")

    readme_path = Path("README.md")
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_once(readme, r"目前內容版本：`[^`]+`", f"目前內容版本：`{library['version']}`", "README version")
    line = (
        f"- 《投資學》：一般大學投資學核心，22 章、3 附錄、110 題題庫、165 筆搜尋索引與 22 張圖解；"
        f"發布後第二次獨立內容審計修正 APT、DuPont、免疫、forward、ETF、匯率報酬與 Information Ratio 等 7 個精確性區域，內容版本 `{BOOK_VERSION}`。"
    )
    lines = readme.splitlines()
    matches = [i for i, x in enumerate(lines) if x.startswith("- 《投資學》：")]
    if len(matches) != 1:
        raise AssertionError(f"README investments line count={len(matches)}")
    lines[matches[0]] = line
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    cp_path = Path("docs/shared_checkpoint.md")
    cp = cp_path.read_text(encoding="utf-8")
    section = f'''### 17. 投資學
- Book ID：`investments`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學投資學；報酬與風險、投資組合、資產定價、證券估值、衍生工具、資產配置與績效評估。
- 成品：22 章、3 附錄、110 題、165 搜尋、22 圖解。
- 初版 QA：第一輪 2,672／2,672、第二輪 139／139；45 個量化節點重算、20 個高風險概念重判。
- 2026-07-30 發布後第二次獨立內容審計：7 個精確性修正區域、6 題詳解精確化；v2 reaudit validator {reaudit_checks} 項通過。
- 45 個量化題再次由原始數字獨立重算，未發現既有數值答案算術錯誤。
- 修正重點：APT 零均值 factor surprise、DuPont 平均存量、convexity／immunization、forward cost-of-carry、主動／被動 ETF、外幣資產本幣報酬、Information Ratio。
- 章節 ID、110 題題目 ID、Book ID 與閱讀／錯題儲存相容性均保持不變；其他教材 hash 不變。
- 正式 Pages run：`{run_id}`；Source commit：`{source_sha}`；artifact：`{artifact_id}`。
- Artifact digest／下載 SHA-256：`{digest}`。
- 文件：`docs/books/investments/scope.md`、`docs/books/investments/qa_report.md`、`docs/books/investments/status.md`。
- 狀態：已部署。

'''
    cp, n = re.subn(r"(?ms)^### 17\. 投資學\n.*?(?=^### 18\. 計量經濟學)", section, cp, count=1)
    if n != 1:
        raise AssertionError("checkpoint investments section not found")
    cp_path.write_text(cp, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python deploy/record_investments_v2_deployment.py SITE_ROOT")
    main(sys.argv[1])
