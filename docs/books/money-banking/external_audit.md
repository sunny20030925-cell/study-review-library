# 《貨幣銀行學》External Audit

更新日期：2026-07-30  
Task ID：`money-banking:EA`  
Book ID：`money-banking`  
內容版本：`2026.07.29-2`

## 結論

- External Audit：`passed`
- 審計模式：risk-based sampling
- 路由：Wolfram + 中央銀行官方資料
- Consensus／Scite：未使用；本輪重點為計算與現行制度描述。
- 核心答案錯誤：0
- 需要內容修正／升版：否
- unresolved blocker：0

## 高風險抽查

present/future value、Fisher approximation、bond duration、bank balance sheet／ROA／ROE、simple money-multiplier caveat、準備金、公開市場操作、政策利率與最後貸款者制度。

Wolfram 代表性結果：PV=`10000`、FV=`108160`、Fisher approximation=`4%`、duration price effect=`-2.5%`、bank equity=`80`、ROA=`0.8%`、ROE=`10%`，均與教材一致。

Official primary source：臺灣中央銀行 2026-07 更新的貨幣政策工具與準備金制度資料確認公開市場操作、貼現窗口、存款準備金與選擇性信用管理均屬正式政策工具；公開市場操作是常用操作工具，重貼現率具主要政策利率／最後融通角色。教材沒有把 `1/rr` 簡單乘數當成現代銀行體系的無條件實際貨幣供給倍數。

## 相容性

教材正文、題庫、ID、PWA、閱讀進度與錯題資料均未修改。