# 《高等統計學》第二次內容審計發現

日期：2026-07-30

本文件記錄 v1 正式發布後的獨立內容審計發現；正式修正版目標為 `2026.07.30-1`。

## 實際發現

1. **充分性／完備性關係表述不精確**：v1 以「完備性比充分性更強」概括兩者，容易誤導為一般蘊含關係。修正為：兩者是不同性質，一般互不推出；「完備且充分」表示同時具備兩項條件。
2. **Negative Binomial 覆蓋不足**：章名與 scope 已列入，但正文只有名稱，未給支撐、PMF、期望、變異數與參數化差異。v2 補齊。
3. **多元常態條件分布條件不足**：補明公式需要聯合常態與 `Var(X)>0`；只有兩個邊際常態不足以套用。
4. **Slutsky 僅列名詞未正式講授**：補正式敘述、studentization 例與 Delta method 一階導數為 0 時的退化提醒。
5. **MLE invariance 缺漏**：scope 已列但 v1 正文未教，v2 補參數轉換不變性與例題。
6. **估計量大樣本性質不足**：補一致性、漸近常態、Bernoulli Fisher information 的內點條件與 Rao–Blackwell 的有限二階矩語境。
7. **z／t 信賴區間的精確與近似需再分清**：補常態母體、已知／未知 sigma、S² 定義及 CLT 近似邊界。
8. **size 與 level 未分開**：補 `size=sup_{theta in Theta0} Ptheta(reject)` 與 `level alpha` 只要求 `size<=alpha`；p-value 補 composite null／nuisance parameter 校準，NP 補離散 randomization。
9. **UMP／Wilks 條件可再精確**：補 MLR／Karlin–Rubin；Wilks 補 H0、正則巢狀、可識別、內點條件與非正則邊界例外。
10. **Gauss–Markov 與精確 F 條件可再精確**：補條件於 X 的零條件平均、球形條件變異、full rank，以及精確 F 的 normal-error 條件與自由度定義。

## 相容性

- 20 章、3 附錄、100 題、189 搜尋、20 SVG 均不改數量。
- `ch00`–`ch19` 全部章節 ID 不變。
- 100 個 question ID 全部不變；其中 7 題內容／詳解調整。
- 不改既有儲存鍵，因此閱讀進度與錯題紀錄相容。
- 正式整合必須證明其他教材內容與資產逐檔 hash 不變。
