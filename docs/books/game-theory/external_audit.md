# 《賽局理論及應用》External Audit

更新日期：2026-07-30  
Task ID：`game-theory:EA`  
Book ID：`game-theory`  
內容版本：`2026.07.30-2`

## 結論

- External Audit：`passed`
- 審計模式：risk-based sampling
- 主路由：Wolfram
- Consensus／Scite：未使用；抽查集中於形式化均衡、策略與機制設計條件。
- 核心答案錯誤：0
- 需要內容修正／升版：否
- unresolved blocker：0

## 高風險抽查

- 2×2 coordination mixed indifference、zero-sum mixed equilibrium。
- Cournot、entry/backward induction、commitment、Rubinstein bargaining。
- repeated Prisoner's Dilemma grim-trigger threshold。
- Bayesian entry、first-price auction iid-uniform equilibrium。
- signaling IC、PBE 邊界、VCG payment、core／Shapley。

Wolfram 代表性結果：coordination mixed probabilities `0.4/0.6`、zero-sum probabilities `1/2` 與 `1/3`、Cournot `q1=q2=30`／`P=40`／profit=`900`、Rubinstein (δ=.9) 約 `0.5263/0.4737`、grim threshold `δ=1/2`、first-price bid (n=3,v=.9)=`.6`、VCG payment=`80`、對稱三人 Shapley=`30`，均與教材一致。

額外檢查確認教材有區分 Nash equilibrium 與效率、Bayesian Nash 與 PBE，且定理結論未脫離其資訊與均衡假設。

## 相容性

本輪只新增審計證據與狀態；教材正文、題庫、ID、PWA 與使用者資料均不變。