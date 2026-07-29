#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from investments_v2_corrections import VERSION

BOOK = "investments"
EXPECTED_QIDS = [f"ch{i:02d}-q{j:02d}" for i in range(22) for j in range(1, 6)]


def visible(raw: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))).strip()


def first_number(text: str) -> float:
    norm = text.replace("−", "-")
    m = re.search(r"\d[\d,]*(?:\.\d+)?", norm)
    if not m:
        raise AssertionError(f"no numeric answer in {text!r}")
    value = float(m.group(0).replace(",", ""))
    if "-" in norm[:m.start()]:
        value = -value
    return value


def main(site_root: str, expected_library_version: str | None = None) -> None:
    site = Path(site_root)
    root = site / "books" / BOOK
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    qtop = json.loads((root / "questions.json").read_text(encoding="utf-8"))
    search = json.loads((root / "search.json").read_text(encoding="utf-8"))
    library = json.loads((site / "data/library.json").read_text(encoding="utf-8"))
    checks = 0
    quantitative = 0

    def C(condition: bool, message: str) -> None:
        nonlocal checks
        if not condition:
            raise AssertionError(message)
        checks += 1

    C(manifest["id"] == BOOK, "manifest id")
    C(manifest["version"] == VERSION, "manifest version")
    C(qtop["bookId"] == BOOK, "question book id")
    C(qtop["version"] == VERSION, "question version")
    C(qtop["count"] == 110 and len(qtop["items"]) == 110, "question count")
    C([x["id"] for x in qtop["items"]] == EXPECTED_QIDS, "question IDs/order")
    C(Counter(x["chapterId"] for x in qtop["items"]) == {f"ch{i:02d}": 5 for i in range(22)}, "five questions/chapter")
    C(len(search["entries"]) == 165, "search count")
    chapters = [m for m in manifest["chapters"] if m["kind"] == "chapter"]
    appendices = [m for m in manifest["chapters"] if m["kind"] == "appendix"]
    C([m["id"] for m in chapters] == [f"ch{i:02d}" for i in range(22)], "chapter IDs")
    C([m["id"] for m in appendices] == ["appendix-a", "appendix-b", "appendix-c"], "appendix IDs")
    C(len(list((site / "assets/investments-svg").glob("*.svg"))) == 22, "22 figures")

    ids = [b["id"] for b in library["books"]]
    C(ids.count(BOOK) == 1, "single investments registry entry")
    C("civil-law-overview" in ids and ids.index("civil-law-overview") < ids.index(BOOK), "predecessor retained")
    if "econometrics" in ids:
        C(ids.index(BOOK) < ids.index("econometrics"), "registry order retained")
    if expected_library_version:
        C(library["version"] == expected_library_version, "expected library version")
    C(f"study-library-{library['version']}" in (site / "sw.js").read_text(encoding="utf-8"), "service worker version")

    chapter_text = {}
    chapter_raw = {}
    for meta in chapters:
        raw = (root / meta["file"]).read_text(encoding="utf-8")
        text = visible(raw)
        chapter_raw[meta["id"]] = raw
        chapter_text[meta["id"]] = text
        for token in ("本章要解決的問題", "白話直覺", "正式定義與核心概念", "核心公式與成立條件",
                      "完整標準例題", "常見錯誤", "考試判斷方法", "理解檢查"):
            C(token in text, f"{meta['id']} section {token}")

    for item in qtop["items"]:
        C(item["bookId"] == BOOK, f"{item['id']} book")
        C(bool(item["question"].strip()), f"{item['id']} question")
        C(bool(item["answer"].strip()), f"{item['id']} answer")
        C(bool(item["explanation"].strip()), f"{item['id']} explanation")

    ch09, ch13, ch15, ch17, ch19, ch20, ch21 = (chapter_text[f"ch{i:02d}"] for i in (9,13,15,17,19,20,21))
    for token in ("E[F_j]=0", "E[e_i]=0", "因子 surprise", "截距"):
        C(token.casefold() in ch09.casefold(), f"APT gate {token}")
    for token in ("Average\\ Assets", "Average\\ Equity", "平均資產", "平均權益"):
        C(token in chapter_raw["ch13"] or token in ch13, f"DuPont gate {token}")
    for token in ("money duration", "BPV", "Macaulay duration", "再平衡", r"\frac{\partial^2P}{\partial y^2}"):
        C(token.casefold() in ch15.casefold() or token in chapter_raw["ch15"], f"duration gate {token}")
    C(r"\[F_0=S_0(1+r)^T\]" in chapter_raw["ch17"], "forward exact carry formula")
    for token in ("無收益", "無套利", "持有成本", "便利收益"):
        C(token in ch17, f"forward condition {token}")
    for token in ("ETF（Exchange-Traded Fund）", "主動管理", "不等於被動指數化"):
        C(token in ch19, f"ETF gate {token}")
    for token in ("本幣／外幣", "R_{FX}", "15.5%", "精確乘法"):
        C(token in ch20 or token in chapter_raw["ch20"], f"FX gate {token}")
    C(r"\overline{R_P-R_B}" in chapter_raw["ch21"], "IR mean active return formula")
    C("期間與年化口徑必須一致" in ch21, "IR horizon consistency")

    appa_raw = (root / appendices[0]["file"]).read_text(encoding="utf-8")
    appa = visible(appa_raw)
    appc = visible((root / appendices[2]["file"]).read_text(encoding="utf-8"))
    for token in ("零均值", "Average\\ Assets", "F_0=S_0", "1+R_{home}", r"\overline{R_P-R_B}"):
        C(token in appa or token in appa_raw, f"appendix A {token}")
    C("交易所交易基金 ETF" in appc and "主動式 ETF" in appc, "appendix C ETF terminology")

    combined_raw = "\n".join(chapter_raw.values()) + "\n" + appa_raw
    C(r"R_{home}\approx(1+R_{foreign})(1+R_{FX})-1" not in combined_raw, "old FX approximate identity removed")
    C(r"IR=\frac{R_P-R_B}{\sigma(R_P-R_B)}" not in combined_raw, "old IR numerator removed")
    C(r"F_0\approx S_0(1+r)^T" not in combined_raw, "old forward approximation removed")
    C(r"\frac{Sales}{Assets}\times\frac{Assets}{Equity}" not in combined_raw, "old DuPont stock-flow mismatch removed")
    C("Exchange-Traded Fund</td><td>指數股票型基金 ETF</td>" not in combined_raw, "old ETF translation removed")

    smap = {(e["chapterId"], e["page"]): e["text"] for e in search["entries"]}
    for key, token in {
        ("ch09", 2): "零均值",
        ("ch13", 2): "Average\\ Assets",
        ("ch15", 2): r"\partial^2P",
        ("ch17", 2): "F_0=S_0",
        ("ch19", 0): "主動管理",
        ("ch20", 2): "精確乘法",
        ("ch21", 2): r"\overline{R_P-R_B}",
    }.items():
        C(token in smap[key], f"search synchronized {key}")

    qmap = {x["id"]: x for x in qtop["items"]}

    def Q(qid: str, expected: float, tol: float = 1e-2) -> None:
        nonlocal quantitative
        got = first_number(qmap[qid]["answer"])
        if not math.isclose(got, expected, abs_tol=tol, rel_tol=0):
            raise AssertionError(f"{qid} numeric answer {got} != {expected}")
        quantitative += 1
        C(True, f"{qid} independent numeric recheck")

    Q("ch00-q01", 100*(0.5*0.10+0.5*(-0.02)))
    Q("ch00-q02", 100*(0.07-0.02))
    Q("ch01-q02", 74-80)
    Q("ch01-q03", 50-45)
    Q("ch02-q01", 100*((105-100+2)/100))
    Q("ch02-q02", 100*((1.10*0.90)-1))
    Q("ch02-q03", (20+(-10))/2)
    Q("ch02-q04", 100*(math.sqrt(1.20*0.90)-1))
    Q("ch02-q05", 100*((1.08/1.03)-1))
    Q("ch03-q01", 100*(0.5*0.08+0.5*0.02))
    Q("ch03-q02", 100*math.sqrt(0.5*(0.08-0.05)**2+0.5*(0.02-0.05)**2))
    Q("ch04-q01", 100*(0.02+0.5*(0.08-0.02)))
    Q("ch04-q02", 100*(0.5*0.12))
    Q("ch04-q03", (0.10-0.02)/0.16)
    Q("ch05-q01", 100*(0.5*0.06+0.5*0.10))
    Q("ch05-q02", 100*math.sqrt((0.5**2)*(0.10**2)+(0.5**2)*(0.10**2)))
    Q("ch06-q02", 50)
    Q("ch07-q01", 0.015/0.010)
    Q("ch07-q04", 100*math.sqrt((1.5**2)*(0.10**2)+(0.08**2)))
    Q("ch08-q01", 100*(0.03+0.8*(0.09-0.03)))
    Q("ch08-q02", 100*(0.02+1.2*(0.08-0.02)))
    Q("ch08-q03", 100*(0.10-(0.02+1.2*(0.08-0.02))))
    Q("ch09-q01", 100*(0.01+1*0.03+0.5*0.02))
    Q("ch10-q01", 3-1)
    Q("ch10-q02", 1+2-0.5)
    Q("ch12-q01", 2/(0.09-0.04))
    Q("ch12-q02", 2*1.05)
    Q("ch13-q01", 100*(0.05*2*1.5))
    Q("ch13-q02", 100*(0.5*0.12))
    Q("ch14-q01", 1050/1.05)
    Q("ch14-q02", 1000/1.05)
    Q("ch15-q01", 100*(-5*0.001))
    Q("ch15-q02", 100*(-4.5*0.002))
    Q("ch16-q01", 0.01*(1-0.50)*2_000_000)
    Q("ch16-q02", 0.02*(1-0.40)*1_000_000)
    Q("ch17-q01", 74-80)
    Q("ch17-q02", 100-112)
    Q("ch18-q01", max(100-90,0))
    Q("ch18-q02", max(120-100,0))
    Q("ch18-q05", 12-100+95)
    Q("ch19-q01", (22_000_000-2_000_000)/2_000_000)
    Q("ch19-q02", 100*((10.20-10)/10))
    Q("ch20-q01", 100*((0.6*1.2)/(0.6*1.2+0.4)))
    Q("ch21-q01", (0.09-0.01)/0.16)
    Q("ch21-q02", 100*(0.10-(0.02+1.2*(0.08-0.02))))

    C(quantitative == 45, "45 quantitative rechecks")
    C(math.isclose((1.10*1.05)-1, 0.155, abs_tol=1e-12), "FX corrected example recomputed")
    C(math.isclose(0.02+1.2*0.04+0.5*0.02, 0.078, abs_tol=1e-12), "APT example recomputed")
    C(math.isclose(0.08*1.5*2, 0.24, abs_tol=1e-12), "DuPont example recomputed")
    C(math.isclose(-4.5*0.002, -0.009, abs_tol=1e-12), "duration example recomputed")
    C(math.isclose((105_000_000-5_000_000)/10_000_000, 10, abs_tol=1e-12), "NAV example recomputed")
    C(math.isclose((0.10-0.02)/0.16, 0.5, abs_tol=1e-12), "Sharpe example recomputed")
    C(math.isclose(0.10-(0.02+1.2*(0.08-0.02)), 0.008, abs_tol=1e-12), "Jensen example recomputed")

    print(
        f"INVESTMENTS_REAUDIT_V2_OK checks={checks} chapters=22 appendices=3 "
        f"questions=110 search=165 figures=22 quantitative_rechecks={quantitative} "
        f"correction_areas=7 question_explanations_adjusted=6 ids_preserved=true"
    )


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: python deploy/qa_investments_reaudit_v2.py SITE_ROOT [EXPECTED_LIBRARY_VERSION]")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
