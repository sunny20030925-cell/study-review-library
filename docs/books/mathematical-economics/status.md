# 《數理經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`mathematical-economics`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-9`
- 目前 stage：`VP`
- Task ID：`mathematical-economics:VP`
- 下一階段：`PUB`
- Published：既有正式版本維持 `passed`；本書屬 workflow v2 建立前已發布教材。
- QA 報告：`docs/books/mathematical-economics/qa_report.md`
- External Audit：`docs/books/mathematical-economics/external_audit.md`

## Internal QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- 第二次獨立內容審計修正／補強 13 個核心區域，調整 11 題高風險題庫。
- v2 獨立 QA：855 項；數值／公式重算：23 項；高風險邏輯 gate：10 項，全部通過。
- 補強內容含 rank／聯立系統一致性、內積與線性組合、鏈鎖律、隱函數 Jacobian、凹性／擬凹性、受限二階條件、bordered Hessian、KKT 前提、constrained envelope theorem、積分累積與動態穩定邊界。

## External Audit（2026-07-30）

- 結果：`passed`。
- 主路由：Wolfram。
- 以既有 13 個高風險修正區域、23 個數值／公式節點與 10 個邏輯 gate 為抽樣母體，不對普通基礎敘述做第三次全量 QA。
- Wolfram 獨立重算 23 個 QA 數值／公式節點，全部與正式 v2 一致。
- 額外形式化檢查 rank、一維 invariant span、Hessian、等式限制切方向 SOC、KKT 邊界乘數、envelope derivative、Euler 齊次關係、`b=-1` 二期循環及 `F'(x*)=0` 線性化失效，均支持教材現有敘述。
- 核心答案錯誤：0。
- unresolved blocker：0。
- 不需修改正文或題庫，不提高 content version。
- Consensus／Scite 未使用：本輪沒有抽到需要實證研究或重要論文引用脈絡才能判定的核心主張。

## 相容性

- Book ID 不變。
- 20 個 chapter ID 不變。
- 100 個 question ID 不變。
- 閱讀進度與錯題資料相容。
- External Audit 沒有修改教材內容包、PWA 資產或 storage key。

## 部署

- canonical workflow：`Deploy study library`
- 最新成功正式 workflow run：`30494922034`
- 最新成功正式 source commit：`d502e3db8be674c030c5b13db88f1b33dfdedb28`
- Pages artifact：`8741187091`
- Artifact digest：`sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`
- 正式書庫書籍數：21 本。
- 本次 External Audit 僅寫回狀態，不重新部署 Pages。
- 下一次真正需要共同 PWA／Pages 發布前，須先修正已知過時的 `industry-trade` registry-tail inline gate。
