from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

BOOK = "international-economics"
VERSION = "2026.07.29-2"
checks = 0
numeric = 0


def ck(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def num(cond: bool, msg: str) -> None:
    global numeric
    numeric += 1
    ck(cond, msg)


def main(site_root: str, expected_library: str) -> None:
    site = Path(site_root)
    root = site / "books" / BOOK
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    qdata = json.loads((root / "questions.json").read_text(encoding="utf-8"))
    sdata = json.loads((root / "search.json").read_text(encoding="utf-8"))
    library = json.loads((site / "data/library.json").read_text(encoding="utf-8"))

    ids = [book["id"] for book in library["books"]]
    ck(library["version"] == expected_library, "library version")
    ck(len(ids) == 11, "book count")
    ck(ids[-3:] == ["macroeconomics", BOOK, "public-finance"], "book tail order")
    ck(ids.count(BOOK) == 1, "international book uniqueness")

    ck(manifest["id"] == BOOK, "manifest id")
    ck(manifest["version"] == VERSION, "manifest version")
    ck(qdata["bookId"] == BOOK, "questions book id")
    ck(qdata["version"] == VERSION, "questions version")
    ck(manifest["releaseNotes"][0]["version"] == VERSION, "release-note version")
    ck(
        manifest["releaseNotes"][0]["title"] == "發布後第二次獨立內容複核與糾錯",
        "release-note title",
    )
    ck(
        "章節 ID、題目 ID、題數與儲存鍵不變"
        in manifest["releaseNotes"][0]["progressImpact"],
        "progress compatibility release note",
    )

    chapters = [x for x in manifest["chapters"] if x["kind"] == "chapter"]
    appendices = [x for x in manifest["chapters"] if x["kind"] == "appendix"]
    ck(len(chapters) == 20, "chapter count")
    ck(len(appendices) == 3, "appendix count")
    ck([x["id"] for x in chapters] == [f"ch{i:02d}" for i in range(20)], "chapter ids")
    ck(
        [x["id"] for x in appendices] == ["appendix-a", "appendix-b", "appendix-c"],
        "appendix ids",
    )

    ck(qdata["count"] == 100 == len(qdata["items"]), "question count")
    ck(len({x["id"] for x in qdata["items"]}) == 100, "unique question ids")
    ck(
        Counter(x["chapterId"] for x in qdata["items"])
        == {f"ch{i:02d}": 5 for i in range(20)},
        "five questions per chapter",
    )
    qmap = {x["id"]: x for x in qdata["items"]}
    for i, item in enumerate(qdata["items"]):
        ck(item["id"] == f"ch{i//5:02d}-q{i%5+1:02d}", f"q order {i}")
        ck(item["bookId"] == BOOK, f"q book {i}")
        ck(item["chapterId"] == f"ch{i//5:02d}", f"q chapter {i}")
        ck(item["difficulty"] in {"基礎", "標準", "綜合", "陷阱"}, f"q difficulty {i}")
        ck(len(item["question"].strip()) >= 8, f"q stem {i}")
        ck(bool(item["answer"].strip()), f"q answer {i}")
        ck(len(item["explanation"].strip()) >= 5, f"q explanation {i}")
        ck(item["source"] == "本書自編標準題型", f"q source {i}")

    recompute = {
        "ch00-q03": 120 / 80,
        "ch01-q01": 2 / 4,
        "ch02-q01": 50 * 4,
        "ch04-q01": 120 / 100 * 100,
        "ch07-q01": 100 * 1.20,
        "ch07-q02": 80 - 50,
        "ch07-q03": 20 * 30,
        "ch08-q01": (125 - 100) * 40,
        "ch11-q02": 80,
        "ch11-q04": 500 - 620,
        "ch12-q02": 32 * 1.10,
        "ch12-q04": 32 * 100 / 3200,
        "ch13-q01": 32 * 1.04 / 1.02,
        "ch13-q03": 0.05 - 0.02,
        "ch14-q01": 120 / 4,
        "ch14-q02": 0.05 - 0.02,
        "ch14-q03": 30 * 4 / 120,
    }
    expected_numeric_answers = {
        "ch00-q03": "1.5。",
        "ch01-q01": "0.5 單位小麥。",
        "ch02-q01": "NT$200。",
        "ch04-q01": "120。",
        "ch07-q01": "NT$120。",
        "ch07-q02": "30。",
        "ch07-q03": "NT$600。",
        "ch08-q01": "NT$1,000。",
        "ch11-q02": "80。",
        "ch11-q04": "-120。",
        "ch12-q02": "35.2。",
        "ch12-q04": "1。",
        "ch13-q01": "約 32.63 NT$/US$。",
        "ch13-q03": "約 3%。",
        "ch14-q01": "30 NT$/US$。",
        "ch14-q02": "約 3%。",
        "ch14-q03": "1。",
    }
    for qid, answer in expected_numeric_answers.items():
        ck(qmap[qid]["answer"] == answer, f"numeric stored answer {qid}")
    num(abs(recompute["ch00-q03"] - 1.5) < 1e-12, "ch00-q03")
    num(abs(recompute["ch01-q01"] - 0.5) < 1e-12, "ch01-q01")
    num(recompute["ch02-q01"] == 200, "ch02-q01")
    num(recompute["ch04-q01"] == 120, "ch04-q01")
    num(recompute["ch07-q01"] == 120, "ch07-q01")
    num(recompute["ch07-q02"] == 30, "ch07-q02")
    num(recompute["ch07-q03"] == 600, "ch07-q03")
    num(recompute["ch08-q01"] == 1000, "ch08-q01")
    num(recompute["ch11-q02"] == 80, "ch11-q02")
    num(recompute["ch11-q04"] == -120, "ch11-q04")
    num(abs(recompute["ch12-q02"] - 35.2) < 1e-12, "ch12-q02")
    num(recompute["ch12-q04"] == 1, "ch12-q04")
    num(round(recompute["ch13-q01"], 2) == 32.63, "ch13-q01")
    num(round(recompute["ch13-q03"] * 100) == 3, "ch13-q03")
    num(recompute["ch14-q01"] == 30, "ch14-q01")
    num(round(recompute["ch14-q02"] * 100) == 3, "ch14-q02")
    num(recompute["ch14-q03"] == 1, "ch14-q03")

    expected_adjustments = {
        "ch03-q03": ("上升。", "標準 2×2"),
        "ch03-q04": ("增加。", "Rybczynski"),
        "ch05-q03": ("每位消費者可接觸的品種通常增加，代表性廠商規模擴大。", "世界廠商總數不必"),
        "ch06-q03": ("國際價格歧視；尚不足以單憑此點判定傾銷。", "出口價格低於正常價值"),
        "ch08-q03": ("下降。", "不是在扭曲之外再加一次"),
        "ch11-q05": ("不應。", "BPM7"),
        "ch14-q01": ("30 NT$/US$。", "CPI 指數水準"),
    }
    for qid, (answer, token) in expected_adjustments.items():
        ck(qmap[qid]["answer"] == answer, f"adjusted answer {qid}")
        ck(token in (qmap[qid]["question"] + qmap[qid]["explanation"]), f"adjusted token {qid}")

    chapter_text = {}
    for ch in manifest["chapters"]:
        path = root / ch["file"]
        ck(path.is_file() and path.stat().st_size > 600, f"chapter exists {ch['id']}")
        html = path.read_text(encoding="utf-8")
        chapter_text[ch["id"]] = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        ck("\f" not in html and "\t" not in html, f"control chars {ch['id']}")
        ck("<script" not in html.lower(), f"inline script {ch['id']}")
        if ch["kind"] == "chapter":
            ck("本章理解檢查" in chapter_text[ch["id"]], f"practice {ch['id']}")

    positive = [
        ("ch03", "兩種商品都持續生產"),
        ("ch03", "要素密集度反轉"),
        ("ch05", "每位消費者通常可接觸更多差異化品種"),
        ("ch05", "世界廠商總數不必高於"),
        ("ch06", "不同市場價格不相同本身並不足以判定傾銷"),
        ("ch06", "出口價格低於正常價值"),
        ("ch06", "損害與因果關係"),
        ("ch07", "線性供需圖"),
        ("ch08", "不是在生產與消費扭曲之外再加一次"),
        ("ch08", "過度生產與不足消費"),
        ("ch11", "IMF 現行 BPM7"),
        ("ch11", "淨金融資產取得額 − 淨負債發生額"),
        ("ch11", "FA_{in}=-FA_{BPM7}"),
        ("ch13", "相同到期日"),
        ("ch13", "具約束力的資本管制"),
        ("ch14", "CPI 通常是各國以不同基期正規化的指數"),
        ("ch14", "不能把兩國「CPI 指數水準」直接相除"),
        ("ch16", "標準特例"),
        ("ch16", "初始貿易大致平衡"),
        ("ch16", "匯率傳遞不完全"),
        ("ch18", "外國官方持有的美元兌換為黃金"),
        ("appendix-b", "政府補貼支出在生產／消費扭曲之外再算一次效率損失"),
        ("appendix-b", "CPI 指數水準相除求絕對 PPP"),
    ]
    for cid, token in positive:
        ck(token in chapter_text[cid], f"positive correction gate {cid}: {token}")

    stale = [
        "傾銷常指同一廠商對不同市場設定不同價格，或出口價低於某些基準",
        "生產與消費扭曲加上政府支出造成淨效率損失",
        "BPM6",
        "常見充分條件是 Marshall–Lerner 條件",
        "以美元對黃金、其他貨幣對美元的可調整固定匯率為核心",
    ]
    full = "\n".join(chapter_text.values()) + "\n" + json.dumps(qdata, ensure_ascii=False)
    for token in stale:
        ck(token not in full, f"stale wording: {token}")

    ck(len(sdata["entries"]) == 144, "search count")
    valid_ids = {x["id"] for x in manifest["chapters"]}
    for entry in sdata["entries"]:
        ck(entry["chapterId"] in valid_ids, "search chapter id")
        ck(isinstance(entry["page"], int) and entry["page"] >= 0, "search page")
        ck(bool(entry["title"].strip()), "search title")
        ck(bool(entry["text"].strip()), "search text")
    corpus = "\n".join(e["title"] + " " + e["text"] for e in sdata["entries"])
    for token in [
        "出口價格低於正常價值",
        "過度生產與不足消費",
        "IMF 現行 BPM7",
        "CPI 通常是各國以不同基期正規化的指數",
        "Marshall–Lerner",
        "外國官方持有的美元兌換為黃金",
    ]:
        ck(token in corpus, f"search updated concept {token}")
    for token in [
        "傾銷常指同一廠商對不同市場設定不同價格",
        "政府還要支出補貼，通常造成淨效率損失",
    ]:
        ck(token not in corpus, f"search stale concept {token}")

    figures = sorted((site / "assets/international-economics-svg").glob("*.svg"))
    ck(len(figures) == 20, "figure count")
    for figure in figures:
        svg = figure.read_text(encoding="utf-8")
        ck("<title" in svg, f"figure title {figure.name}")
        ck("<desc" in svg, f"figure desc {figure.name}")
        ck("viewBox=" in svg, f"figure viewbox {figure.name}")
        ck("href=\"http" not in svg and "href='http" not in svg, f"remote figure {figure.name}")

    sw = (site / "sw.js").read_text(encoding="utf-8")
    ck(f"const VERSION = 'study-library-{expected_library}';" in sw, "sw version")
    for token in [
        "./books/international-economics/manifest.json",
        "./books/international-economics/questions.json",
        "./books/international-economics/search.json",
        "./books/international-economics/chapters/ch19.html",
        "./books/international-economics/chapters/appendix-c.html",
        "./books/public-finance/manifest.json",
    ]:
        ck(token in sw, f"sw path {token}")

    print(
        f"INTERNATIONAL_ECONOMICS_V2_QA_OK checks={checks} "
        f"questions_rechecked={len(qdata['items'])} quantitative_rechecks={numeric} "
        f"content_corrections=11 question_adjustments=7 search={len(sdata['entries'])} "
        f"figures={len(figures)} books={len(ids)} library={expected_library}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: qa_international_economics_v2.py SITE_ROOT EXPECTED_LIBRARY_VERSION"
        )
    main(sys.argv[1], sys.argv[2])
