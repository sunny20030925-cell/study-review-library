from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from computer_fundamentals_content_a import CHAPTERS_A
from computer_fundamentals_content_b import CHAPTERS_B
from computer_fundamentals_questions_a import QUESTIONS_A
from computer_fundamentals_questions_b import QUESTIONS_B
from generate_computer_fundamentals import appendix_a, appendix_b, appendix_c, chapter_html, search_entries

BOOK='computer-fundamentals'
SOURCE_VERSION='2026.07.29-1'
TARGET_VERSION='2026.07.30-2'

CORRECTION_AREAS = [
    'byte 定義與歷史例外',
    'interrupt 與 synchronous exception 區分',
    'CPU waiting-time 公式適用條件',
    'virtual memory 與 page fault 精確化',
    'HTTP(S) URL authority 結構',
    'HTTP/3 使用 QUIC/TLS 1.3 的現代補充',
    'Big-O 與 Theta tight bound 區分',
    '1024 元素二分搜尋減半次數與比較次數區分',
    'relation 與 SQL table 的概念邊界',
    'foreign key self-reference 與被參照唯一鍵',
    'ACID Consistency 的完整語意',
    'cryptographic hash 與一般 hash 區分',
    'password hashing/KDF 的可調成本與 salt',
    'NIST cloud 五項核心特徵',
    'edge computing 不自動保證隱私或安全',
]

QUESTION_ADJUSTMENTS = {
    'ch06-q03','ch08-q01','ch08-q03','ch08-q05','ch10-q04',
    'ch12-q01','ch12-q02','ch12-q05','ch14-q02','ch16-q04','ch16-q05','ch18-q01',
}


def by_id(items, item_id):
    for item in items:
        if item['id'] == item_id:
            return item
    raise AssertionError(f'missing {item_id}')


def corrected_chapters():
    chapters=copy.deepcopy(CHAPTERS_A + CHAPTERS_B)

    ch=by_id(chapters,'ch01')
    ch['definitions'][1]=('byte（位元組）','本書與現代通用計算語境採 1 byte = 8 bits。歷史上曾有非 8-bit byte 的機器，但不屬本書計算題範圍。')
    ch['traps'][0]='把 1 byte 寫成 8 bytes；本書固定採 1 byte = 8 bits。'

    ch=by_id(chapters,'ch06')
    ch['intuition'][1]='裝置完成工作時常用硬體中斷通知 CPU，讓 CPU 不必持續輪詢。這類硬體 interrupt 通常是非同步事件；除零、非法指令、page fault 等則屬由目前指令觸發的同步 exception。不同教材可能用「中斷」作較廣義總稱，作答時要看定義。'
    ch['definitions'][2]=('Interrupt（硬體中斷）','通常由外部硬體非同步發出事件通知，使處理器在允許的時機保存必要狀態並轉去執行中斷處理常式；是否立即處理還受優先權與遮罩等機制影響。')
    ch['definitions'].append(('Exception（例外）','由目前執行指令同步引發的處理器事件，例如除零、非法指令或 page fault；有些可由作業系統處理後繼續，有些會轉成程式錯誤。'))
    ch['example'][1]='鍵盤按鍵發生時，控制器可以送出硬體中斷，CPU 不必每個時脈週期都問「有沒有新按鍵」；相對地，程式存取尚未駐留的合法虛擬頁面所造成的 page fault 是同步 exception。'
    ch['traps'][1]='把所有 interrupt／exception 都當成作業系統崩潰；許多事件其實是正常控制流程的一部分。'
    ch['exam'][0]='先分事件是外部裝置非同步通知，還是目前指令同步觸發的 exception；再判斷是否需要緩衝、佇列或 handler。'

    ch=by_id(chapters,'ch07')
    ch['formulas'][1]=('waiting time = turnaround time − CPU burst time','只適用於教科書的簡化排程題：程序只有所列 CPU burst、沒有另計 I/O／sleep 等非 CPU 時間。一般實際程序不能直接用此式把所有非 CPU 時間都稱為等待。')

    ch=by_id(chapters,'ch08')
    ch['intuition'][0]='虛擬記憶體讓程序看到自己的虛擬位址空間；對目前駐留的頁面，硬體透過頁表把虛擬頁映射到實體 page frame。未駐留內容可能由檔案、swap／pagefile 提供，或在第一次使用時配置，不是 CPU 把虛擬位址直接「翻譯成磁碟位址」。'
    ch['intuition'][1]='當目前的頁表狀態無法直接完成某次記憶體存取時，CPU 會產生 page fault exception。原因可能是頁面尚未駐留、copy-on-write，或存取違反保護權限；作業系統能處理的 fault 可修正映射後重試，非法存取則可能終止程式。'
    ch['definitions'][0]=('Virtual Memory（虛擬記憶體）','以虛擬位址空間、頁表與保護機制把程序的位址觀點與實體記憶體配置解耦；非駐留頁面的內容可由後備儲存或按需求配置取得。')
    ch['definitions'][2]=('Page Fault（缺頁／頁面錯誤例外）','當處理器無法依目前頁表狀態完成某次虛擬記憶體存取時產生的同步 exception，例如頁面 not-present、copy-on-write 或保護權限違反。作業系統可能修復後重試，也可能判定為非法存取。')
    ch['formulas'][0]=('resident virtual address → page-table translation → physical address','只有有效且目前可存取的駐留映射才能直接完成實體位址轉譯；not-present 或權限不符會先產生 page fault。')
    ch['example'][1]='若合法頁面尚未在 RAM，第一次存取可能觸發 demand paging；第一次寫入 copy-on-write 頁也可能觸發 fault 讓 OS 複製頁面。相反地，存取根本未映射或禁止寫入的區域也可能 fault，但最後會被判定為程式錯誤。'
    ch['traps'][0]='把所有 page fault 都當成「從硬碟讀頁」；demand-zero、copy-on-write、保護違規等也可能造成 page fault。'
    ch['exam'][0]='位址題先分虛擬位址、目前是否有有效駐留映射、實體 frame，以及 fault handler 是否需要介入。'

    ch=by_id(chapters,'ch10')
    ch['intuition'][1]='DNS 把人容易記的網域名稱解析成位址等紀錄。傳輸服務常見 TCP 與 UDP：TCP 提供可靠、有序的位元組串流；UDP 提供較精簡的資料報服務。HTTP/1.1 與 HTTP/2 常見於 TCP 上，而 HTTP/3 則把 HTTP semantics 映射到 QUIC；QUIC 使用 UDP 並整合 TLS 1.3。'
    ch['intuition'][2]='瀏覽器向 Web 伺服器送出 HTTP 請求並接收 HTTP 回應。HTTPS 表示 HTTP 使用經 TLS 保護與驗證的安全傳輸；在 HTTP/3 中，TLS 1.3 是 QUIC 連線建立的一部分。HTTPS 保護傳輸與對端身分驗證，不保證網站內容本身一定真實可信。'
    ch['definitions'][4]=('HTTP / HTTPS','HTTP 定義 Web 的請求、回應與資源語意；HTTPS 表示這些 HTTP semantics 經 TLS 所保護的安全傳輸承載。HTTP/3 使用 QUIC，而 QUIC 內整合 TLS 1.3。')
    ch['formulas'][0]=('common HTTP(S) URL ≈ scheme://authority/path?query#fragment','對常見階層式 HTTP(S) URL，authority 包含 host，並可含 port 等資訊；query 與 fragment 都是可選。fragment 由用戶端處理，不會作為 HTTP request target 的一部分送給伺服器。')
    ch['example'][0]='例：開啟 https://example.com/notes。瀏覽器先取得 example.com 的名稱解析結果，再依協定協商建立安全傳輸：可能是 TCP 上的 TLS，也可能是整合 TLS 1.3 的 QUIC；之後再交換 HTTP 請求與回應。'
    ch['traps'].append('把 HTTPS 固定等同「HTTP + TCP + TLS」；HTTP/3 使用 QUIC，而 QUIC 以 UDP 為基礎並整合 TLS 1.3。')
    ch['exam'][0]='網址題先分 scheme、authority（含 host／可能的 port）、path、query、fragment，再分 DNS、傳輸與 HTTP semantics 的角色。'

    ch=by_id(chapters,'ch12')
    ch['intuition'][2]='Big-O 嚴格來說描述漸近上界；若要表示「成長率上下界同階、是 tight bound」，用 Θ 更精確。日常教材常口語說「某演算法是 O(n)」來談成長，但 O(n) 本身不表示它一定恰好是線性階。'
    ch['definitions'][4]=('Big-O','描述函數在輸入夠大後的漸近上界；例如 Θ(log n) 的演算法同時也是 O(n)，所以 O 並不自動表示 tight bound。')
    ch['definitions'].append(('Big-Theta, Θ','描述漸近上下界同階的 tight bound；若某最壞情況操作量確實按 n 成長，可寫 Θ(n)。'))
    ch['formulas'][0]=('linear search worst case: Θ(n) (therefore also O(n))','最壞情況需要與 n 同階的檢查；寫 Θ(n) 比只寫 O(n) 更精確。')
    ch['formulas'][1]=('binary search worst case: Θ(log₂ n)','前提是搜尋空間有序且能有效取得中間元素；每輪把候選範圍縮小約一半。')
    ch['formulas'][2]=('comparison sorting lower bound: Ω(n log n)','在只靠元素比較來區分排列的模型下，任一比較式排序演算法的最壞情況需要 Ω(n log n) 次比較；此敘述不是所有非比較排序的下界。')
    ch['example'][0]='例：1024 個已排序元素做二分搜尋，候選範圍經 10 次減半可從 1024 縮到 1；但若計算典型 binary-search comparison loop 的最壞迭代／中間元素比較次數，還可能需要最後一次比較，因此可到 11 次。兩種數字回答的是不同問題。'
    ch['traps'][0]='把 O(n) 當成「剛好做 n 次」或 tight bound；O 只給漸近上界，tight bound 應看 Θ。'
    ch['exam'][2]='複雜度題先分 O（上界）、Ω（下界）、Θ（tight bound）；再把漸近成長與實際常數、秒數分開。'
    ch['checks'][1]='1024 個有序元素二分搜尋要把候選範圍縮到 1 需幾次減半？若算典型最壞 comparison-loop 次數又可能是多少？'

    ch=by_id(chapters,'ch14')
    ch['intuition'][0]='資料庫管理系統（DBMS）負責有結構地儲存、查詢、更新、保護與協調資料。關聯模型中的 relation 可用表格呈現，但數學上的 relation 是 tuple 的集合、沒有列的固有順序；SQL table 在實務語意上不必與純數學 relation 完全相同，例如查詢結果若未去重可含重複列。'
    ch['intuition'][1]='主鍵用來唯一識別一列；外鍵要求其非 NULL 值能對應到被參照的候選鍵／唯一鍵，以維持參照完整性。被參照者可以在另一張表，也可以是同一張表的 self-referential foreign key。正規化的核心直覺是減少重複與更新異常，不是把表拆得越多越好。'
    ch['definitions'][1]=('Relation / SQL Table（關聯／SQL 資料表）','關聯模型的 relation 是 tuple 的集合；教材常用列與欄的表格表示。SQL table 與查詢結果的實務語意較寬，不能把兩者所有性質完全畫上等號。')
    ch['definitions'][3]=('Foreign Key（外鍵）','一組 referencing 欄位，其非 NULL 值必須符合被參照表（可以是同一張表）的主鍵或其他符合 DBMS 規則的唯一候選鍵，以維持參照完整性。外鍵本身不必唯一。')
    ch['formulas'][1]=('ACID = Atomicity + Consistency + Isolation + Durability','Consistency 指交易在資料庫所宣告的完整性規則與不變條件下，從一個合法狀態轉到另一個合法狀態；它不表示 DBMS 能自動保證所有業務事實或應用邏輯都正確。')
    ch['example'].append('例：員工表可有 manager_id 外鍵參照同一張員工表的 employee_id，形成主管階層；這就是 self-referential foreign key。')
    ch['traps'][1]='以為外鍵一定唯一或一定要指向「另一張」表；外鍵可重複，也可以 self-reference。'
    ch['exam'][0]='先圈出 entity、主鍵／候選鍵、referencing 欄位與被參照鍵；再判斷是否可能是 self-reference。'

    ch=by_id(chapters,'ch16')
    ch['intuition'][2]='加密使用金鑰把明文轉成可在持有正確金鑰時還原的密文；密碼學雜湊則設計成單向固定長度摘要。要注意，資料結構章的 hash function 不一定具密碼學安全性。密碼儲存應使用專為密碼設計、具可調工作成本且常兼顧記憶體成本的 password hashing／KDF，搭配每筆唯一隨機 salt；例如目前常見建議優先考慮 Argon2id，實際選擇仍應依最新安全標準與系統限制。'
    ch['definitions'].append(('Cryptographic Hash（密碼學雜湊）','設計目標包含抗原像、抗第二原像與抗碰撞等安全性質的單向摘要函數；一般雜湊表用 hash function 不一定具備這些性質。'))
    ch['formulas'][1]=('stored verifier = PasswordHash/KDF(password, unique salt, cost parameters)','概念式；salt 應每筆唯一且通常隨機產生，演算法要能設定足夠的時間／記憶體成本。不要以快速通用 hash 或可逆加密直接取代 password hashing。')
    ch['example'][0]='例：網站資料庫可保存 password hashing／KDF 的輸出、salt 與必要的 cost parameters；登入時用相同演算法與參數驗證輸入，不需也不應能從儲存值「解密」回原始密碼。'
    ch['traps'][0]='把任何 hash function 都當成 cryptographic hash，或把 hashing 與 encryption 當同義詞。'
    ch['exam'][2]='密碼題若看到「可逆解密取回原密碼」或「直接用快速 SHA 類 hash 不加 password-specific cost」，都要警覺設計問題。'

    ch=by_id(chapters,'ch18')
    ch['intuition'][1]='雲端運算不是單純把伺服器搬遠端。NIST 的經典定義強調五項核心特徵：on-demand self-service、broad network access、resource pooling、rapid elasticity 與 measured service；SaaS、PaaS、IaaS 則是常見服務模型。'
    ch['definitions'][1]=('Cloud Computing（雲端運算）','以網路按需求存取共享、可配置的運算資源池，並能快速配置與釋放；經典 NIST 定義的五項核心特徵是按需自助、廣泛網路存取、資源池化、快速彈性與可量測服務。')
    ch['example'].append('例：單純租用一台固定規格的遠端主機可以是託管服務，但是否完整符合 cloud model，還要看是否具備按需自助、資源池化、快速彈性、量測等特徵。')
    ch['traps'].append('認為把運算移到 edge 就自動更安全或更隱私；edge 可能減少外傳資料，但仍需處理裝置、更新、金鑰、存取控制與實體風險。')
    ch['exam'][0]='雲端題若依 NIST 口徑，優先找按需自助、廣泛網路存取、資源池化、快速彈性與可量測服務；不要只看到「遠端伺服器」就判定。'

    return chapters


def corrected_questions():
    questions=copy.deepcopy(QUESTIONS_A + QUESTIONS_B)
    updates={
        'ch06-q03':('硬體中斷（interrupt）的一個主要好處是什麼？','裝置可在事件發生時通知 CPU，減少持續輪詢；CPU 會依優先權與遮罩等規則在允許的時機處理。','硬體中斷通常是非同步事件通知；它和由目前指令同步觸發的 exception（例如 page fault）要分開。'),
        'ch08-q01':('虛擬位址是否必然直接等於實體 RAM 位址？','不必然。','對目前有效且駐留的映射，頁表把虛擬頁轉到實體 frame；若頁面 not-present 或權限不符，會先產生 page fault，而不是把虛擬位址直接翻成磁碟位址。'),
        'ch08-q03':('Page fault 是否一定代表程式崩潰或一定要從磁碟讀資料？','兩者都不一定。','合法的 demand-zero、demand paging 或 copy-on-write 都可能造成可被 OS 解決的 page fault；保護違規或無效位址也可能 fault，最後才可能轉成程式錯誤。'),
        'ch08-q05':('「虛擬記憶體就是把硬碟當慢速 RAM」是否完整正確？','不完整。','虛擬記憶體核心是位址空間、頁表映射、保護與隔離；pagefile／swap 或檔案後備只處理部分非駐留內容，不是虛擬位址直接映射成磁碟位址。'),
        'ch10-q04':('使用者輸入 https://example.com 後，DNS、安全傳輸與 HTTP 大致各負責什麼？','DNS 做名稱解析；TLS 提供安全性與對端驗證；HTTP 定義請求／回應語意。HTTP/1.1、HTTP/2 常見於 TCP 上，HTTP/3 則使用整合 TLS 1.3 的 QUIC。','HTTPS 不應死背成固定的「HTTP + TCP + TLS」：HTTP/3 把 HTTP semantics 放在 QUIC 上，而 QUIC 以 UDP 為基礎並整合 TLS 1.3。'),
        'ch12-q01':('線性搜尋最壞情況若要寫 tight bound，通常是多少？','Θ(n)；因此它當然也屬於 O(n)。','最壞情況需要與 n 同階的檢查。Θ(n) 表示 tight bound；單寫 O(n) 只表示漸近上界。'),
        'ch12-q02':('1024 個已排序元素做二分搜尋，候選範圍縮到 1 要幾次減半？典型最壞 comparison-loop 又可能到幾次？','10 次減半；典型最壞 comparison-loop／中間元素比較可到 11 次。','1024=2^10，所以 10 次減半可把候選數量從 1024 縮到 1；若還要對最後一個候選做比較，迭代／比較次數可再多 1。'),
        'ch12-q05':('「某演算法是 O(n)」是否表示它一定恰好做 n 次操作，而且 Θ(n)？','不是。','O(n) 只給漸近上界；例如 Θ(log n) 的演算法也同時是 O(n)。若要表示上下界同階，應使用 Θ。'),
        'ch14-q02':('Foreign key 本身是否一定唯一？而且一定只能參照另一張表嗎？','都不是：外鍵可重複，也可以參照同一張表形成 self-referential foreign key。','外鍵約束的是 referencing 值必須對應被參照的主鍵／符合規則的唯一候選鍵；多列可引用同一父列，同一表也可自我參照。'),
        'ch16-q04':('Cryptographic hashing 與 encryption 的核心差異之一是什麼？','加密設計成持有正確金鑰可逆；密碼學雜湊是單向摘要，不用來還原原文。','另外，雜湊表使用的普通 hash function 不一定具抗原像、抗碰撞等密碼學安全性，不能因為都叫 hash 就混在一起。'),
        'ch16-q05':('密碼儲存為什麼要用 password hashing／KDF、每筆唯一 salt 與足夠的 cost parameters？','讓離線猜密碼更昂貴，並避免相同密碼直接產生可被批次比對的相同儲存值。','現代 password hashing 應能調整時間／記憶體成本；salt 通常每筆唯一且隨機。快速通用 hash 或可逆加密都不是理想的密碼儲存替代品。'),
        'ch18-q01':('Cloud computing 是否只是「租一台遠端電腦」的同義詞？若依 NIST 口徑還要看哪些核心特徵？','不是；核心特徵包括按需自助、廣泛網路存取、資源池化、快速彈性與可量測服務。','單純遠端託管主機未必呈現完整 cloud model；NIST 的經典定義以五項 essential characteristics 描述雲端。'),
    }
    for qid,(question,answer,explanation) in updates.items():
        q=by_id(questions,qid)
        q['question']=question; q['answer']=answer; q['explanation']=explanation
    return questions


def main(site_root: str) -> None:
    site=Path(site_root)
    root=site/'books'/BOOK
    manifest_path=root/'manifest.json'
    qpath=root/'questions.json'
    spath=root/'search.json'
    if not manifest_path.is_file():
        raise AssertionError('computer fundamentals not present in site')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    qdoc=json.loads(qpath.read_text(encoding='utf-8'))
    if manifest['version'] not in (SOURCE_VERSION,TARGET_VERSION):
        raise AssertionError(f'unexpected source content version {manifest["version"]}')

    chapters=corrected_chapters()
    questions=corrected_questions()

    for ch in chapters:
        (root/'chapters'/f'{ch["id"]}.html').write_text(chapter_html(ch),encoding='utf-8')
    (root/'chapters'/'appendix-a.html').write_text(appendix_a(chapters),encoding='utf-8')
    (root/'chapters'/'appendix-b.html').write_text(appendix_b(),encoding='utf-8')
    (root/'chapters'/'appendix-c.html').write_text(appendix_c(),encoding='utf-8')

    existing={item['id']:item for item in qdoc['items']}
    new_items=[]
    chapter_title={ch['id']:f'第 {int(ch["id"][2:])} 章 {ch["title"]}' for ch in chapters}
    chapter_topic={ch['id']:ch['title'] for ch in chapters}
    for src in questions:
        old=copy.deepcopy(existing[src['id']])
        old.update({
            'bookId':BOOK,
            'chapterId':src['chapterId'],
            'chapterTitle':chapter_title[src['chapterId']],
            'topic':chapter_topic[src['chapterId']],
            'question':src['question'],
            'answer':src['answer'],
            'explanation':src['explanation'],
        })
        new_items.append(old)
    if len(new_items)!=100 or len({x['id'] for x in new_items})!=100:
        raise AssertionError('question identity/count drift')
    qdoc['version']=TARGET_VERSION
    qdoc['count']=100
    qdoc['items']=new_items
    qpath.write_text(json.dumps(qdoc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    spath.write_text(json.dumps({'entries':search_entries(chapters)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    manifest['version']=TARGET_VERSION
    manifest['updatedAt']='2026-07-30'
    manifest['releaseNotes']=[{
        'version':TARGET_VERSION,
        'date':'2026-07-30',
        'title':'發布後第二次內容複核與精確性修正',
        'changes':[
            '精確化 page fault、interrupt/exception、URL authority、HTTP/3、Big-O/Theta、外鍵與 ACID 等概念',
            '修正二分搜尋 1024 元素「10 次減半」與「最壞比較可到 11 次」的區別',
            '補強 password hashing/KDF、NIST cloud 五項核心特徵與 edge 安全邊界',
            f'共 {len(CORRECTION_AREAS)} 個內容修正／補強區域、{len(QUESTION_ADJUSTMENTS)} 題題庫精確化；章節 ID、題目 ID 與題數均未變',
        ],
        'progressImpact':'章節 ID、題目 ID、Book ID、題數與進度儲存鍵均未變；既有閱讀進度與錯題紀錄相容。',
    }] + [x for x in manifest.get('releaseNotes',[]) if x.get('version')!=TARGET_VERSION]
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    print(json.dumps({
        'book':BOOK,'source_version':SOURCE_VERSION,'target_version':TARGET_VERSION,
        'chapters':20,'appendices':3,'questions':100,'search':150,
        'correction_areas':len(CORRECTION_AREAS),'question_adjustments':len(QUESTION_ADJUSTMENTS),
    },ensure_ascii=False))


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/patch_computer_fundamentals_v2.py SITE_ROOT')
    main(sys.argv[1])
