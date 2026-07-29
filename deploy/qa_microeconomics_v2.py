#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

BOOK = "microeconomics"
VERSION = "2026.07.29-2"
CHECKS = 0


def ck(cond: bool, msg: str) -> None:
    global CHECKS
    if not cond:
        raise AssertionError(msg)
    CHECKS += 1


def main(site_root: str) -> None:
    site = Path(site_root)
    book = site / "books" / BOOK
    manifest = json.loads((book / "manifest.json").read_text(encoding="utf-8"))
    questions_doc = json.loads((book / "questions.json").read_text(encoding="utf-8"))
    search_doc = json.loads((book / "search.json").read_text(encoding="utf-8"))
    questions = questions_doc["items"]

    ck(manifest["id"] == BOOK, "manifest id")
    ck(manifest["version"] == VERSION, "manifest version")
    ck(questions_doc["version"] == VERSION, "questions version")
    ck(manifest["releaseNotes"][0]["version"] == VERSION, "release note version")
    ck(manifest["releaseNotes"][0]["title"] == "發布後獨立二次複核與條件精確化", "release note title")

    chapters = [x for x in manifest["chapters"] if x["kind"] == "chapter"]
    appendices = [x for x in manifest["chapters"] if x["kind"] == "appendix"]
    ck(len(chapters) == 20, "20 chapters")
    ck(len(appendices) == 3, "3 appendices")
    ck([x["id"] for x in chapters] == [f"ch{i:02d}" for i in range(20)], "chapter ids")

    all_html = []
    for entry in manifest["chapters"]:
        path = book / entry["file"]
        ck(path.is_file(), f"missing {entry['file']}")
        text = path.read_text(encoding="utf-8")
        all_html.append(text)
        ck("<h2" in text, f"missing headings {entry['id']}")
        ck(not any(ord(c) < 32 and c not in "\n\r\t" for c in text), f"control char {entry['id']}")
        ck(text.count("<figure>") == (1 if entry["kind"] == "chapter" else 0), f"figure count {entry['id']}")
    corpus = "\n".join(all_html)

    ck(questions_doc["count"] == 100, "question count field")
    ck(len(questions) == 100, "100 questions")
    ck(len({q["id"] for q in questions}) == 100, "unique question ids")
    ck(Counter(q["chapterId"] for q in questions) == {f"ch{i:02d}": 5 for i in range(20)}, "five questions per chapter")
    expected_ids = {f"ch{i:02d}-q{j:02d}" for i in range(20) for j in range(1, 6)}
    ck({q["id"] for q in questions} == expected_ids, "question id set")
    for q in questions:
        for key in ("id", "bookId", "chapterId", "chapterTitle", "topic", "difficulty", "question", "answer", "explanation", "source"):
            ck(bool(q.get(key)), f"{q.get('id')} missing {key}")
        ck(q["bookId"] == BOOK, f"{q['id']} book id")

    ck(len(search_doc["entries"]) == 154, "154 search entries")
    chapter_ids = {x["id"] for x in manifest["chapters"]}
    for entry in search_doc["entries"]:
        ck(entry["chapterId"] in chapter_ids, "search chapter id")
        ck(bool(entry["title"]) and bool(entry["text"]), "search text")

    figures = sorted((site / "assets/microeconomics-svg").glob("*.svg"))
    ck(len(figures) == 20, "20 figures")
    for svg in figures:
        text = svg.read_text(encoding="utf-8")
        ck("<title" in text and "<desc" in text and "viewBox=" in text, f"svg metadata {svg.name}")

    required_phrases = [
        "可行集合為凸集、目標函數在其上嚴格凹",
        "任何最適點都會用盡預算",
        "\\bar u=v(p,m)",
        "準線性、所得效果為零",
        "只有正仿射轉換",
        "不能在沒有額外條件時把任意需求曲線面積直接當成精確福利",
        "混合策略的期望報酬",
        "產品價格與其他投入固定",
        "個別預算式以等號成立",
        "只有 \\(p\\cdot x_i\\le p\\cdot \\omega_i\\) 而未保證用盡預算時，不能直接推出等號",
        "若最適點在角點，應改用相應不等式條件",
        "凸的投入需求集合",
    ]
    for phrase in required_phrases:
        ck(phrase in corpus, f"missing corrected phrase: {phrase}")

    forbidden_phrases = [
        "若目標函數在可行集合上是嚴格凹函數，滿足一階條件的內點解通常就是唯一全域最大值",
        "若偏好局部非飽和，最適點通常用完預算",
        "若每位消費者都滿足預算限制，總超額需求向量",
        "報酬只需反映偏好排序；數值本身未必代表金額",
        "在沒有外部性、資訊問題、市場力量等扭曲時，競爭均衡的交易量",
    ]
    for phrase in forbidden_phrases:
        ck(phrase not in corpus, f"stale phrase remains: {phrase}")

    search_corpus = "\n".join(e["text"] for e in search_doc["entries"])
    for phrase in [
        "個別預算式以等號成立",
        "混合策略的期望報酬",
        "準線性偏好或可忽略所得效果",
        "MRP 曲線可直接作為個別企業的勞動需求曲線",
    ]:
        ck(phrase in search_corpus, f"search missing {phrase}")
    for phrase in forbidden_phrases:
        ck(phrase not in search_corpus, f"search stale {phrase}")

    qmap = {q["id"]: q for q in questions}
    ck(qmap["ch14-q03"]["question"] == "若某策略不論對手怎麼做，都嚴格優於自己所有其他策略，稱什麼？", "dominant strategy prompt")
    ck("原最適效用" in qmap["ch05-q04"]["explanation"], "Slutsky question explanation")
    ck("準線性偏好" in qmap["ch06-q05"]["explanation"], "consumer surplus question explanation")
    ck("用盡預算" in qmap["ch17-q03"]["question"], "Walras question condition")

    numeric_checks = {
        "ch00-q02": 12 / 2,
        "ch01-q03": 6 / 2,
        "ch02-q02": (0.5 * 600 / 10, 0.5 * 600 / 20),
        "ch08-q01": 0.5 * math.sqrt(100) + 0.5 * math.sqrt(400),
        "ch08-q02": 15**2,
        "ch08-q03": 250 - 225,
        "ch09-q02": 12 / 4,
        "ch10-q02": 300 / 600,
        "ch11-q03": 50 * 4,
        "ch13-q02": ((100 - 20) / 2, 100 - (100 - 20) / 2),
        "ch13-q03": 1 / 4,
        "ch15-q02": (90 - 30) / 3,
        "ch15-q03": 30,
        "ch16-q02": 80 * 3,
        "ch18-q02": 50 + 20,
    }
    numeric_targets = {
        "ch00-q02": 6, "ch01-q03": 3, "ch02-q02": (30, 15),
        "ch08-q01": 15, "ch08-q02": 225, "ch08-q03": 25,
        "ch09-q02": 3, "ch10-q02": 0.5, "ch11-q03": 200,
        "ch13-q02": (40, 60), "ch13-q03": 0.25,
        "ch15-q02": 20, "ch15-q03": 30, "ch16-q02": 240, "ch18-q02": 70,
    }
    expected_answers = {
        "ch00-q02": "\\(x=6\\)。", "ch01-q03": "3。", "ch02-q02": "\\(x=30,\\ y=15\\)。",
        "ch08-q01": "15。", "ch08-q02": "225。", "ch08-q03": "25。", "ch09-q02": "3。",
        "ch10-q02": "0.5。", "ch11-q03": "NT$200。", "ch13-q02": "\\(Q=40,\\ P=60\\)。",
        "ch13-q03": "0.25。", "ch15-q02": "20。", "ch15-q03": "30。", "ch16-q02": "NT$240。", "ch18-q02": "70。",
    }
    for qid, value in numeric_checks.items():
        ck(qmap[qid]["answer"] == expected_answers[qid], f"numeric answer text {qid}")
        target = numeric_targets[qid]
        if isinstance(value, tuple):
            ck(len(value) == len(target) and all(math.isclose(a, b, rel_tol=0, abs_tol=1e-12) for a, b in zip(value, target)), f"numeric tuple recompute {qid}")
        else:
            ck(math.isclose(value, target, rel_tol=0, abs_tol=1e-12), f"numeric recompute {qid}")

    logic_expected = {
        "ch03-q05": "不可以。", "ch05-q03": "不是。", "ch05-q05": "不一定。", "ch06-q02": "不符合。",
        "ch06-q05": "不一定。", "ch08-q05": "不會。", "ch09-q05": "不必然。", "ch11-q05": "不一定。",
        "ch12-q05": "不能。", "ch13-q05": "不會。", "ch14-q04": "不一定，典型囚犯困境不是。",
        "ch15-q05": "不一定。", "ch16-q05": "不必然。", "ch17-q04": "最後一個也必須出清。",
        "ch17-q05": "不是。", "ch18-q05": "不是。", "ch19-q01": "簽訂前。", "ch19-q02": "契約後不可觀察行動。",
        "ch19-q05": "不一定。", "ch14-q03": "嚴格優勢策略。",
    }
    for qid, expected in logic_expected.items():
        ck(qmap[qid]["answer"] == expected, f"logic answer {qid}")

    canonical = "\n".join(f"{q['id']}|{q['question']}|{q['answer']}|{q['explanation']}" for q in questions)
    ck(hashlib.sha256(canonical.encode()).hexdigest() == "b6d49afcb71bb8de7ce50068367828b7e4d31767f6e628439ffbeb3d4ade408d", "reviewed question snapshot")

    print(f"MICRO_V2_QA_OK checks={CHECKS} chapters=20 appendices=3 questions=100 search=154 figures=20 numeric_rechecks=15 logic_rechecks=20 version={VERSION}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
