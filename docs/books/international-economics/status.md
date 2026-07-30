# 《國際經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`international-economics`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-20`
- 目前 stage：`PUB`
- Task ID：`international-economics:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：既有 v2 二次內容複核與正式部署證據保留。
- External Audit：`docs/books/international-economics/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋 144 筆、SVG 20 張。
- v2 獨立 QA：1,656／1,656；100 題全數重查、17 題量化重算。
- 已補 H-O 定理群條件、trade welfare、BPM7、CIP/PPP、Marshall–Lerner/J curve 與 Bretton Woods 邊界。

## External Audit

- 結果：`passed`
- 路由：Wolfram + Consensus + IMF/WTO official primary sources。
- 抽查 comparative advantage、tariff/quota、CA、exchange rates、CIP/UIP/PPP、heterogeneous firms、BPM7 與 anti-dumping 法律邊界。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均未變；正式 21 本 artifact 為 `2026.07.30-20`。

## Visual Polish 完成（2026-07-30）

- Task：`international-economics:VP`；結果：`passed`。
- 高價值資產：`國際經濟學貿易模型匯率條件與福利判斷地圖`。
- Canva design ID：`DAHQ4X_5oYU`；可編輯來源：`https://www.canva.com/d/Kn8KqUTKvQn_qh1`。
- PWA 資產：`assets/international-economics-svg/international-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30567646466`；Pages artifact：`8769471948`。
- Artifact digest：`sha256:e03c4f4d56b8b014635c45b33651a4f170c95a0a2548d1997d5c0614eb0c484a`；重新下載 SHA256 完全一致。
- VP validator：`137 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/international-economics/visual_polish.md`。
- 本書已切換至 `international-economics:PUB`。
- 全書庫下一個 Visual Polish target：`industrial-economics`。
