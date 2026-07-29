from __future__ import annotations

QUESTIONS_B = [
    {'id':'ch10-q01','chapterId':'ch10','question':'IPv4 與 IPv6 位址長度各是多少 bits？','answer':'IPv4 為 32 bits；IPv6 為 128 bits。','explanation':'這是兩個 IP 版本的基本位址長度。'},
    {'id':'ch10-q02','chapterId':'ch10','question':'DNS 的主要工作是什麼？','answer':'把網域名稱解析成 IP 位址等 DNS 記錄。','explanation':'DNS 是分散式名稱系統，不是搜尋引擎。'},
    {'id':'ch10-q03','chapterId':'ch10','question':'TCP 與 UDP 的核心服務差別之一是什麼？','answer':'TCP 提供可靠、有序的位元組串流；UDP 提供較精簡的資料報服務，不自行保證可靠重傳與順序。','explanation':'應比較服務特性，而不是背「誰一定比較快」。'},
    {'id':'ch10-q04','chapterId':'ch10','question':'使用者輸入 https://example.com 後，DNS、TLS 與 HTTP 大致各負責什麼？','answer':'DNS 做名稱解析；TLS 保護連線；HTTP 傳送 Web 請求與回應。','explanation':'三者位於不同功能層次。'},
    {'id':'ch10-q05','chapterId':'ch10','question':'看到 HTTPS 是否代表網站上的資訊一定真實？','answer':'不代表。','explanation':'HTTPS 主要保護傳輸與連線身分驗證，不替內容本身保證正確或可信。'},

    {'id':'ch11-q01','chapterId':'ch11','question':'if 敘述主要屬於順序、選擇還是迭代控制？','answer':'選擇（selection）。','explanation':'if 依條件選擇不同執行路徑。'},
    {'id':'ch11-q02','chapterId':'ch11','question':'for / while 迴圈主要用來做什麼？','answer':'重複執行一組步驟，直到次數完成或條件改變。','explanation':'迴圈是 iteration 的基本工具。'},
    {'id':'ch11-q03','chapterId':'ch11','question':'編譯成功是否保證程式邏輯符合需求？','answer':'不保證。','explanation':'編譯成功通常只表示語法與部分靜態規則通過，仍可能有執行或邏輯錯誤。'},
    {'id':'ch11-q04','chapterId':'ch11','question':'同一個找最大值演算法能不能用 Python、C 或 Java 等不同語言實作？','answer':'可以。','explanation':'演算法是解題方法，程式語言是實作與表達工具。'},
    {'id':'ch11-q05','chapterId':'ch11','question':'「某語言天生只能編譯、絕不可能使用直譯或 JIT」這種說法通常是否過度簡化？','answer':'是。','explanation':'語言規格與具體實作要分開；同一語言可有不同執行策略。'},

    {'id':'ch12-q01','chapterId':'ch12','question':'線性搜尋最壞情況的時間複雜度通常是多少？','answer':'O(n)。','explanation':'最壞可能檢查 n 個元素。'},
    {'id':'ch12-q02','chapterId':'ch12','question':'1024 個已排序元素用二分搜尋，最壞大約需要多少次把範圍減半？','answer':'約 10 次。','explanation':'2^10=1024，所以約 log₂1024=10。'},
    {'id':'ch12-q03','chapterId':'ch12','question':'二分搜尋可以直接套在任何未排序陣列上並保證 O(log n) 嗎？','answer':'不可以。','explanation':'二分搜尋需要可利用的有序結構與合適存取方式。'},
    {'id':'ch12-q04','chapterId':'ch12','question':'若演算法 A 是 O(n)，B 是 O(n log n)，是否能保證任何小 n 的實測 A 都較快？','answer':'不能。','explanation':'Big-O 描述漸近成長，常數因子、硬體與輸入分布仍會影響實測。'},
    {'id':'ch12-q05','chapterId':'ch12','question':'O(n) 是否表示演算法一定「剛好做 n 次」操作？','answer':'不是。','explanation':'Big-O 是漸近上界／成長等級，不是精確操作次數。'},

    {'id':'ch13-q01','chapterId':'ch13','question':'後進先出（LIFO）對應 stack 還是 queue？','answer':'Stack。','explanation':'Stack 的典型操作是 push 與 pop，最後放入的先取出。'},
    {'id':'ch13-q02','chapterId':'ch13','question':'先進先出（FIFO）對應 stack 還是 queue？','answer':'Queue。','explanation':'Queue 先 enqueue 的元素通常先 dequeue。'},
    {'id':'ch13-q03','chapterId':'ch13','question':'80 筆資料、100 個 buckets，load factor α 為多少？','answer':'0.8。','explanation':'α=80/100=0.8。'},
    {'id':'ch13-q04','chapterId':'ch13','question':'函式呼叫與返回順序更適合用 stack 還是 queue 模型？','answer':'Stack。','explanation':'最近呼叫的函式通常最先返回，符合 LIFO。'},
    {'id':'ch13-q05','chapterId':'ch13','question':'雜湊表是否能保證任何資料、任何情況查找都為 O(1)？','answer':'不能。','explanation':'碰撞、負載與實作會影響效能；平均常很快，但最壞情況可能退化。'},

    {'id':'ch14-q01','chapterId':'ch14','question':'Primary key 的核心作用是什麼？','answer':'唯一識別資料表中的資料列。','explanation':'主鍵不是「最重要欄位」的主觀稱呼，而是識別性約束。'},
    {'id':'ch14-q02','chapterId':'ch14','question':'Foreign key 是否一定必須唯一？','answer':'不一定。','explanation':'多筆資料可以引用同一筆父表資料，因此外鍵常可重複。'},
    {'id':'ch14-q03','chapterId':'ch14','question':'ACID 的 D（Durability）表示什麼？','answer':'交易一旦成功提交，其結果應能持久保存，即使之後系統發生故障。','explanation':'Durability 關心 committed data 的持久性。'},
    {'id':'ch14-q04','chapterId':'ch14','question':'SQL 的 SELECT、FROM、WHERE 大致分別負責什麼？','answer':'SELECT 指定要取的欄位／運算；FROM 指定資料來源；WHERE 篩選資料列。','explanation':'這是基本查詢骨架。'},
    {'id':'ch14-q05','chapterId':'ch14','question':'正規化是否等於把資料表拆得越多越好？','answer':'不是。','explanation':'正規化是依相依關係降低重複與異常，仍需考慮實際設計與查詢需求。'},

    {'id':'ch15-q01','chapterId':'ch15','question':'Regression test 的主要目的為何？','answer':'確認修改後既有功能仍然正常。','explanation':'回歸測試防止修新問題時破壞舊功能。'},
    {'id':'ch15-q02','chapterId':'ch15','question':'API 最主要描述什麼？','answer':'軟體元件對外提供的操作、資料格式與互動契約。','explanation':'API 讓不同元件能依穩定介面協作。'},
    {'id':'ch15-q03','chapterId':'ch15','question':'一個有效 test case 至少應包含哪兩類資訊？','answer':'輸入／前提與可判定的 expected behavior。','explanation':'只有「跑一下」而沒有預期結果，無法可靠判定通過或失敗。'},
    {'id':'ch15-q04','chapterId':'ch15','question':'版本控制中的 branch 主要用途是什麼？','answer':'讓一條變更線與其他工作暫時分開發展，再視需要比較或合併。','explanation':'分支支援平行開發與隔離變更。'},
    {'id':'ch15-q05','chapterId':'ch15','question':'所有自動測試都通過，是否能證明軟體不存在任何 bug？','answer':'不能。','explanation':'測試只能對已覆蓋的情境提供證據，無法窮舉所有可能輸入與環境。'},

    {'id':'ch16-q01','chapterId':'ch16','question':'檔案被未授權修改主要傷害 CIA 中哪一項？','answer':'Integrity（完整性）。','explanation':'完整性要求資料未被未授權竄改。'},
    {'id':'ch16-q02','chapterId':'ch16','question':'驗證「你是不是這個帳號本人」屬 authentication 還是 authorization？','answer':'Authentication。','explanation':'認證回答身分；授權回答能做什麼。'},
    {'id':'ch16-q03','chapterId':'ch16','question':'判斷某已登入使用者能否刪除管理資料屬 authentication 還是 authorization？','answer':'Authorization。','explanation':'此時身分已知，要判斷其操作權限。'},
    {'id':'ch16-q04','chapterId':'ch16','question':'Hashing 與 encryption 的核心差異之一是什麼？','answer':'加密設計為持有金鑰可逆；一般密碼學雜湊是單向映射，不用來還原原文。','explanation':'兩者用途與安全性質不同。'},
    {'id':'ch16-q05','chapterId':'ch16','question':'為什麼密碼儲存通常要加 salt 並使用專門的慢速 KDF／password hash？','answer':'降低預先計算與大量猜測攻擊效率，讓相同密碼也不直接產生相同儲存值。','explanation':'Salt 應隨機且每筆不同；KDF 則提高猜密碼成本。'},

    {'id':'ch17-q01','chapterId':'ch17','question':'AI 與 machine learning 的關係為何？','answer':'Machine learning 是 AI 領域中的一類方法；AI 的範圍更廣。','explanation':'不能把兩者完全畫上等號。'},
    {'id':'ch17-q02','chapterId':'ch17','question':'Training 與 inference 的核心差別是什麼？','answer':'Training 用資料調整模型參數；inference 用已訓練模型處理新輸入。','explanation':'兩者是模型生命週期中的不同階段。'},
    {'id':'ch17-q03','chapterId':'ch17','question':'100 筆測試資料預測正確 90 筆，accuracy 是多少？','answer':'90%。','explanation':'accuracy=90/100=0.9。'},
    {'id':'ch17-q04','chapterId':'ch17','question':'類別極度不平衡時，單看 accuracy 是否可能誤導？','answer':'可能。','explanation':'模型可能只猜多數類就得到很高 accuracy，因此要看 precision、recall 等其他指標與任務成本。'},
    {'id':'ch17-q05','chapterId':'ch17','question':'生成式 AI 回答很流暢，是否足以證明內容是真實且已查證？','answer':'不足。','explanation':'生成式模型做機率式推論，輸出仍可能錯誤、過時或帶偏誤，需要外部來源驗證。'},

    {'id':'ch18-q01','chapterId':'ch18','question':'Cloud computing 是否只是「租一台遠端電腦」的同義詞？','answer':'不是。','explanation':'雲端更強調共享資源池、按需求配置、服務化與彈性等特性。'},
    {'id':'ch18-q02','chapterId':'ch18','question':'某月共 43,200 分鐘，服務停機 43.2 分鐘，availability 約多少？','answer':'99.9%。','explanation':'可用時間 43,156.8 分鐘，除以 43,200 = 0.999。'},
    {'id':'ch18-q03','chapterId':'ch18','question':'Edge computing 為什麼可能降低延遲？','answer':'因為把部分計算放到更接近使用者或資料來源的位置，減少必須往返遠端資料中心的路徑與等待。','explanation':'邊緣也可能節省頻寬並提高斷線時的局部自主性。'},
    {'id':'ch18-q04','chapterId':'ch18','question':'把服務分散到更多節點是否只會增加好處、不增加新的困難？','answer':'不是。','explanation':'分散式系統還要處理網路延遲、部分故障、一致性與協調。'},
    {'id':'ch18-q05','chapterId':'ch18','question':'Availability 高是否等於資料一定正確、服務一定安全？','answer':'不等於。','explanation':'可用性只描述服務可提供的程度；正確性與安全性是不同品質屬性。'},

    {'id':'ch19-q01','chapterId':'ch19','question':'Open source software 是否等於沒有著作權？','answer':'不等於。','explanation':'開源通常仍受著作權保護，只是權利人以授權條款允許特定使用、修改與散布。'},
    {'id':'ch19-q02','chapterId':'ch19','question':'Data minimization 的核心原則是什麼？','answer':'只蒐集與保留達成明確目的所必要的資料。','explanation':'資料越多不代表系統越負責任；不必要資料還會增加隱私與外洩風險。'},
    {'id':'ch19-q03','chapterId':'ch19','question':'刪掉姓名後，資料是否必然已完全匿名且永遠無法重新識別？','answer':'不必然。','explanation':'其他欄位與外部資料仍可能組合出身分，因此匿名化需評估重新識別風險。'},
    {'id':'ch19-q04','chapterId':'ch19','question':'一個演算法計算答案完全正確，是否代表整個資訊系統就一定負責任？','answer':'不是。','explanation':'還要考慮隱私、安全、公平、可近用性、授權、資料品質與使用情境。'},
    {'id':'ch19-q05','chapterId':'ch19','question':'系統出現「網頁打不開」時，為什麼不應立刻只怪應用程式？','answer':'因為問題可能位於 DNS、網路、TLS、伺服器、作業系統、資料或應用等不同層。','explanation':'計算機概論的系統觀要求先定位故障層次，再進一步診斷。'},
]
