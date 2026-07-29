# 《計算機概論》QA 報告

更新日期：2026-07-30

## 版本與範圍

- Book ID：`computer-fundamentals`
- 正式內容版本：`2026.07.30-2`
- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 圖解：20 張自製 SVG。

## 第一輪：製作內檢

初版候選 workflow 以當時最新已部署書庫 artifact 的副本重新生成本書，並檢查：

1. Python source 可編譯。
2. 20 章、3 附錄、100 題、150 搜尋與 20 SVG 結構完整。
3. 每章具本章問題、白話直覺、正式定義、核心關係／公式、完整例題、常見錯誤、考試判斷與理解檢查。
4. 100 題 ID 唯一且每章恰 5 題；答案與詳解不可為空。
5. 代表性數值答案重新核對：進位、位元樣式、影像容量、CPU 時間、AMAT、I/O 時間、分頁、網路速率／傳輸延遲、二分搜尋、雜湊負載、accuracy 與 availability。
6. 重要精確性字串與高風險過度敘述掃描。
7. manifest、題庫、搜尋、章節與圖檔全部加入 service worker cache。
8. 新書只能追加在當時正式書庫尾端；既有書籍逐檔 SHA-256 前後必須一致。
9. `app.js` 與 `sw.js` 必須通過 JavaScript syntax check。
10. 平板實際會讀取的所有章節與圖檔路徑必須存在。

## 第二輪：獨立複核

第二支獨立 QA 程式不重用第一輪的答案計算，而會重新：

1. 計算二進位 11010、十六進位 FF、12-bit pattern 數、影像 bits、2 GHz 週期與 CPU time、AMAT、傳輸時間、頁數、Mb/s→MB/s、binary search 次數、hash load factor、accuracy 與 availability。
2. 重判 26 個高風險觀念節點，包括 KiB、浮點近似、CPU 時脈、concurrency／parallelism、虛擬記憶體、DNS、TCP／UDP、HTTPS、Big-O、外鍵、測試覆蓋、authentication／authorization、hash／encryption、AI 評估、distributed system 與 open source。
3. 對 100 題逐題檢查題幹、答案與詳解長度與完整性，防止只給答案或空泛詳解。
4. 重新掃描 20 章的核心術語一致性與常見矛盾式敘述。
5. 檢查每章正文不是只有大綱，而有足夠解釋段落、陷阱與考試判斷內容。

## 發布門檻

- 兩輪 QA 必須在正式發布 gate 通過。
- 若 QA 發現內容錯誤，修正後重新跑驗證；需要時提高內容版本並留下修正紀錄。
- 正式發布前再次讀取最新 `main`、`docs/shared_checkpoint.md`、最新正式 registry 與 deployment receipt。
- 共同書庫版本與 service worker version 必須從正式最新尾端順增。
- 既有 Book ID、章節 ID、題目 ID、閱讀進度、錯題與設定儲存鍵不得被修正版破壞。

## 目前結果

《計算機概論》初版與發布後第二次內容審計均已完成正式 Pages 部署；目前正式內容版本為 `2026.07.30-2`，正式書庫版本為 `2026.07.30-8`。

## 正式發布結果

- 第一輪 release QA：757 項，通過。
- 第二輪獨立 QA：598 項，通過；17 個數值節點重算、26 個高風險概念 gate。
- 既有 13 本內容 hash：整合前後完全一致。
- 初版正式書庫：14 本，版本 `2026.07.29-19`。
- 初版 Pages run：`30469780777`。
- 初版 Pages artifact：`8731105330`；digest `sha256:1b20af1baf726d1de0517df4e09c5796354b45f00e0a71c9b606793932b9029d`。
- 初版部署後 artifact 重新下載：23 份本書 HTML、100 題、150 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`。

## 發布後第二次內容審計（v2）

- 正式內容版本：`2026.07.30-2`。
- 內容修正／補強區域：15 個；題庫精確化：12 題。
- 獨立 QA：128 項通過；數值節點重新計算：36 項通過。
- 高風險主題重新判讀：page fault／virtual memory、interrupt／exception、HTTP/3／QUIC／TLS、Big-O／Θ、binary search、foreign key／ACID、cryptographic hash／password KDF、NIST cloud／edge。
- Book ID、章節 ID、題目 ID、題數與進度儲存鍵均未變。
- 所有非目標教材內容 hash 在修正前後完全一致。
- 正式書庫：20 本，版本 `2026.07.30-8`。
- Pages run：`30493970959`；artifact：`8740844265`；digest `sha256:a0d6b573084f870eb4fbd6416d46585ecca5b980f5e35534f2ab676e0c847cf7`。
- 部署後重新下載 artifact：23 份本書 HTML、100 題、150 搜尋、20 SVG 與 v2 QA 全數重驗通過。
