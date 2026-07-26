# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-27

## 書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫，可持續加入新科目。
- 使用者操作限制：只使用平板；不得要求終端機、Git 或電腦檔案管理操作。

## 正式規格

- 已建立 `AGENTS.md`。
- 已建立 `docs/project_knowledge_index.md`。
- 已建立 `docs/content_authoring_spec.md`。
- 新任務必須先依 knowledge index 讀取正式文件。
- 科目本位原則已固定：使用者的主修背景只決定程度與可能範圍，不得主導其他科目的內容、案例與題型。

## 已有書籍

### 大一微積分

- Book ID：`calculus`
- 目前線上版本：`2026.07.27-2`
- 現況：網站功能與第二輪數學 QA 已完成，但內容取向過度偏向經濟學。
- 已確認需修正：
  - 移除「經濟學取向」定位。
  - 核心正文與題庫改回純微積分本位。
  - 經濟學專屬章節與案例不得留在核心進度；若保留，只能成為明確標示的選讀附錄。
  - 補強標準數學課程常見內容與圖形題型。
- 正在進行的正式任務：微積分科目本位重整與重新 QA。

## 下一個新科目流程

1. 新開對話。
2. 使用者只需指定科目。
3. 助理先讀 `AGENTS.md` 與 knowledge index 指定文件。
4. 先建立該科目的 scope/status，再開始製作。
5. 完成兩輪 QA 後加入同一書庫。

## 建議的新對話開頭

> 下一本製作「科目名稱」。請先從 `sunny20030925-cell/study-review-library` 的 `AGENTS.md` 與 knowledge index 讀取正式規格和目前 checkpoint，再開始規劃。

不需要重新貼上本專案的全部歷史要求。
