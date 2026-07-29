# 《計算機概論》External Audit

更新日期：2026-07-30  
Task ID：`computer-fundamentals:EA`  
Book ID：`computer-fundamentals`  
內容版本：`2026.07.30-2`

## 結論

- External Audit：`passed`
- 審計模式：risk-based sampling
- 路由：official primary sources + Wolfram calculations
- Consensus／Scite：未使用；本輪技術標準以 RFC／NIST 官方來源優先。
- 核心答案錯誤：0
- 需要內容修正／升版：否
- unresolved blocker：0

## 官方技術來源抽查

- RFC 9293：TCP 提供 reliable、in-order byte-stream service。
- RFC 768：UDP 不保證 delivery／duplicate protection。
- RFC 9114：HTTP/3 使用 QUIC，且 QUIC 與 TLS 1.3 安全層整合。
- NIST SP 800-145：cloud computing 的五項 essential characteristics。
- NIST SP 800-63B-4：password verifier 應採 salted password hashing scheme 並具適當 cost factor。

教材在 TCP/UDP、HTTP/3、cloud、password hashing、virtual memory／page fault、Big-O vs Θ、database keys／ACID 等高風險節點均保留正確邊界。

## Wolfram 計算驗證

代表性重算：binary `11010=26`、hex `FF=255`、`4 KiB=4096 bytes`、8-bit signed range `[-128,127]`、1920×1080×24-bit image=`49,766,400 bits`、2 GHz cycle=`0.5 ns`、AMAT=`5 ns`、100 Mb/s=`12.5 MB/s`、1024 二分減半=`10` 次、99.9% availability 範例均一致。

## 相容性

本輪不改教材、題庫、ID、PWA、離線快取結構或使用者進度資料。