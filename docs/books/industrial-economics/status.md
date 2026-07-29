# 《產業經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`industrial-economics`
- 內容版本：`2026.07.29-1`
- 狀態：正文、圖解、題庫與兩輪 QA 完成；正式發布候選驗證中。
- Draft PR：`#80`
- 最新已驗證 Pages 基底：18 本、書庫版本 `2026.07.29-23`（計量經濟學正式 Pages artifact）。
- `deployment_receipt.json` 仍停在 17 本／`2026.07.29-22`，原因是計量經濟學舊 workflow 沒有 post-deploy recorder；產經 base-selector 會同時驗證 receipt artifact 與最新成功 workflow artifact，採用實際較新的 18 本／v23 成品。
- 本輪預期候選：19 本、書庫版本 `2026.07.29-24`；產經正式部署成功後 structured recorder 會把 deployment receipt 一併對齊最新版本。

## 固定規模

- 正文 20 章（`ch00`–`ch19`）
- 附錄 3 份
- 題庫 100 題，每章 5 題
- 搜尋索引 150 筆
- 自製 SVG 20 張

## QA

- 第一輪：結構、模型條件、題庫、搜尋、圖解與高風險觀念 gate。
- 第二輪：100 題逐題檢查、17 個量化節點獨立重算、18 組高風險模型／條件複核。
- 整合器會對發布前所有正式教材逐書計算內容 hash；新增本書後必須全部不變。
- post-deploy recorder 已納入候選 CI dry-run，會驗證 receipt、README 與 shared checkpoint 的結構化更新。

## 發布規則

優先使用 `docs/deployment_receipt.json` 指定的正式 Pages artifact；若最新 `Deploy study library` workflow 明確成功、其 `github-pages` artifact digest 可重驗，且 artifact 內書庫版本高於 receipt，才允許採用該較新 Pages artifact 作為正式基底。Pages deployment、artifact 重新下載與結構化 receipt 三者都成功後，才標記「已部署」。
