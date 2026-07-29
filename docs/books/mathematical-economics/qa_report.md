# 《數理經濟學》QA 報告

更新日期：2026-07-30

## 版本與成品目標

- Book ID：`mathematical-economics`
- 修正版內容版本：`2026.07.30-2`
- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 自製 SVG：20 張。
- 本輪性質：第二次獨立內容審計；不以初版 QA 通過作為正確前提。

## 本輪查出的主要問題

1. KKT 被描述成無條件的一階必要條件，缺少 constraint qualification 前提。
2. homothetic 的定義只寫「單調轉換」，應收斂為「齊次函數的嚴格遞增轉換」。
3. 彈性章放入 `y=Ax^ay^b` 這條刻意自相矛盾的式子，不應把錯誤式本身當核心公式展示。
4. 特徵向量「方向不變」的說法忽略負特徵值會反向、零特徵值會映到零向量；應改成不變的一維子空間／span。
5. 全微分與有限變動近似混在一起，需分清 `dz` 與 `Δz≈...`。
6. 基礎微分工具缺鏈鎖律、乘法與商數法則，對一般數理經濟學課程不完整。
7. 多元最佳化只講 Hessian 定號，欠缺凹性、擬凹性與全域最適判斷的基本連結。
8. 等式限制範例以模糊的「凹化條件」支持最大值，未沿可行切方向說明受限制二階條件。
9. KKT sufficient condition 需要把「凹目標＋凸不等式可行結構」講清楚，並與必要性的 CQ 分開。
10. constrained envelope theorem 只剩影子價格片段，欠缺 `dV/dθ=∂L/∂θ` 的通用寫法。
11. 隱函數定理需要明確指出是「對欲解出的內生變數」的 Jacobian 非奇異。
12. 差分方程的 `|b|=1` 邊界與 `b=-1` 二期循環未交代。
13. 一維連續動態在 `F′(x*)=0` 時線性化不下結論，初版未明示。

## 修正內容

- `ch04`：補 Cramer 法則 `det(A)≠0` 前提。
- `ch05`：重寫特徵方向與二次型曲率的精確敘述。
- `ch06`：補乘法法則、商數法則、鏈鎖律與 Taylor 誤差語意。
- `ch07`：分離 differential 與 finite-change approximation；限定梯度最快上升的 Euclidean 條件。
- `ch08`：精確化 implicit function theorem 的 Jacobian 條件。
- `ch09`：移除矛盾公式，改成 Cobb–Douglas 對數微分與 1.7% 標準例題。
- `ch11`：補 concavity、strict concavity、quasi-concavity 與 Hessian 全域判讀。
- `ch12`：補切空間二階條件／bordered Hessian 定位；重寫 `xy, x+y=10` 的最大值理由。
- `ch13`：補 LICQ／Slater、necessary vs sufficient conditions、完整 stationarity。
- `ch14`：補 constrained envelope theorem 與限制右側影子價格條件。
- `ch15`：homothetic 改為 strictly increasing transformation。
- `ch18`：補 `b=-1`、`|b|=1` 邊界情形。
- `ch19`：補 `F′(x*)=0` 線性化失效情形。
- 題庫：調整 11 題，新增鏈鎖律、對數微分、受限 SOC、KKT CQ、constrained envelope、homothetic、動態邊界等直接測試。

## 第二次獨立 QA gate

修正版 QA 不只比對固定答案，另要求：

- 20 章、3 附錄、100 題、150 搜尋與 20 SVG 結構完整。
- 13 個修正區域的新概念／前提必須實際出現在生成後 HTML。
- 4 組已知舊錯誤文字不得殘留。
- 11 題調整題目逐題核對答案與解析。
- 23 個代表性數值／公式節點重新計算。
- 10 個高風險邏輯 gate 獨立重判。
- 搜尋索引必須同步修正版概念，不能只改正文。
- 導數 prime 的 MathJax 輸出不得殘留 `\\'`。
- 整合前後所有既有教材及既有 assets 的 hash 不得改變。

## 正式發布結果

已完成 canonical `Deploy study library` 正式發布、Pages deployment、artifact 重新下載驗證與結構化 deployment receipt 回寫；以下為正式發布證據。

## 第二次獨立內容審計與正式發布（v2）

- 正式內容版本：`2026.07.30-2`。
- 實質修正／補強區域：13 個；高風險題庫調整：11 題。
- 獨立 QA：855 項通過；數值／公式節點重算：23 項通過；高風險邏輯 gate：10 項通過。
- 20 章內容密度全部達 gate；正文 20 章、3 附錄、100 題、150 搜尋、20 SVG 完整。
- 既有教材內容與既有 assets hash 在整合前後保持一致。
- 正式書庫：21 本，版本 `2026.07.30-9`。
- Pages run：`30494922034`；artifact：`8741187091`；digest `sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`。
- 部署後重新下載 artifact，23 份本書 HTML、100 題、150 搜尋、20 SVG 與完整 v2 QA 全數重驗通過。
