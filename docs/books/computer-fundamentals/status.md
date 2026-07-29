# 《計算機概論》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`computer-fundamentals`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-9`
- 狀態：已部署；發布後第二次內容複核與精確性修正完成。
- 範圍文件：`docs/books/computer-fundamentals/scope.md`
- QA 報告：`docs/books/computer-fundamentals/qa_report.md`

## 成品與 v2 內容審計

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- 第二次內容審計共 15 個修正／補強區域，12 題題庫精確化。
- v2 獨立 QA：128 項；獨立數值重算：36 項，全部通過。
- 修正重點：page fault／virtual memory、interrupt vs exception、URL authority、HTTP/3 + QUIC/TLS 1.3、Big-O vs Θ、二分搜尋減半／比較次數、foreign key、ACID、password hashing、NIST cloud 與 edge security/privacy。
- 全部非目標教材內容 hash 在修正前後完全一致。
- Book ID、20 個章節 ID、100 個題目 ID、題數與進度儲存鍵均未變，既有閱讀進度與錯題紀錄相容。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`30494922034`
- source commit：`d502e3db8be674c030c5b13db88f1b33dfdedb28`
- Pages artifact：`8741187091`
- Artifact digest：`sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`
- 正式書庫書籍數：21 本。
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。
