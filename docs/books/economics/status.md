# 《經濟學原理》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`economics`
- 正式內容版本：`2026.07.27-2`
- 正式書庫版本：`2026.07.30-28`
- 目前 stage：`PUB`
- Task ID：`economics:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：既有發布後獨立糾錯複核與 1,333／1,333 QA。
- External Audit：`docs/books/economics/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 144 筆、SVG 20 張。
- 正文／附錄修正 14 處、題庫 6 題同步修正；100 題重新檢查，代表性數值題獨立重算。

## External Audit

- 結果：`passed`
- 路由：Wolfram。
- 抽查供需、elasticity、budget、comparative advantage、tax/subsidy、welfare/externality、basic multiplier 與 BOP 基礎關係。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`economics:VP`；結果：`passed`。
- 高價值資產：`經濟學原理衝擊曲線均衡福利與政策判斷地圖`。
- Canva design ID：`DAHQ5KUGsYE`；可編輯來源：`https://www.canva.com/d/MugMiO_8aGO0Myb`。
- PWA 資產：`assets/economics-svg/ppf.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30587535167`；Pages artifact：`8777075509`。
- Artifact digest：`sha256:7b1b17a635fbc393947b7f0c1c6ab05a6f54362a2c6b38e0ea39118d24664234`；重新下載 SHA256 完全一致。
- VP validator：`84 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/economics/visual_polish.md`。
- 本書已切換至 `economics:PUB`。
- 全書庫下一個 Visual Polish target：`computer-fundamentals`。
