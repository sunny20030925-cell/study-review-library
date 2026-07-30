# 《統計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`statistics`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-16`
- 目前 stage：`PUB`
- Task ID：`statistics:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/statistics/qa_report.md`
- External Audit：`docs/books/statistics/external_audit.md`

## Internal QA 證據

- 正文 19 章、附錄 3 份、題庫 95 題、搜尋索引 169 筆、SVG 19 張。
- 發布後獨立二次校錯：1,195／1,195；95／95 題重查；44 個計算／公式／統計判斷重算重判。
- 已補直方圖密度、CV、Chebyshev、variance/covariance、z/t、比例 CI/test、p-value、非參數與 `R²=r²` 的成立條件。

## External Audit

- 結果：`passed`
- 路由：Wolfram。
- 抽查描述統計、機率／Bayes、分配、sampling SE、CI、z/t、chi-square、ANOVA、簡單迴歸與推論語意。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、閱讀進度、錯題資料與 PWA storage 均不變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`statistics:VP`；結果：`passed`。
- 高價值資產：`統計學推論方法選擇地圖`。
- Canva design ID：`DAHQ3VXu1eY`；可編輯來源：`https://www.canva.com/d/U6gZwMg-Ro4Z3Lg`。
- PWA 資產：`assets/statistics-svg/data-process.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30547172891`；Pages artifact：`8761199558`。
- Artifact digest：`sha256:0a6dabaadf0679e67f85e2a2146e978023d0bf0a18b1dd091e24c523c7f52dd7`；重新下載 SHA256 完全一致。
- VP validator：`108 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/statistics/visual_polish.md`。
- 本書已切換至 `statistics:PUB`。
- 全書庫下一個 Visual Polish target：`game-theory`。
