# 《投資學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`investments`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-8`
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
- 2026-07-30 發布後第二次獨立審計：7 個修正區域、6 題詳解精確化；v2 reaudit validator 共 730 項通過。
- 45 個數值題再次由原始數字獨立重算；未發現既有數值答案算術錯誤。
- 修正重點：APT 零均值 factor surprise、DuPont 平均存量口徑、duration／convexity／immunization、forward cost-of-carry、ETF 主動／被動分類、外幣資產本幣報酬、Information Ratio。
- ETF 分類以 2026-07-30 查核之臺灣證券交易所現行說明為校對基準；不把 ETF 與「指數股票型基金」無條件視為同義詞。

## 正式發布證據

- canonical workflow：`Deploy study library`
- workflow run：`30490932468`
- source commit：`3b5d3f894432810299bc30fc86fd741d3feb6ff8`
- Pages artifact：`8739640949`
- Artifact digest：`sha256:dfefd00509f0b661dc03bfc09bb98262ea762bab096769c7356256f09182d150`
- 正式書庫：20 本，版本 `2026.07.30-8`。
- Pages deployment、artifact 下載後重驗與結構化 deployment receipt 均成功。
