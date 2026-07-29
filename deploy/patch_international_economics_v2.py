from __future__ import annotations

import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

BOOK_ID = "international-economics"
SOURCE_VERSION = "2026.07.29-1"
TARGET_VERSION = "2026.07.29-2"

TOUCHED_CHAPTERS = {
    "ch03", "ch05", "ch06", "ch07", "ch08",
    "ch11", "ch13", "ch14", "ch16", "ch18", "appendix-b",
}
QUESTION_ADJUSTMENTS = {
    "ch03-q03", "ch03-q04", "ch05-q03", "ch06-q03",
    "ch08-q03", "ch11-q05", "ch14-q01",
}


def read_soup(root: Path, chapter_id: str) -> BeautifulSoup:
    path = root / "chapters" / f"{chapter_id}.html"
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def write_soup(root: Path, chapter_id: str, soup: BeautifulSoup) -> None:
    path = root / "chapters" / f"{chapter_id}.html"
    path.write_text(str(soup).strip() + "\n", encoding="utf-8")


def replace_first_paragraph_after(soup: BeautifulSoup, heading_id: str, html: str) -> None:
    heading = soup.find(id=heading_id)
    if heading is None:
        raise AssertionError(f"missing heading {heading_id}")
    node = heading.find_next_sibling()
    while node is not None and getattr(node, "name", None) is None:
        node = node.find_next_sibling()
    if node is None or node.name != "p":
        raise AssertionError(f"missing paragraph after {heading_id}")
    node.replace_with(BeautifulSoup(html, "html.parser"))


def patch_ch03(root: Path) -> None:
    soup = read_soup(root, "ch03")
    replace_first_paragraph_after(
        soup,
        "Stolper–Samuelson",
        r"""<p>在標準 2×2 Heckscher–Ohlin 模型中，若兩種商品都持續生產、技術相同且沒有要素密集度反轉，某商品相對價格上升會提高密集使用於該商品之要素的實質報酬，並降低另一要素的實質報酬；這是貿易價格變動與所得分配連結的基準結果，不應脫離模型條件無限外推。</p>""",
    )
    replace_first_paragraph_after(
        soup,
        "Rybczynski-效果",
        r"""<p>在標準 2×2 模型中，商品價格固定、兩種商品都持續生產且要素充分就業時，一種要素供給增加會使密集使用該要素的產業產出擴張，另一產業產出收縮。這是供給面重新配置，不是需求增加造成的雙雙擴張。</p>""",
    )
    write_soup(root, "ch03", soup)


def patch_ch05(root: Path) -> None:
    soup = read_soup(root, "ch05")
    replace_first_paragraph_after(
        soup,
        "獨占性競爭",
        r"""<p>獨占性競爭下廠商產品有差異、各自面對向下傾斜需求，但長期自由進出使超額利潤趨近零。兩國市場整合後，每位消費者通常可接觸更多差異化品種，代表性廠商也能在較大規模上生產；但整合後世界廠商總數不必高於兩國封閉時廠商數的總和，重點是市場規模、品種可得性與單廠規模同時改變。</p>""",
    )
    write_soup(root, "ch05", soup)


def patch_ch06(root: Path) -> None:
    soup = read_soup(root, "ch06")
    replace_first_paragraph_after(
        soup,
        "傾銷的經濟學定義",
        r"""<p>要先把「國際價格歧視」與「傾銷」分開。市場可分割且需求彈性不同時，同一廠商可能在不同國家收取不同價格，這是國際價格歧視；但不同市場價格不相同本身並不足以判定傾銷。國際貿易的標準基準與 WTO 反傾銷規則都把傾銷核心放在「出口價格低於正常價值」，最簡化的可比情形是出口價低於出口國國內可比價格。傾銷也不等於掠奪性定價；是否構成法律上的反傾銷案件還要依正常價值、損害與因果關係等規則判定。</p>""",
    )
    write_soup(root, "ch06", soup)


def patch_ch07(root: Path) -> None:
    soup = read_soup(root, "ch07")
    replace_first_paragraph_after(
        soup,
        "福利分解",
        r"""<p>價格上升使消費者剩餘下降、生產者剩餘上升，政府取得關稅收入。小國沒有改善世界貿易條件的利益，因此總福利下降；在教科書常用的線性供需圖中，淨損失畫成生產扭曲與消費扭曲兩個三角形。一般而言，重點是這兩類資源錯置，而不是「政府收到關稅」本身造成效率損失。</p>""",
    )
    write_soup(root, "ch07", soup)


def patch_ch08(root: Path) -> None:
    soup = read_soup(root, "ch08")
    replace_first_paragraph_after(
        soup,
        "出口補貼",
        r"""<p>出口補貼提高出口誘因。在標準小國、單一出口品模型中，若每單位出口補貼為 s，國內價格可由世界價格提高到約 \(P_w+s\)：消費者受損、生產者受益，政府按出口量支付補貼。做福利分解時，政府補貼支出是必須列入的財政項目，但它不是在生產與消費扭曲之外再加一次的「額外效率損失」；把消費者、生產者與政府三者合併後，小國的淨無謂損失來自過度生產與不足消費兩類扭曲。若是大國，還要另外計入可能惡化的貿易條件。</p>""",
    )
    write_soup(root, "ch08", soup)


def patch_ch11(root: Path) -> None:
    soup = read_soup(root, "ch11")
    replace_first_paragraph_after(
        soup,
        "金融帳與本書符號",
        r"""<p>本書計算題為了直觀地表達「資金流入」，明確定義 \(FA_{in}\) 為淨金融流入，即「淨負債發生額 − 淨金融資產取得額」。這與 IMF 現行 BPM7 金融帳的平衡項方向相反：BPM7 以「淨金融資產取得額 − 淨負債發生額」表示金融帳的淨貸出／淨借入，因此可把本書記號理解為 \(FA_{in}=-FA_{BPM7}\)。若暫時忽略資本帳與統計差異，本書使用 \(CA+FA_{in}=0\)；遇到官方資料或其他教材時，必須先讀其符號定義，不能只看正負號判斷對錯。</p>""",
    )
    replace_first_paragraph_after(
        soup,
        "雙重記帳",
        r"""<p>出口商品而取得外國存款時，會同時記錄一筆經常帳收入與一筆對外金融資產增加。依 BPM7 的金融帳方向，金融資產取得增加是正項；依本書 \(FA_{in}\) 的「淨流入為正」記號，同一筆資產增加則使 \(FA_{in}\) 為負，正好與正的經常帳項目配對。每一筆跨境交易都有對應項目，因此必須在同一套符號下檢查平衡。</p>""",
    )
    write_soup(root, "ch11", soup)


def patch_ch13(root: Path) -> None:
    soup = read_soup(root, "ch13")
    replace_first_paragraph_after(
        soup,
        "拋補利率平價-CIP",
        r"""<p>若 S 與 F 都採 NT$/US$，比較的是相同到期日、相近信用與流動性風險的可交易資產，且沒有具約束力的資本管制與足以阻斷套利的交易成本，拋補利率平價可寫成 \(1+i_{TW}=(F/S)(1+i_{US})\)。投資人用遠期鎖定未來換回新臺幣的匯率，因此這是一個無套利基準；現實中的融資利差、交易成本、信用風險與資本限制會形成偏離區間。</p>""",
    )
    write_soup(root, "ch13", soup)


def patch_ch14(root: Path) -> None:
    soup = read_soup(root, "ch14")
    replace_first_paragraph_after(
        soup,
        "絕對與相對-PPP",
        r"""<p>在 S=NT$/US$ 下，若比較的是同一個可比商品籃，絕對 PPP 的簡化式是 \(S=P_{TW}/P_{US}\)；相對 PPP 則近似為 \(Δ S/S≈π_{TW}-π_{US}\)，所以本國通膨較高時，本幣長期傾向貶值。要注意：跨國 CPI 通常是各國以不同基期正規化的指數，不能把兩國「CPI 指數水準」直接相除當成絕對 PPP 匯率；絕對 PPP 需要可比價格水準或同籃商品價格。</p>""",
    )
    write_soup(root, "ch14", soup)


def patch_ch16(root: Path) -> None:
    soup = read_soup(root, "ch16")
    replace_first_paragraph_after(
        soup,
        "貶值Marshall–Lerner-與-J-曲線",
        r"""<p>本幣貶值能否改善貿易餘額，取決於出口與進口數量對相對價格的反應。教科書常見的 Marshall–Lerner「進出口需求價格彈性絕對值之和大於 1」是標準特例：通常還隱含供給高度有彈性／價格可充分傳遞，且以初始貿易大致平衡為基準；若初始進出口額不等、供給彈性有限或匯率傳遞不完全，一般條件要相應調整。短期又可能因契約、交貨、定價貨幣與數量反應較慢，使進口的本幣支出先上升、之後數量才調整，形成 J 曲線直覺；它不是每次貶值都必然出現的定律。</p>""",
    )
    write_soup(root, "ch16", soup)


def patch_ch18(root: Path) -> None:
    soup = read_soup(root, "ch18")
    replace_first_paragraph_after(
        soup,
        "Bretton-Woods",
        r"""<p>二戰後 Bretton Woods 制度以「其他會員國貨幣維持對美元的可調整固定匯率」為核心，而美國則承諾按官方價格把外國官方持有的美元兌換為黃金；這不是一般民眾可隨時把美元拿去兌金的全面金本位。制度同時容許較多資本管制並由 IMF 等國際機構支撐，最終因流動性、信心與國內外政策矛盾瓦解，之後主要貨幣轉向浮動。</p>""",
    )
    write_soup(root, "ch18", soup)


def patch_appendix_b(root: Path) -> None:
    soup = read_soup(root, "appendix-b")
    paragraphs = soup.find_all("p")
    target = next((p for p in paragraphs if "不要把絕對利益當比較利益" in p.get_text()), None)
    if target is None:
        raise AssertionError("appendix-b common-mistakes paragraph not found")
    target.string = (
        "不要把絕對利益當比較利益、不要把消費者損失全算成社會淨損失、"
        "不要把政府補貼支出在生產／消費扭曲之外再算一次效率損失、"
        "不要把配額租固定當政府收入、不要把 CA=S-I 當單向因果、"
        "不要把遠期匯率當未來即期的保證預測、不要直接用兩國各自基期的 CPI 指數水準相除求絕對 PPP，"
        "也不要在沒有匯率單位時直接判斷「上升就是升值或貶值」。"
    )
    write_soup(root, "appendix-b", soup)


def update_questions(root: Path) -> None:
    path = root / "questions.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["version"] != SOURCE_VERSION:
        raise AssertionError(f"unexpected questions version {data['version']}")
    q = {item["id"]: item for item in data["items"]}

    q["ch03-q03"]["question"] = "在標準 2×2、兩商品都持續生產且無要素密集度反轉等條件下，勞動密集品相對價格上升時，勞動實質報酬如何？"
    q["ch03-q03"]["explanation"] = "Stolper–Samuelson 在這組基準條件下，將商品相對價格上升連到該商品密集要素的實質報酬上升；條件不成立時不能機械外推。"
    q["ch03-q04"]["question"] = "在標準 Rybczynski 條件下，商品價格固定、兩商品都持續生產時，資本供給增加，資本密集品產出如何？"
    q["ch03-q04"]["explanation"] = "Rybczynski 效果使密集使用增加要素的產業擴張、另一產業收縮；這依賴商品價格固定與多樣化生產等基準條件。"

    q["ch05-q03"]["answer"] = "每位消費者可接觸的品種通常增加，代表性廠商規模擴大。"
    q["ch05-q03"]["explanation"] = "市場整合擴大單一市場，使消費者可接觸更多差異化品種、廠商生產規模上升；但世界廠商總數不必高於兩國封閉時廠商數之和。"

    q["ch06-q03"]["question"] = "同一廠商在可分割的兩個國家市場依需求彈性設定不同價格，單憑這件事最適合先稱為什麼？"
    q["ch06-q03"]["answer"] = "國際價格歧視；尚不足以單憑此點判定傾銷。"
    q["ch06-q03"]["explanation"] = "不同市場差別定價是價格歧視。傾銷的標準核心是出口價格低於正常價值；最簡化的可比情形是出口價低於出口國國內可比價格。"

    q["ch08-q03"]["explanation"] = "政府補貼支出必須列入福利帳，但不是在扭曲之外再加一次的資源損失；消費者、生產者與政府合併後，小國的淨無謂損失來自過度生產與不足消費兩類扭曲。"

    q["ch11-q05"]["explanation"] = "不應。IMF 現行 BPM7 的金融帳平衡項採「淨金融資產取得減淨負債發生」方向；本書 FA_in 則定義為淨金融流入，方向相反。先讀定義再套恆等式。"

    q["ch14-q01"]["question"] = "同一個可比商品籃在台灣價格為 NT$120、在美國為 US$4，依簡化絕對 PPP，S 應是多少 NT$/US$？"
    q["ch14-q01"]["explanation"] = "S=P_TW/P_US=120/4=30。這裡使用同一可比商品籃的價格；一般不能直接拿兩國各自基期的 CPI 指數水準相除。"

    data["version"] = TARGET_VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def refresh_search(root: Path) -> None:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    path = root / "search.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    chapter_map = {item["id"]: item for item in manifest["chapters"]}
    for entry in data["entries"]:
        cid = entry["chapterId"]
        if cid not in TOUCHED_CHAPTERS:
            continue
        chapter = chapter_map[cid]
        soup = BeautifulSoup((root / chapter["file"]).read_text(encoding="utf-8"), "html.parser")
        if cid.startswith("appendix-"):
            first = soup.find("p")
            if first is not None:
                entry["text"] = first.get_text(" ", strip=True)
            continue
        if entry["page"] == 0:
            first = soup.find("p")
            if first is None:
                raise AssertionError(f"missing intro paragraph {cid}")
            entry["text"] = first.get_text(" ", strip=True)
        else:
            headings = [h for h in soup.find_all("h2") if "理解檢查" not in h.get_text(" ", strip=True)]
            index = entry["page"] - 1
            if index >= len(headings):
                raise AssertionError(f"search page out of range {cid} {entry['page']}")
            heading = headings[index]
            paragraph = heading.find_next_sibling("p")
            if paragraph is None:
                raise AssertionError(f"missing indexed paragraph {cid} {entry['page']}")
            entry["title"] = heading.get_text(" ", strip=True)
            entry["text"] = paragraph.get_text(" ", strip=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_manifest(root: Path) -> None:
    path = root / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["version"] != SOURCE_VERSION:
        raise AssertionError(f"unexpected manifest version {data['version']}")
    data["version"] = TARGET_VERSION
    data["updatedAt"] = "2026-07-29"
    note = {
        "version": TARGET_VERSION,
        "date": "2026-07-29",
        "title": "發布後第二次獨立內容複核與糾錯",
        "changes": [
            "精確化 Stolper–Samuelson、Rybczynski、獨占性競爭與傾銷的模型條件與術語邊界",
            "修正出口補貼福利分解，明確區分政府補貼支出與真正的生產／消費無謂損失",
            "依 IMF BPM7 更新國際收支金融帳符號對照，補強 CIP、PPP、Marshall–Lerner 與 Bretton Woods 的適用條件",
            "同步修正 7 題題幹、答案或詳解；章節 ID、題目 ID 與題數均未變",
        ],
        "progressImpact": "內容精確化與糾錯；章節 ID、題目 ID、題數與儲存鍵不變，既有閱讀進度與錯題紀錄可沿用。",
    }
    data["releaseNotes"] = [note] + [x for x in data.get("releaseNotes", []) if x.get("version") != TARGET_VERSION]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(site_root: str) -> None:
    root = Path(site_root) / "books" / BOOK_ID
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    questions = json.loads((root / "questions.json").read_text(encoding="utf-8"))
    if manifest["version"] != SOURCE_VERSION or questions["version"] != SOURCE_VERSION:
        raise AssertionError("international economics v2 patch requires v1 source")

    patch_ch03(root)
    patch_ch05(root)
    patch_ch06(root)
    patch_ch07(root)
    patch_ch08(root)
    patch_ch11(root)
    patch_ch13(root)
    patch_ch14(root)
    patch_ch16(root)
    patch_ch18(root)
    patch_appendix_b(root)
    update_questions(root)
    refresh_search(root)
    update_manifest(root)
    print(
        f"INTERNATIONAL_ECONOMICS_V2_PATCH_OK touched_chapters={len(TOUCHED_CHAPTERS)} "
        f"question_adjustments={len(QUESTION_ADJUSTMENTS)} target={TARGET_VERSION}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: patch_international_economics_v2.py SITE_ROOT")
    main(sys.argv[1])
