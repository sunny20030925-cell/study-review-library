from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

BOOK_ID = "cost-accounting"
SOURCE_VERSION = "2026.07.29-1"
TARGET_VERSION = "2026.07.29-2"
LIBRARY_VERSION = "2026.07.29-8"


def fragment(html: str):
    return BeautifulSoup(html, "html.parser")


def replace_first_paragraph_after(soup: BeautifulSoup, heading_id: str, html: str) -> None:
    heading = soup.find(id=heading_id)
    if heading is None:
        raise AssertionError(f"missing heading {heading_id}")
    node = heading.find_next_sibling()
    while node is not None and getattr(node, "name", None) is None:
        node = node.find_next_sibling()
    if node is None or node.name != "p":
        raise AssertionError(f"missing paragraph after {heading_id}")
    node.replace_with(fragment(html))


def insert_before_heading(soup: BeautifulSoup, heading_id: str, html: str) -> None:
    heading = soup.find(id=heading_id)
    if heading is None:
        raise AssertionError(f"missing heading {heading_id}")
    heading.insert_before(fragment(html))


def replace_section_until_next_h2(soup: BeautifulSoup, heading_id: str, html: str) -> None:
    heading = soup.find(id=heading_id)
    if heading is None:
        raise AssertionError(f"missing heading {heading_id}")
    node = heading.find_next_sibling()
    while node is not None and node.name != "h2":
        nxt = node.find_next_sibling()
        node.extract()
        node = nxt
    heading.insert_after(fragment(html))


def set_practice_item(soup: BeautifulSoup, index: int, text: str) -> None:
    box = soup.find("div", class_="practicebox")
    items = box.find_all("li") if box else []
    if len(items) != 5:
        raise AssertionError("practice item count changed")
    p = items[index].find("p")
    p.string = text


def read_soup(root: Path, chapter_id: str) -> BeautifulSoup:
    path = root / "chapters" / f"{chapter_id}.html"
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def write_soup(root: Path, chapter_id: str, soup: BeautifulSoup) -> None:
    path = root / "chapters" / f"{chapter_id}.html"
    path.write_text(str(soup).strip() + "\n", encoding="utf-8")


def patch_ch00(root: Path) -> None:
    soup = read_soup(root, "ch00")
    insert_before_heading(
        soup,
        "考題方法與常見錯誤",
        r'''<h2 id="主要成本與加工成本">主要成本與加工成本</h2>
<p>主要成本（prime costs）是直接材料與直接人工之和；加工成本（conversion costs）是直接人工與製造費用之和。直接人工同時出現在兩個分類中，因此不能把主要成本與加工成本直接相加，否則會重複計入直接人工。</p>
<p class="math display">\[主要成本=直接材料+直接人工\]</p>
<p class="math display">\[加工成本=直接人工+製造費用\]</p>''',
    )
    set_practice_item(soup, 4, "加工成本由哪兩類製造成本組成？")
    write_soup(root, "ch00", soup)


def patch_ch01(root: Path) -> None:
    soup = read_soup(root, "ch01")
    replace_first_paragraph_after(
        soup,
        "直接材料耗用",
        r'''<p>材料採購先增加原料存貨；實際投入生產後，直接材料轉入在製品，間接材料則進製造費用。考題若給「原料期初、進料、原料期末」，先算本期材料耗用，再視直接與間接部分拆分。這裡的「進料」應是淨進料；若另給進貨運費、退回或折讓，必須先依題意調整，不能把毛進貨額直接帶入。</p>''',
    )
    write_soup(root, "ch01", soup)


def patch_ch03(root: Path) -> None:
    soup = read_soup(root, "ch03")
    replace_first_paragraph_after(
        soup,
        "安全邊際與基本假設",
        r'''<p>安全邊際（margin of safety）是實際或預計銷售超過損益平衡銷售的部分。基本 CVP 在相關範圍內通常假設單位售價與單位變動成本近似不變、固定成本總額近似不變；多產品時還要假設銷售組合固定。CVP 以貢獻邊際式損益與銷售量為主；若改用吸收成本法且存貨變動，固定製造費用的遞延或釋放必須另行調整，不能只用「產銷差異不大」含糊帶過。</p>''',
    )
    write_soup(root, "ch03", soup)


def patch_ch07(root: Path) -> None:
    soup = read_soup(root, "ch07")
    replace_section_until_next_h2(
        soup,
        "加權平均法的核心",
        r'''<p>加權平均法（weighted-average method）把期初在製品成本與本期新增成本合併，但材料與加工成本仍須分別計算。每一成本成分都要用自己的約當產量作分母；不能把材料與加工總成本先混在一起，再除以單一約當產量。</p>
<p class="math display">\[WA單位成本_c=(期初WIP成本_c+本期新增成本_c)\div WA約當產量_c\]</p>
<p>其中下標 c 代表特定成本成分，例如直接材料或加工成本。</p>''',
    )
    replace_first_paragraph_after(
        soup,
        "分配與檢核",
        r'''<p>先分別算出材料與加工的每約當單位成本，再按各自完工程度分配給「完工轉出」與「期末在製品」；完工單位的總單位成本才是各成本成分單位成本之和。最後一定檢查：分配總成本 = 期初在製品成本 + 本期新增成本。若差一大截，通常是約當產量、完工程度或成本成分混用。</p>''',
    )
    write_soup(root, "ch07", soup)


def patch_ch08(root: Path) -> None:
    soup = read_soup(root, "ch08")
    replace_first_paragraph_after(
        soup,
        "轉入成本",
        r'''<p>後續部門接收前部門完工單位時，前部門成本成為轉入成本（transferred-in cost），並須與本部門材料、加工成本分開計算。單位一進入本部門，通常即對轉入成本視為 100% 完成；但 FIFO 仍要區分期間：期初 WIP 已帶入的轉入成本屬前期成本，不進入本期每約當單位成本的分子；本期轉入成本則對應本期由前部門轉入的單位。不能把本部門加工完成百分比直接套到轉入成本。</p>''',
    )
    set_practice_item(soup, 4, "後部門期末 WIP 的轉入成本完工程度是否必須等於本部門加工成本完工程度？")
    write_soup(root, "ch08", soup)


def patch_ch09(root: Path) -> None:
    soup = read_soup(root, "ch09")
    replace_first_paragraph_after(
        soup,
        "正常與異常損壞",
        r'''<p>正常損壞（normal spoilage）是在有效率生產條件下仍預期會發生的損耗，其成本通常由通過相關檢驗點的合格產出吸收；異常損壞（abnormal spoilage）超出正常水準，通常在當期單獨認列損失，以免把異常效率問題資本化進存貨。</p>''',
    )
    replace_first_paragraph_after(
        soup,
        "檢驗點的重要性",
        r'''<p>損壞通常在某個檢驗點被發現。成本負擔取決於單位是否已通過該檢驗點：若期末 WIP 尚未到達檢驗點，通常不應分攤該檢驗點才辨認出的正常損壞成本；若已通過，才可能與完工合格品一同吸收。題目因此必須同時讀取檢驗點、完工程度與正常損壞率的分母。</p>''',
    )
    write_soup(root, "ch09", soup)


def patch_ch12(root: Path) -> None:
    soup = read_soup(root, "ch12")
    insert_before_heading(
        soup,
        "分離點銷售價值法",
        r'''<h2 id="物量法與限制">物量法與限制</h2>
<p>物量法（physical-measure method）按重量、體積、數量等實體單位分攤聯合成本。它容易計算，適合產出可用共同物量衡量的情況；但若各產品價值差異很大，物量比例未必能代表經濟受益，因此不能把它視為天然最合理的方法。</p>''',
    )
    insert_before_heading(
        soup,
        "決策邊界",
        r'''<h2 id="副產品的辨認與處理">副產品的辨認與處理</h2>
<p>副產品（by-product）也是共同製程的產出，但相對於主要產品，其銷售價值通常不重大。常見簡化作法是在副產品可出售時，以其淨變現價值沖減共同製程或主要產品成本；有些制度則在出售時列為其他收入。兩種作法的認列時點與表達不同，應依題目或企業政策一致處理，不能把副產品當成與聯產品同等重要後再平均分攤。</p>''',
    )
    set_practice_item(soup, 4, "副產品與聯產品的主要區別是什麼？")
    write_soup(root, "ch12", soup)


def patch_ch14(root: Path) -> None:
    soup = read_soup(root, "ch14")
    intro = soup.find("p")
    intro.string = "材料與人工差異最容易因符號太像而混亂。材料價格差異要先分清實際購買量與實際使用量；材料用量差異則一定比較實際使用量與實際產出允許的標準用量。人工差異再以實際工時與標準工時對照。"
    replace_section_until_next_h2(
        soup,
        "材料價格差異",
        r'''<p>直接材料價格差異（materials price variance, MPV）若在購買時認列，應以實際購買量 AQP（actual quantity purchased）衡量；若制度在使用時才認列，才改用實際使用量 AQU（actual quantity used）。兩種制度都可以，但同一題不能把購買量與使用量混成一個未定義的 AQ。</p>
<p class="math display">\[MPV=AQP\times(AP-SP)\quad（購買時認列）\]</p>
<p class="math display">\[MPV=AQU\times(AP-SP)\quad（使用時認列）\]</p>''',
    )
    replace_section_until_next_h2(
        soup,
        "材料用量差異",
        r'''<p>直接材料用量差異（materials quantity variance, MQV）比較實際使用量 AQU 與實際產出應允許的標準用量 SQ，並以標準價格 SP 衡量。</p>
<p class="math display">\[MQV=SP\times(AQU-SQ)\]</p>''',
    )
    replace_section_until_next_h2(
        soup,
        "完整例題",
        r'''<div class="examplebox"><p class="box-title">材料差異</p><p>實際購買 5,400 公斤，每公斤實際價 NT$31；標準價 NT$30。實際使用 5,200 公斤，實際產出允許標準用量 5,000 公斤。若價格差異在購買時認列，MPV = 5,400×(31−30)=NT$5,400 U；MQV = 30×(5,200−5,000)=NT$6,000 U。</p></div>''',
    )
    tip = soup.find("div", class_="examtip")
    tip.find("p").string = "材料價格差異：先確認用 AQP（購買時）或 AQU（使用時）；材料用量差異：固定用 AQU 與 SQ，並以 SP 衡量。人工工資率差異用 AH，人工效率差異比較 AH 與 SH。"
    summary = soup.find("div", class_="summarybox")
    summary.find("p").string = "先固定 AQP、AQU、SQ、AP、SP（或 AH、SH、AR、SR）的意義，再代公式；不要讓同一個 AQ 同時扮演購買量與使用量。"
    set_practice_item(soup, 0, "若材料價格差異在購買時認列，AQP=5,400 公斤、AP=NT$31、SP=NT$30。材料價格差異多少？")
    set_practice_item(soup, 1, "AQU=5,200 公斤、SQ=5,000 公斤、SP=NT$30。材料用量差異多少？")
    write_soup(root, "ch14", soup)


def patch_ch16(root: Path) -> None:
    soup = read_soup(root, "ch16")
    first = soup.find("p")
    first.string = "吸收成本法（absorption costing）把合理分攤的固定製造費用納入產品成本；變動成本法（variable costing）則把固定製造費用視為期間成本。兩法最大的損益差異，來自固定製造費用是否暫存在存貨，但吸收成本法不等於把任何閒置產能成本都硬塞進產品。"
    replace_first_paragraph_after(
        soup,
        "產品成本的組成",
        r'''<p>吸收成本法產品成本包含直接材料、直接人工、變動製造費用與合理分攤的固定製造費用。變動成本法產品成本只包含變動製造成本；固定製造費用在發生期間全數列費用。對外存貨衡量時，固定製造費用的單位分攤仍須受正常產能原則限制。</p>''',
    )
    replace_section_until_next_h2(
        soup,
        "利潤調節公式",
        r'''<p>一般調節先比較期末與期初存貨內含的固定製造費用：</p>
<p class="math display">\[吸收利益-變動利益=期末存貨內含固定OH-期初存貨內含固定OH\]</p>
<p>只有在期初與期末每單位固定 OH 率相同、沒有其他製造費用差異調整時，才可簡化為「存貨增加單位 × 每單位固定 OH」。</p>''',
    )
    example = soup.find("div", class_="examplebox")
    example.find_all("p")[1].string = "假設期初存貨為 0，本期生產 10,000 單位、銷售 8,500 單位，且正常產能下可分攤固定製造費用 NT$300,000，沒有多分／少分等其他調整。每單位固定 OH = NT$30；期末存貨增加 1,500 單位，因此吸收成本法利益比變動成本法高 NT$45,000。"
    replace_first_paragraph_after(
        soup,
        "用途與限制",
        r'''<p>對外財務報導的存貨成本採吸收成本觀念，但固定製造費用通常按正常產能分攤；異常低產量形成的未分攤固定製造費用應在當期認列，不應藉由提高單位率全部留在存貨。變動成本法則能直接呈現貢獻邊際結構，便於內部分析。兩法利益差異主要是固定製造費用認列時點，不代表現金流量同步改變。</p>''',
    )
    set_practice_item(soup, 0, "若正常產能下可分攤固定製造費用 NT$300,000，並按 10,000 單位分攤，每單位固定製造費用多少？")
    write_soup(root, "ch16", soup)


def patch_ch17(root: Path) -> None:
    soup = read_soup(root, "ch17")
    replace_first_paragraph_after(
        soup,
        "幾種產能觀念",
        r'''<p>理論產能假設沒有停機；實務產能（practical capacity）扣除正常維修、休息等不可避免中斷，偏向工程上可供使用的能力；正常產能（normal capacity）則是正常情況下跨數期或季節預期達成的平均產量，並考量計畫性維修；預算產能依當期預計需求。這些分母定義不同，不能互換名稱。</p>''',
    )
    insert_before_heading(
        soup,
        "閒置產能可見性",
        r'''<h2 id="對外存貨衡量的正常產能規則">對外存貨衡量的正常產能規則</h2>
<p>對外存貨衡量分攤固定製造費用時，通常以正常產能為基礎。產量異常偏低時，不應因實際分母變小就把單位固定 OH 無限制提高；未分攤部分應在當期認列。產量異常偏高時，單位分攤率反而要調低，避免存貨成本高於實際發生的固定製造費用。</p>''',
    )
    set_practice_item(soup, 4, "產量異常偏低時，正常產能下未分攤的固定製造費用通常如何處理？")
    write_soup(root, "ch17", soup)


def patch_appendix_a(root: Path) -> None:
    soup = read_soup(root, "appendix-a")
    replace_section_until_next_h2(
        soup,
        "分步與約當產量",
        r'''<p class="math display">\[EUP_{WA,c}=完工轉出量+期末WIP約當量_c\]</p>
<p class="math display">\[WA單位成本_c=(期初成本_c+本期成本_c)\div EUP_{WA,c}\]</p>
<p>材料與加工成本分別使用自己的約當產量，最後再加總為完工單位成本。</p>''',
    )
    replace_section_until_next_h2(
        soup,
        "標準成本差異",
        r'''<p>材料價格（購買時認列）：AQP(AP−SP)；材料價格（使用時認列）：AQU(AP−SP)；材料用量：SP(AQU−SQ)。人工工資率：AH(AR−SR)；人工效率：SR(AH−SH)。</p>
<p>固定 OH：預算差異 = 實際 FOH − 預算 FOH；生產量差異 = 預算 FOH − 已分攤 FOH。</p>
<p>吸收／變動利益調節：期末存貨內含固定 OH − 期初存貨內含固定 OH；固定率相同且無其他差異時，才可簡化為存貨增加單位 × 每單位固定 OH。</p>''',
    )
    write_soup(root, "appendix-a", soup)


def patch_appendix_c(root: Path) -> None:
    soup = read_soup(root, "appendix-c")
    table = soup.find("table")
    if table is None:
        raise AssertionError("missing glossary table")
    body = table.find("tbody") or table
    rows = [
        ("主要成本", "prime costs", "—"),
        ("加工成本", "conversion costs", "—"),
        ("副產品", "by-product", "—"),
        ("正常產能", "normal capacity", "—"),
        ("實際購買量", "actual quantity purchased", "AQP"),
        ("實際使用量", "actual quantity used", "AQU"),
    ]
    existing = table.get_text(" ", strip=True)
    for zh, en, abbr in rows:
        if zh in existing:
            continue
        row = fragment(f"<tr><td>{zh}</td><td>{en}</td><td>{abbr}</td></tr>")
        body.append(row)
    write_soup(root, "appendix-c", soup)


def update_questions(root: Path) -> None:
    path = root / "questions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["version"] != SOURCE_VERSION:
        raise AssertionError(f"unexpected questions source version {data['version']}")
    qmap = {q["id"]: q for q in data["items"]}

    qmap["ch00-q05"].update(
        topic="分類",
        question="加工成本由哪兩類製造成本組成？",
        answer="直接人工與製造費用。",
        explanation="加工成本反映把材料轉換為產品所投入的直接人工與製造費用；直接人工也同時屬主要成本。",
    )
    qmap["ch08-q05"].update(
        question="後部門期末 WIP 的轉入成本完工程度是否必須等於本部門加工成本完工程度？",
        answer="不必；單位進入後部門時，轉入成本通常已視為 100%，本部門加工可能仍未完成。",
        explanation="轉入成本與本部門材料、加工成本是不同成本成分；FIFO 還須把期初舊成本與本期轉入成本分開。",
    )
    qmap["ch09-q03"].update(
        answer="通常由已通過相關檢驗點的合格產出吸收。",
        explanation="若期末 WIP 尚未到達檢驗點，通常不應分攤該檢驗點才辨認出的正常損壞成本。",
    )
    qmap["ch12-q05"].update(
        topic="分類",
        question="副產品與聯產品的主要區別是什麼？",
        answer="副產品相對於主要產品的銷售價值通常不重大；聯產品各自具有重要銷售價值。",
        explanation="副產品常以淨變現價值沖減共同製程成本或於出售時列收入，處理方式與聯產品分攤不同。",
    )
    qmap["ch14-q01"].update(
        question="若材料價格差異在購買時認列，AQP=5,400 公斤、AP=NT$31、SP=NT$30。材料價格差異多少？",
        answer="NT$5,400 U。",
        explanation="5,400×(31−30)=5,400，不利；購買時認列使用實際購買量 AQP。",
    )
    qmap["ch14-q02"].update(
        question="AQU=5,200 公斤、SQ=5,000 公斤、SP=NT$30。材料用量差異多少？",
        explanation="30×(5,200−5,000)=6,000，不利；用量差異使用實際使用量 AQU。",
    )
    qmap["ch16-q01"].update(
        question="若正常產能下可分攤固定製造費用 NT$300,000，並按 10,000 單位分攤，每單位固定製造費用多少？",
        explanation="300,000÷10,000=30；題目已明定這是可分攤固定製造費用與分攤單位。",
    )
    qmap["ch16-q04"].update(
        answer="吸收成本法。",
        explanation="吸收成本法將合理分攤的固定製造費用納入產品成本；異常低產量的未分攤部分不應硬塞進存貨。",
    )
    qmap["ch17-q05"].update(
        question="產量異常偏低時，正常產能下未分攤的固定製造費用通常如何處理？",
        answer="在當期認列為費用。",
        explanation="不能因實際產量偏低就無限制提高單位固定製造費用並資本化進存貨。",
    )

    data["version"] = TARGET_VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_manifest_and_library(site: Path, root: Path) -> None:
    path = root / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest["version"] != SOURCE_VERSION:
        raise AssertionError(f"unexpected manifest source version {manifest['version']}")
    manifest["version"] = TARGET_VERSION
    manifest["updatedAt"] = "2026-07-29"
    manifest["releaseNotes"].insert(
        0,
        {
            "version": TARGET_VERSION,
            "date": "2026-07-29",
            "title": "發布後獨立二次內容審計與糾錯",
            "changes": [
                "補入主要成本與加工成本，並補正分步成本按成本成分分別計算約當產量與單位成本",
                "區分材料價格差異的實際購買量 AQP 與實際使用量 AQU，修正例題與題庫答案",
                "補齊副產品與物量法，並精確化正常損壞、FIFO 轉入成本與 CVP 存貨前提",
                "依正常產能原則補正吸收成本與固定製造費用分攤，明定異常低產量未分攤部分當期認列",
                "95 題全數重查，44 個數值答案重新計算，搜尋索引與離線快取同步重建",
            ],
            "progressImpact": "章節 ID、題目 ID 與題數不變；既有閱讀進度與錯題紀錄保留。",
        },
    )
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lib_path = site / "data" / "library.json"
    library = json.loads(lib_path.read_text(encoding="utf-8"))
    library["version"] = LIBRARY_VERSION
    lib_path.write_text(json.dumps(library, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def regenerate_search(root: Path) -> int:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    entries = []
    for chapter in manifest["chapters"]:
        soup = read_soup(root, chapter["id"])
        first_h2 = soup.find("h2")
        intro_nodes = []
        for child in soup.contents:
            if child == first_h2:
                break
            intro_nodes.append(child)
        intro_soup = BeautifulSoup("".join(str(x) for x in intro_nodes), "html.parser")
        intro_text = " ".join(intro_soup.get_text(" ", strip=True).split())
        if intro_text:
            entries.append(
                {
                    "chapterId": chapter["id"],
                    "chapterTitle": chapter["title"],
                    "page": 0,
                    "title": chapter["title"],
                    "text": intro_text,
                }
            )
        page = 1
        for h2 in soup.find_all("h2"):
            parts = [str(h2)]
            node = h2.find_next_sibling()
            while node is not None and node.name != "h2":
                parts.append(str(node))
                node = node.find_next_sibling()
            section_soup = BeautifulSoup("".join(parts), "html.parser")
            text = " ".join(section_soup.get_text(" ", strip=True).split())
            entries.append(
                {
                    "chapterId": chapter["id"],
                    "chapterTitle": chapter["title"],
                    "page": page,
                    "title": " ".join(h2.get_text(" ", strip=True).split()),
                    "text": text,
                }
            )
            page += 1
    (root / "search.json").write_text(
        json.dumps({"entries": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return len(entries)


def update_service_worker(site: Path) -> None:
    path = site / "sw.js"
    text = path.read_text(encoding="utf-8")
    text, n = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{LIBRARY_VERSION}';",
        text,
        count=1,
    )
    if n != 1:
        raise AssertionError("service worker version not updated")
    path.write_text(text, encoding="utf-8")


def main(site_arg: str) -> None:
    site = Path(site_arg)
    root = site / "books" / BOOK_ID
    patch_ch00(root)
    patch_ch01(root)
    patch_ch03(root)
    patch_ch07(root)
    patch_ch08(root)
    patch_ch09(root)
    patch_ch12(root)
    patch_ch14(root)
    patch_ch16(root)
    patch_ch17(root)
    patch_appendix_a(root)
    patch_appendix_c(root)
    update_questions(root)
    update_manifest_and_library(site, root)
    search_count = regenerate_search(root)
    update_service_worker(site)
    print(f"COST_ACCOUNTING_V2_PATCH_OK search={search_count}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python patch_cost_accounting_v2.py SITE_ROOT")
    main(sys.argv[1])
