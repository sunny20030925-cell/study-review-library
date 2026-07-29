# 《高等統計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`advanced-statistics`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-8`
- 狀態：已部署。
- 範圍文件：`docs/books/advanced-statistics/scope.md`
- QA 報告：`docs/books/advanced-statistics/qa_report.md`

## 成品與第二次內容審計

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、自製 SVG 20 張。
- 初版兩輪 QA 保留：27 個量化節點獨立重算、45 個高風險概念 gate。
- 2026-07-30 第二次內容審計：10 個章節修正／補強區域、7 題題庫精確化；v2 validator 1059 項、獨立數值重算 20 項全數通過。
- 主要修正：完備性與充分性的一般關係、Negative Binomial、Slutsky、MLE invariance、一致性／漸近常態、條件常態、Rao–Blackwell／CRLB、精確 z/t 區間、size vs level、p-value／NP、UMP／MLR／Wilks、Gauss–Markov 條件。
- chapter IDs `ch00`–`ch19`、100 個 question IDs、題數與儲存鍵全部維持；既有閱讀進度與錯題紀錄相容。
- 正式整合只改本書與本書衍生索引；其他正式教材內容 hash 保持不變。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`30490932468`
- source commit：`3b5d3f894432810299bc30fc86fd741d3feb6ff8`
- Pages artifact：`8739640949`
- Artifact digest：`sha256:dfefd00509f0b661dc03bfc09bb98262ea762bab096769c7356256f09182d150`
- 正式書庫：20 本，版本 `2026.07.30-8`。
- Pages deployment、artifact 下載後重驗與 deployment receipt 均成功。
