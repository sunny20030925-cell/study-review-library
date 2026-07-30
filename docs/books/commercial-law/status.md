# 《商事法》製作狀態

更新日期：2026-07-30

## 版本

- Book ID：`commercial-law`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-11`
- 正式分支：`main`
- 法規基準：2026-07-29 複核之現行公司法、證券交易法與公開發行公司董事會議事辦法。

## 已固定範圍

- 課程主軸：公司法＋證券交易法。
- 公司法：以股份有限公司為主，補有限公司、閉鎖性股份有限公司與必要關係企業概念。
- 證券交易法：募集／發行／私募、資訊揭露、公開發行公司治理、證券詐欺、財報不實、操縱市場、短線交易與內線交易。
- 票據法、保險法、海商法不進入核心正文與核心題庫。
- 成品：18 章、3 附錄、90 題、111 筆搜尋索引、18 張 SVG，整合既有平板 PWA。

## 完成狀態

- 初版第一輪 QA：完成。
- 初版第二輪獨立法律複核：完成。
- 發布後獨立內容複核：完成；正文、3 附錄與 90 題重新檢查。
- 發布後實質修正：共記錄 13 次內容修正事件；6 個題目 ID 依法律精確化同步調整。
- 公司法第 8 條 follow-up：完成。`2026.07.29-1` 曾誤採舊法「公開發行股票之公司」限制；經最終查核現行公司法與修法沿革後，已由 `2026.07.29-2` 立即回修為現行一般規則。
- 第 8 條獨立重新生成驗證：版本、18 章、3 附錄、90 題、每章 5 題、111 搜尋，以及現行法主體／實質執行／實質控制／不得限縮為公開發行公司等檢查全部通過。
- QA 報告：`docs/books/commercial-law/qa_report.md`。
- 正式入口：`https://sunny20030925-cell.github.io/study-review-library/`。
- 部署回條：`docs/deployment_receipt.json`。
- 閱讀進度：章節 ID、題目 ID 與題數未變，`progress_storage_changed=false`。

## Visual Polish 執行中（2026-07-30）

- Task：`commercial-law:VP`。
- 已核准並正式儲存 Canva 高價值資產：《商事法案例題雙軌判斷地圖》。
- Canva design ID：`DAHQ2c1bRXE`；可編輯來源：`https://www.canva.com/d/tW8J87KlNJIiXkN`。
- PWA 實作 PR：#154，merge SHA `2261c0f4e638bf516c4b79079a22a1900e5d14ad`。
- 預定正式資產：`assets/commercial-law-svg/law-map.svg`；沿用既有 cache URL，SVG 總數維持 18。
- 本地正式 artifact 模擬：library `2026.07.30-11 → 2026.07.30-12`；第二次套用維持 `-12`；VP validator `59 checks` PASS。
- PR #154 合併後 canonical `Deploy study library` run `30531864083` 已成功；artifact `8755007481`、digest `sha256:11f3b4ddf80f32e9232244839fcecef119acb6ff7b8037f731a8c4324ee82129` 重下載驗證通過。
- canonical artifact 仍為 VP 前基底 `2026.07.30-11`；`Apply commercial law Visual Polish` follow-up 尚未留下正式 deployment recorder，因此 **VP 尚不得標記 passed，也不得提前切換 PUB**。
- 這段狀態只記錄正式部署中的中間節點；成功部署後會由 closure PR 改寫為最終 `PUB` 狀態。

## 主要修正

1. 公司法第 8 條第 3 項：現行法不限於公開發行公司；公司之非董事符合實質執行董事業務或實質控制並指揮董事等要件時，原則上與董事同負相應責任，並保留法定政府指揮例外。
2. 補入已依證券交易法發行股票之公司董事會不得少於 5 人。
3. 區分公司法董事會一般 3 日通知與公開發行公司董事會原則 7 日通知。
4. 補入利害關係董事有害公司利益之虞時的表決排除及表決權數效果。
5. 公司法第 194 條補入繼續持股 1 年以上門檻，與第 214 條代表訴訟門檻分離。
6. 閉鎖性公司 50 人基本上限補入主管機關增加上限的法定例外。
7. 閉鎖性公司技術／勞務出資補入全體股東同意、章程記載與勞務比例限制。
8. 短線交易補入其他具有股權性質之有價證券及第 62 條證券商營業處所準用。
9. 內線交易補入重大影響公司支付本息能力消息所涉及的非股權性質公司債規則。
10. 附錄同步補正董事規則、股東救濟與短線交易速查。
11. 90 題全數重新複核；6 個題目 ID 依上述法律精確化同步調整，題目 ID 不變。
12. 正式部署 gate 新增高風險法律要件、現行公司法第 8 條要件及禁止舊法誤述檢查。

## 發布結果（既有內容版本）

1. canonical `Deploy study library` 持續統一生成並驗證正式書庫。
2. 商事法 `2026.07.29-2` 的 18 章、3 附錄、90 題、111 筆搜尋索引、18 張 SVG、版本 UI、搜尋、題庫與離線快取維持既有 gate。
3. 部署回條記錄 `commercial_law_content_correction_count=13`、`commercial_law_question_adjustment_count=6`、`commercial_law_followup_correction_count=1`、`commercial_law_post_publication_reaudit=passed-after-current-law-followup`。
4. Visual Polish 正式成功證據須另以 follow-up Pages artifact 與 `docs/books/commercial-law/visual_polish.md` 為準。
