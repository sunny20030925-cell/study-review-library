# 《財政學》QA 報告

更新日期：2026-07-29

## 版本與正式狀態

- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-1`
- 正式書庫版本：`2026.07.29-14`
- 正式書庫順位：第 11 本。
- 狀態：兩輪內容 QA、canonical-tail preflight、正式 Pages artifact 終檢均完成；已部署。

## 成品範圍

- 正文：20 章（`ch00`–`ch19`）
- 附錄：3 份
- 題庫：100 題，每章 5 題
- 搜尋索引：189 筆
- 圖解：20 張自製 SVG

## 第一輪製作內檢

- 科目範圍與一般大學財政學／公共經濟學共同核心一致。
- 公共財、外部性、公共選擇、成本效益、所得分配、社會保險、醫療與教育支出均有正文、公式條件、例題、常見錯誤與理解檢查。
- 租稅篇區分法定歸宿與經濟歸宿、稅收與無謂損失、平均與邊際稅率、純效率 Ramsey 直覺與分配限制。
- 地方財政區分一般補助與配合補助；公債區分赤字 flow、債務 stock、初級盈餘與債務比動態。
- 一般金額例題使用 `NT$`；債務比變動明確使用「GDP 百分點」。
- 避免把當年度臺灣稅率、扣除額、申報門檻寫成固定核心知識；VAT 數字例明示為假設機制示範。
- 不把 IS–LM、AD–AS、DSGE 或完整總體財政政策模型納入財政學核心正文。

## 第二輪獨立內容複核

- 20／20 章核心定義、公式、成立條件與兩段式例題重新核對。
- 100／100 題重新檢查題幹、答案與詳解；每章 5 題保留基礎理解、標準計算／判斷、綜合與陷阱型題目。
- 高風險方向另外交叉核對：Samuelson 公共財條件、Pigouvian 邊際矯正概念、Coase 條件、租稅歸宿的相對彈性、DWL 與稅收區分、Ramsey 逆彈性規則的限制、公司稅法定／經濟歸宿，以及 `Δb≈(r-g)b-ps` 的正負號與近似性質。
- 數值例題與題庫由原始數值重新計算；NPV、教育投資現值、PAYG、共同保險、租稅歸宿、DWL、EMTR、利息稅盾、VAT、配合款與債務比動態結果一致。
- 未發現需改變財政學理論答案的內容錯誤。

## 第二輪抓到並修正的工程問題

- 原候選題庫缺少正式平板介面會使用的 `bookId`、`chapterTitle`、`topic`、`difficulty`、`source`；已補齊。
- 原 manifest 章節缺少顯示用 `number`；已補齊 0–19 與附錄 A–C。
- 原 validator 以子字串攔錯誤敘述，會把正確句「不能假設政府介入必然改善」誤判成錯；已改為只攔完整錯誤斷言。
- 題庫難度固定為每章 `基礎／標準／標準／綜合／陷阱`，全書分布 20／40／20／20。

## 高風險答案與公式自動門檻

固定重查 40 個高風險答案；其中數值題另由原始數值重新計算。涵蓋：

- 社會淨效益與總剩餘
- MPC／MEC／MSC 與 Pigouvian 稅
- 中位數選民位置
- NPV 與教育投資現值
- 貧窮率、替代率、共同保險自付
- 平均稅率、租稅歸宿比例
- DWL 與稅收
- Ramsey 逆彈性比例
- EMTR、扣除與抵免
- 公司利息稅盾
- VAT 銷項／進項扣抵
- 配合款地方自付額
- `Δb≈(r-g)b-ps` 債務比動態

## 候選與正式整合驗證

### 早期候選整合

- Run `30442363064`：以 9 本／`2026.07.29-12` 正式 artifact 做候選整合。
- 結果：`PUBLIC_FINANCE_QA_OK checks=2383`，20 章、3 附錄、100 題、189 搜尋、20 SVG、40 個高風險答案全部通過。
- 這一輪只證明教材候選本身可整合；後續因《國際經濟學》先正式發布，沒有拿這份舊 9 本基底直接上線。

### 最新正式 10 書 canonical-tail preflight

- PR `#70` / Run `30443068402`。
- 基底：正式 10 本、書庫 `2026.07.29-13`，尾端為 `macroeconomics` → `international-economics`。
- 結果：成功生成 11 本／`2026.07.29-14`，尾端為 `macroeconomics` → `international-economics` → `public-finance`。
- 財政學 validator：2,383 項通過；40 個高風險答案重查通過。
- 總體經濟學尾端整合 QA：265 項通過。
- 原 10 本教材檔案 SHA-256 前後一致；`app.js`、`sw.js` 語法檢查通過；財政學平板資產路徑通過。

## 正式 Pages artifact 終檢

- 正式 canonical run：`30443143611`
- Source commit：`6babc326c5f8ae3ceed363466248c50c51ceecd6`
- Pages artifact：`8720289195`
- Artifact digest：`sha256:4193fede294a374210549df3e71161681e63b654956c1207a38d0f5112803215`
- Workflow 的 Upload Pages artifact 與 Deploy to GitHub Pages 步驟均成功；Pages 在 `2026-07-29T10:18:44.896999+00:00` 回報成功。
- 正式 artifact 重新下載後確認：書庫版本 `2026.07.29-14`、11 本書、財政學 23 份章節／附錄、100 題、189 搜尋索引、20 SVG 全部存在。
- 題庫正式 schema、章節顯示編號與 service-worker 離線快取均存在。

## 部署記錄器已知工程瑕疵

- 正式網站部署本身成功後，最後 `Record successful deployment` 步驟因舊寫回器仍尋找舊 checkpoint 格式 `### 個體經濟學`，而現行 checkpoint 已使用編號標題，造成 `microeconomics checkpoint section not found`。
- 此錯誤發生在 Pages 成功之後，沒有改變正式 artifact 或網站內容。
- `docs/deployment_receipt.json` 已依正式 Pages artifact、artifact digest 與部署 log 以 `[skip ci]` 校正；回條明確保留 `workflow_overall_conclusion=failure-after-successful-pages-deploy` 與 recorder failure，不把工程問題偽裝成全綠。
- 後續新增教材前，應把 canonical post-deploy recorder 改成依 Book ID／現行 checkpoint 結構更新，而不是依舊標題與舊句子做字串匹配。

## 最終結論

《財政學》內容、題庫、搜尋、圖解、平板 schema、既有書籍保護與正式 Pages artifact 均通過本次要求；正式網站已是 11 本／`2026.07.29-14`。部署後文件記錄器仍有一項獨立工程技債，但不影響本次已發布教材內容。
