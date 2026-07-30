# 《計算機概論》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`computer-fundamentals`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-29`
- 目前 stage：`PUB`
- Task ID：`computer-fundamentals:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- 範圍：`docs/books/computer-fundamentals/scope.md`
- Internal QA：`docs/books/computer-fundamentals/qa_report.md`
- External Audit：`docs/books/computer-fundamentals/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、SVG 20 張。
- 第二次內容審計 15 個修正區域、12 題精確化；v2 QA 128 項＋36 項獨立數值重算。

## External Audit

- 結果：`passed`
- 路由：RFC／NIST official primary sources + Wolfram。
- 抽查 number representation、CPU/memory、OS/VM、TCP/UDP/HTTP3、Big-O、database、password hashing、cloud 與代表性計算。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

Book／chapter／question IDs、題數、PWA、離線快取結構、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`computer-fundamentals:VP`；結果：`passed`。
- 高價值資產：`計算機概論資料硬體作業系統網路程式與安全判斷地圖`。
- Canva design ID：`DAHQ5HKTq5M`；可編輯來源：`https://www.canva.com/d/pgWvtGBlDcRP0Nd`。
- PWA 資產：`assets/computer-fundamentals-svg/computing-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30587597954`；Pages artifact：`8777096042`。
- Artifact digest：`sha256:400cff28cec915fbe4bd6dc6314fd86f4ea3b838b37990f88bb4646c1778a7ea`；重新下載 SHA256 完全一致。
- VP validator：`92 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/computer-fundamentals/visual_polish.md`。
- 本書已切換至 `computer-fundamentals:PUB`。
- 全書庫下一個 Visual Polish target：`calculus`。
