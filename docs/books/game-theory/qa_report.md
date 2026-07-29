# 《賽局理論及應用》QA 報告

更新日期：2026-07-29

## 目前狀態

- 內容版本：`2026.07.29-1`。
- 第一輪候選驗證：PASS。
- 第二輪獨立內容複核：PASS。
- 正式部署：尚未執行；必須等來源 PR 合併後，以最新 `main` 與最新正式 Pages artifact 序列整合。

## 第一輪候選驗證

GitHub Actions run：`30468164830`

結果：

- `GAME_THEORY_QA_OK checks=2385`
- 候選基底：12 本正式書庫，候選加入後 13 本。
- 候選 library version：`2026.07.29-18`（僅隔離驗證用，正式發布仍須重新由最新書庫計算）。
- 20 章、3 附錄、100 題、189 筆搜尋、20 張 SVG 全部通過。
- 34 個高風險答案 gate 全部通過。
- 每章固定 5 題；difficulty 分布為基礎 20、標準 40、綜合 20、陷阱 20。
- Python source、共同 `app.js`、`sw.js` 語法通過。
- 候選產生前後，既有書籍逐檔 SHA-256 無差異。
- 平板端 23 個章節／附錄 HTML、20 個 SVG、100 題與搜尋檔案路徑全部存在。

## 第二輪獨立內容複核

同一成功 run 另執行 `qa_game_theory_second_pass.py`，不是重跑第一輪 validator。

結果：

- `GAME_THEORY_SECOND_PASS_OK checks=360`
- 獨立重算 24 個數值節點：混合策略、zero-sum、Cournot、Rubinstein bargaining、grim-trigger 折現門檻、Bayesian 期望值、第一價拍賣、Bayes posterior、signaling IC、screening utility、VCG 與 cooperative-game core。
- 另做 19 個概念陷阱 gate：weak dominance、Nash 與效率、mixed-strategy 無差異方向、minimax 適用範圍、SPNE、Nash bargaining、folk theorem、Bayesian strategy、auction assumptions、PBE beliefs、equilibrium refinement、signaling/screening、mechanism properties、Shapley/core、social optimum、complete/perfect information。
- 100 題題幹唯一、題目 ID 唯一，每題詳解皆通過最低推理完整度 gate。

## 第二輪找到並修正的內容

第二輪不是零缺陷直接放行；實際抓到 5 題詳解過短，已補強：

- `ch05-q01`：補足零和報酬 `v` 與 `-v` 的關係與理由。
- `ch08-q04`：補明承諾投資已扣成本後的淨報酬比較。
- `ch09-q03`：補明 Rubinstein 份額乘上 NT$100 的換算與模型來源。
- `ch14-q02`：補明 signaling 高型態的工資減教育成本與 IC 用途。
- `ch16-q04`：補明準線性 VCG 效用為價值減支付。

另有兩次早期 CI 失敗屬 validator 假陽性：

- 把「Shapley value 一定在 core；一般賽局不保證」的反例提醒誤抓為過度宣稱。
- 把 Bayesian strategy 的「型態映到行動」等價表述誤判為缺少固定字串。

兩者都修正檢查器而未扭曲教材文字。

## 精確性結論

目前核心精確性 gate 已確認：

- Nash equilibrium 不等於效率、公平、唯一或社會最佳。
- 嚴格與弱劣勢刪除分開處理，弱劣勢順序可能影響結果。
- 混合策略以對手無差異條件求自己的混合機率。
- minimax theorem 不泛化至一般總和賽局。
- SPNE 必須在每個真正子賽局皆為 Nash。
- finite／infinite repeated games 與折現條件分開。
- Bayesian strategy 是 type→action 的完整映射。
- PBE 同時包含 strategy、belief、Bayes consistency 與 sequential rationality。
- auction 結論明示 private/common value、risk neutrality 等適用條件。
- Nash bargaining solution 與 Rubinstein equilibrium 不混稱。
- IC、IR、efficiency、budget balance 分開檢查。
- core、Shapley value 與 non-cooperative Nash equilibrium 不互相替代。

## 已知範圍限制

- fixed-point existence proof、高階 equilibrium refinement、Myerson optimal auction、完整 implementation theory、algorithmic game theory 等維持選讀／範圍外，不進核心題庫。
- 應用案例只服務賽局結構理解，不取代個體經濟學、產業組織、財務或政治學專門課程。
