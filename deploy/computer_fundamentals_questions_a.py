from __future__ import annotations

QUESTIONS_A = [
    {'id':'ch00-q01','chapterId':'ch00','question':'作業系統屬於硬體還是軟體？','answer':'軟體。','explanation':'作業系統是管理硬體資源並提供應用程式介面的系統軟體。'},
    {'id':'ch00-q02','chapterId':'ch00','question':'下列流程何者最接近一般資訊處理主線：輸入→處理→輸出→儲存，還是輸出→輸入→硬體→人員？','answer':'輸入→處理→輸出→儲存。','explanation':'這是理解資料從進入系統到形成結果並保存的基本框架。'},
    {'id':'ch00-q03','chapterId':'ch00','question':'演算法與程式的關係為何？','answer':'演算法是解題步驟；程式是用程式語言等形式把演算法實作成可執行的表示。','explanation':'同一演算法可以用不同程式語言實作。'},
    {'id':'ch00-q04','chapterId':'ch00','question':'網路購物平台除了伺服器硬體，至少還包含哪些資訊系統要素？','answer':'軟體、資料、人員、程序與通訊網路。','explanation':'資訊系統不是單一電腦，而是多種技術與人／程序共同完成目的。'},
    {'id':'ch00-q05','chapterId':'ch00','question':'「計算機科學就是學會使用現成軟體」是否正確？','answer':'不正確。','explanation':'計算機科學還研究資料表示、演算法、程式、系統、網路、安全與計算方法等核心問題。'},

    {'id':'ch01-q01','chapterId':'ch01','question':'1 byte 等於多少 bits？','answer':'8 bits。','explanation':'byte 通常定義為 8 bits。'},
    {'id':'ch01-q02','chapterId':'ch01','question':'11010₂ 等於多少十進位？','answer':'26。','explanation':'16+8+2=26。'},
    {'id':'ch01-q03','chapterId':'ch01','question':'FF₁₆ 等於多少十進位？','answer':'255。','explanation':'15×16+15=255。'},
    {'id':'ch01-q04','chapterId':'ch01','question':'12 bits 可以形成多少種不同位元樣式？','answer':'4096 種。','explanation':'n bits 有 2^n 種樣式；2^12=4096。'},
    {'id':'ch01-q05','chapterId':'ch01','question':'4 KiB 是否等於 4000 bytes？','answer':'不是，4 KiB = 4096 bytes。','explanation':'KiB 是 IEC 二進位前綴，1 KiB=1024 B；kB 才是 SI 的 1000 B。'},

    {'id':'ch02-q01','chapterId':'ch02','question':'8-bit 無號整數的最大值是多少？','answer':'255。','explanation':'2^8−1=255。'},
    {'id':'ch02-q02','chapterId':'ch02','question':'8-bit 二補數有號整數的範圍是多少？','answer':'−128 到 127。','explanation':'n-bit 二補數範圍為 −2^(n−1) 到 2^(n−1)−1。'},
    {'id':'ch02-q03','chapterId':'ch02','question':'同一個 11111111₂ 若按 8-bit 無號與二補數有號解讀，值各是多少？','answer':'無號是 255；二補數有號是 −1。','explanation':'位元樣式本身沒有唯一數值意義，需看資料格式。'},
    {'id':'ch02-q04','chapterId':'ch02','question':'1920×1080、24 bits/pixel 的未壓縮影像約有多少 bits？','answer':'49,766,400 bits。','explanation':'1920×1080×24=49,766,400 bits，約 49.8 Mbits。'},
    {'id':'ch02-q05','chapterId':'ch02','question':'「浮點數可以精確表示所有實數」是否正確？','answer':'不正確。','explanation':'浮點格式只有有限位元，許多實數只能近似表示。'},

    {'id':'ch03-q01','chapterId':'ch03','question':'A=1、B=0 時，A AND B 的輸出是多少？','answer':'0。','explanation':'AND 要所有輸入都是 1 才輸出 1。'},
    {'id':'ch03-q02','chapterId':'ch03','question':'A=1、B=0 時，A XOR B 的輸出是多少？','answer':'1。','explanation':'XOR 在兩個輸入不同時輸出 1。'},
    {'id':'ch03-q03','chapterId':'ch03','question':'半加器輸入 A=1、B=1 時，Sum 與 Carry 各是多少？','answer':'Sum=0，Carry=1。','explanation':'Sum=A XOR B=0；Carry=A AND B=1，所以結果為二進位 10。'},
    {'id':'ch03-q04','chapterId':'ch03','question':'條件「已登入 AND（管理員 OR 擁有者）」中，若未登入但同時是擁有者，整體條件為真嗎？','answer':'不為真。','explanation':'括號內雖為真，但最外層還要與「已登入」做 AND；False AND True=False。'},
    {'id':'ch03-q05','chapterId':'ch03','question':'一般 OR 與 XOR 是否相同？','answer':'不同。','explanation':'兩輸入都為 1 時 OR 輸出 1，但 XOR 輸出 0。'},

    {'id':'ch04-q01','chapterId':'ch04','question':'CPU 中主要執行算術、比較與位元邏輯的是哪個元件？','answer':'ALU（算術邏輯單元）。','explanation':'ALU 負責基本算術與邏輯運算。'},
    {'id':'ch04-q02','chapterId':'ch04','question':'某 CPU 時脈 2 GHz，一個 clock cycle 約多少秒？','answer':'0.5 ns，也就是 5×10^-10 秒。','explanation':'cycle time=1/(2×10^9)=0.5 ns。'},
    {'id':'ch04-q03','chapterId':'ch04','question':'某程式需 10^9 指令，平均 CPI=2，CPU 時脈 2 GHz，簡化 CPU time 約多少？','answer':'約 1 秒。','explanation':'10^9×2×0.5 ns=1 秒。'},
    {'id':'ch04-q04','chapterId':'ch04','question':'若 CPU A 為 3 GHz、CPU B 為 2 GHz，可以只憑時脈斷定 A 跑任何程式都比較快嗎？','answer':'不可以。','explanation':'還要看指令數、CPI、核心、快取、記憶體、軟體與工作負載。'},
    {'id':'ch04-q05','chapterId':'ch04','question':'ISA 與某一顆實體 CPU 型號是完全相同的概念嗎？','answer':'不是。','explanation':'ISA 是軟體可見的指令與架構介面；同一 ISA 可以有許多不同微架構與處理器型號。'},

    {'id':'ch05-q01','chapterId':'ch05','question':'RAM 通常是揮發性還是非揮發性？','answer':'通常是揮發性。','explanation':'一般主記憶體斷電後不保留內容。'},
    {'id':'ch05-q02','chapterId':'ch05','question':'快取命中率 95% 時，miss rate 是多少？','answer':'5%。','explanation':'Miss Rate=1−Hit Rate=5%。'},
    {'id':'ch05-q03','chapterId':'ch05','question':'Hit Time=1 ns、Miss Rate=5%、Miss Penalty=80 ns，AMAT 約多少？','answer':'5 ns。','explanation':'AMAT≈1+0.05×80=5 ns。'},
    {'id':'ch05-q04','chapterId':'ch05','question':'為什麼計算機不把所有資料都放在最快的記憶體層？','answer':'因為速度、容量與成本存在權衡，最快層通常容量小且昂貴。','explanation':'儲存階層用不同技術平衡速度、容量、成本與持久性。'},
    {'id':'ch05-q05','chapterId':'ch05','question':'「快取容量增加，任何程式一定等比例變快」是否正確？','answer':'不正確。','explanation':'效益取決於存取模式、命中率、工作集與其他瓶頸，不會機械式等比例提升。'},

    {'id':'ch06-q01','chapterId':'ch06','question':'裝置驅動程式屬於硬體還是軟體？','answer':'軟體。','explanation':'driver 是讓作業系統能控制特定裝置的軟體元件。'},
    {'id':'ch06-q02','chapterId':'ch06','question':'理想傳輸率 250 MB/s，傳 500 MB 的純資料時間至少約多久？','answer':'約 2 秒。','explanation':'500/250=2 秒，實際系統還可能有額外開銷。'},
    {'id':'ch06-q03','chapterId':'ch06','question':'中斷（interrupt）的一個主要好處是什麼？','answer':'裝置可在需要處理時通知 CPU，減少 CPU 持續輪詢等待。','explanation':'中斷讓處理器可以先做其他工作，事件發生再切去處理。'},
    {'id':'ch06-q04','chapterId':'ch06','question':'Buffer 的主要作用是什麼？','answer':'暫存資料以吸收生產者與消費者的短期速度差。','explanation':'緩衝可平滑 I/O 流量，但容量有限，不能保證永不塞滿。'},
    {'id':'ch06-q05','chapterId':'ch06','question':'介面標示 1 Gbit/s，是否代表應用程式一定每秒可拿到 125 MB 的有效資料？','answer':'不一定。','explanation':'協定開銷、裝置、網路、處理與其他瓶頸都可能降低實際 throughput。'},

    {'id':'ch07-q01','chapterId':'ch07','question':'程式檔案與 process 的差別是什麼？','answer':'程式檔案是靜態指令／資料；process 是程式正在執行時的實例與狀態。','explanation':'同一程式可同時啟動成多個程序。'},
    {'id':'ch07-q02','chapterId':'ch07','question':'單核心 CPU 能不能出現 concurrency（並行）？','answer':'可以。','explanation':'多個工作可快速交錯執行而呈現並行；parallelism 才強調同時在多個執行資源執行。'},
    {'id':'ch07-q03','chapterId':'ch07','question':'同一 process 內的 threads 通常會共享什麼？','answer':'通常共享同一程序的位址空間與許多資源，但各自有執行狀態。','explanation':'這也是多執行緒溝通方便但同步更重要的原因。'},
    {'id':'ch07-q04','chapterId':'ch07','question':'A 在 t=0 到達需 4 ms，B 在 t=1 到達需 2 ms；不可搶先 FCFS 下 B 的完成時間是多少？','answer':'t=6 ms。','explanation':'A 先從 0 執行到 4，B 再由 4 執行到 6。'},
    {'id':'ch07-q05','chapterId':'ch07','question':'「並行（concurrency）一定代表兩個工作物理上同一瞬間執行」是否正確？','answer':'不正確。','explanation':'單核心也能藉交錯排程形成 concurrency；同時執行屬 parallelism 的核心意義。'},

    {'id':'ch08-q01','chapterId':'ch08','question':'虛擬位址是否必然等於實體 RAM 位址？','answer':'不必然。','explanation':'虛擬記憶體透過位址轉譯把虛擬位址映射到實體位址。'},
    {'id':'ch08-q02','chapterId':'ch08','question':'16 KiB 虛擬空間、頁大小 4 KiB，在簡化模型中有幾頁？','answer':'4 頁。','explanation':'16/4=4。'},
    {'id':'ch08-q03','chapterId':'ch08','question':'Page fault 是否一定代表程式崩潰？','answer':'不一定。','explanation':'頁面不在 RAM 時可觸發正常缺頁處理；只有無效存取等情況才可能導致錯誤。'},
    {'id':'ch08-q04','chapterId':'ch08','question':'Virtual machine 與一般 container 在 OS 核心使用上最典型的差別是什麼？','answer':'VM 通常各自執行 guest OS；container 通常共享主機 OS 核心。','explanation':'兩者都提供隔離，但抽象層級不同。'},
    {'id':'ch08-q05','chapterId':'ch08','question':'「虛擬記憶體就是把硬碟當慢速 RAM」是否完整正確？','answer':'不完整。','explanation':'虛擬記憶體核心是位址空間、映射、保護與隔離；交換／後備儲存只是可能的一部分。'},

    {'id':'ch09-q01','chapterId':'ch09','question':'Router 典型上主要依哪一層位址做跨網路轉送？','answer':'IP 位址（網路層）。','explanation':'路由器依網路層路由資訊把封包送往不同網路。'},
    {'id':'ch09-q02','chapterId':'ch09','question':'100 Mb/s 是否等於 100 MB/s？','answer':'不是；100 Mb/s 理想換算為 12.5 MB/s。','explanation':'1 byte=8 bits，所以 100/8=12.5 MB/s。'},
    {'id':'ch09-q03','chapterId':'ch09','question':'1 Mbit 封包經 20 Mbit/s 鏈路，單純 transmission delay 約多少？','answer':'0.05 秒。','explanation':'1/20=0.05 秒。'},
    {'id':'ch09-q04','chapterId':'ch09','question':'端到端延遲除了 transmission delay，還常包含哪些類型？','answer':'processing、queueing 與 propagation delay。','explanation':'完整延遲可拆成處理、排隊、傳輸與傳播。'},
    {'id':'ch09-q05','chapterId':'ch09','question':'「頻寬很高，所以網路延遲一定很低」是否正確？','answer':'不正確。','explanation':'頻寬與延遲是不同維度；距離、排隊、處理等都會影響 latency。'},
]
