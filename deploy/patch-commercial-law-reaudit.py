#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

OLD_VERSION = "2026.07.28-1"
NEW_VERSION = "2026.07.29-1"

TEXT_REPLACEMENTS = [
    (
        "art8-public-company-scope",
        "非董事但實質執行董事業務或實質控制公司而指揮董事者，也可能負相應責任。",
        "另須注意，公司法第 8 條第 3 項只針對公開發行股票之公司：非董事而實質上執行董事業務，或實質控制公司人事、財務或業務經營並實質指揮董事執行業務者，才依該項與董事同負相應民事、刑事及行政責任。",
    ),
    (
        "public-company-board-five-directors",
        "公司法第 192 條原則上規定董事會不得少於 3 人，但非公開發行公司可依章程選擇不設董事會而置 1 人或 2 人董事。公開發行公司的董事人數另受證券交易法等特別規範。",
        "公司法第 192 條以董事會至少 3 人為通常架構，也允許公司依章程選擇不設董事會而置 1 人或 2 人董事；但已依證券交易法發行股票之公司受證交法第 26-3 條特別規範，董事會不得少於 5 人，因此不能只停在公司法的一般規則。",
    ),
    (
        "board-notice-three-versus-seven-days",
        "一般公司董事會原則至少於 3 日前通知董事及監察人，緊急情事可隨時召集。除法律另有規定外，董事會決議須過半數董事出席、出席董事過半數同意。",
        "依公司法第 204 條，一般規則是董事會召集原則於 3 日前通知董事及監察人，緊急情事可隨時召集；公開發行公司另依《公開發行公司董事會議事辦法》原則於 7 日前通知。除法律另有規定外，董事會決議須過半數董事出席、出席董事過半數同意。",
    ),
    (
        "interested-director-voting-exclusion",
        "董事對議案有自身利害關係時，應說明重要內容；其配偶、二親等內血親或具有控制從屬關係的公司有利害關係時，也可能視為董事自身有利害關係。董事長對內主持重要會議，對外代表公司。",
        "董事對議案有自身利害關係時，應說明重要內容；其配偶、二親等內血親或具有控制從屬關係的公司有利害關係時，也可能視為董事自身有利害關係。依第 206 條準用第 178 條及第 180 條第 2 項，若該利害關係有害於公司利益之虞，該董事不得加入表決，其表決權不算入已出席董事的表決權數。董事長對內主持重要會議，對外代表公司。",
    ),
    (
        "art194-one-year-stop-action",
        "公司法另讓符合條件的股東在董事會決議違反法令或章程時，請求董事會停止其行為。考題應區分『事前／進行中的制止』與『損害已發生後的賠償訴訟』。",
        "公司法第 194 條規定，董事會決議為違反法令或章程的行為時，繼續 1 年以上持有公司股份的股東得請求董事會停止其行為。這和第 214 條代表訴訟的『6 個月＋1%＋先請監察人、30 日』是不同門檻。考題應區分『事前／進行中的制止』與『損害已發生後的賠償訴訟』。",
    ),
    (
        "close-company-shareholder-cap-caveat",
        "公司法第 356-1 條把閉鎖性股份有限公司定義為股東人數不超過 50 人、章程定有股份轉讓限制、且非公開發行股票的公司。它仍是股份有限公司，但刻意降低股份自由流通性。",
        "公司法第 356-1 條把閉鎖性股份有限公司定義為股東人數不超過 50 人、章程定有股份轉讓限制、且非公開發行股票的公司；但中央主管機關得視社會經濟情況及實際需要增加股東人數上限。它仍是股份有限公司，但刻意降低股份自由流通性。",
    ),
    (
        "close-company-labor-contribution-conditions",
        "閉鎖性公司發起人在符合法定條件下，可用公司事業所需的財產、技術或勞務抵充出資；但原則不得公開發行或募集有價證券，法定例外如依法透過股權群眾募資平台。這正反映『封閉性換取設計彈性』。",
        "閉鎖性公司發起人在符合法定條件下，可用公司事業所需的財產、技術或勞務抵充出資；其中以技術或勞務出資須經全體股東同意並於章程載明，勞務出資另受主管機關公告比例上限。公司原則不得公開發行或募集有價證券，法定例外如依法透過股權群眾募資平台。這正反映『封閉性換取設計彈性』。",
    ),
    (
        "short-swing-security-scope",
        "上述內部人對公司上市股票，在取得後 6 個月內再賣出，或賣出後 6 個月內再買進並獲利時，公司應請求將利益歸於公司；證交法第 62 條並使第 157 條等規定準用於證券商營業處所買賣。重點不是證明他知道重大消息，而是看身分、證券、方向、期間與利益。",
        "上述內部人對公司上市股票，在取得後 6 個月內再賣出，或賣出後 6 個月內再買進並獲利時，公司應請求將利益歸於公司；公司發行其他具有股權性質之有價證券，也準用第 157 條。證交法第 62 條另使第 157 條準用於證券商營業處所的買賣，因此不能把短線交易理解成只適用上市股票。重點不是證明他知道重大消息，而是看身分、證券、方向、期間與利益。",
    ),
    (
        "insider-non-equity-bond-route",
        "法律要求行為人實際知悉重大影響股票價格的消息。重大消息包括涉及公司財務、業務、證券市場供求、公開收購，且其具體內容足以重大影響股價或正當投資人的投資決定者。單純市場傳言不當然等於法定重大消息。",
        "法律要求行為人實際知悉重大影響股票價格的消息。重大消息包括涉及公司財務、業務、證券市場供求、公開收購，且其具體內容足以重大影響股價或正當投資人的投資決定者。單純市場傳言不當然等於法定重大消息。另外，第 157-1 條第 2 項另處理重大影響公司支付本息能力的消息：法定主體實際知悉後，在消息明確、未公開前或公開後 18 小時內，不得賣出該公司上市或在證券商營業處所買賣的非股權性質公司債。",
    ),
    (
        "appendix-board-rules",
        "一般股東會通知：常會 20 日、臨時會 10 日；公開發行：30 日、15 日",
        "一般股東會通知：常會 20 日、臨時會 10 日；公開發行：30 日、15 日\n董事會召集：公司法一般規則 3 日前；公開發行公司原則 7 日前；已依證交法發行股票之公司董事至少 5 人",
    ),
    (
        "appendix-art194",
        "代表訴訟：繼續 6 個月＋持股 1%；先請監察人，30 日不提起後股東得代公司起訴",
        "停止違法董事會行為（§194）：繼續持股 1 年以上\n代表訴訟（§214）：繼續 6 個月＋持股 1%；先請監察人，30 日不提起後股東得代公司起訴",
    ),
    (
        "appendix-short-swing-scope",
        "短線交易：6 個月；請求權 2 年",
        "短線交易：6 個月；其他具有股權性質之有價證券準用；證券商營業處所買賣依 §62 準用；請求權 2 年",
    ),
]

QUESTION_UPDATES = {
    "ch02-q05": {
        "question": "在公開發行股票之公司，某人沒有董事名義，卻實質控制公司人事、財務或業務經營並實質指揮董事執行業務，是否一定因沒有職稱而不負董事責任？",
        "answer": "不一定。",
        "explanation": "公司法第 8 條第 3 項只針對公開發行股票之公司；符合實質執行董事業務或實質控制並指揮董事等要件者，可能與董事同負相應責任。",
    },
    "ch07-q01": {
        "explanation": "公司法第 192 條允許公司依章程採 1 或 2 名董事制度；但已依證交法發行股票之公司依第 26-3 條董事會不得少於 5 人，因此本題特別限定非公開發行公司。",
    },
    "ch07-q04": {
        "question": "董事對議案有自身利害關係且有害於公司利益之虞時，除了說明重要內容外，能否參與該案表決？",
        "answer": "不能。",
        "explanation": "公司法第 206 條準用第 178 條及第 180 條第 2 項；符合利益衝突排除要件時，不得加入表決，其表決權不算入已出席董事的表決權數。",
    },
    "ch08-q05": {
        "question": "公司法第 194 條請求停止董事會違法行為，與第 214 條股東代表訴訟的持股門檻是否相同？",
        "answer": "不同。",
        "explanation": "第 194 條著重繼續持股 1 年以上；第 214 條則要求繼續 6 個月以上且持有已發行股份總數 1% 以上，另有先書面請求監察人起訴的程序。",
    },
    "ch10-q01": {
        "explanation": "公司法第 356-1 條以不超過 50 人為基本定義之一，但中央主管機關得視社會經濟情況及實際需要增加股東人數上限。",
    },
    "ch16-q04": {
        "explanation": "董事屬法定內部人，取得上市股票後 6 個月內反向賣出獲利符合核心結構；其他具有股權性質之有價證券也準用第 157 條，證券商營業處所的買賣另有第 62 條準用。",
    },
}


def recursive_replace(value, old: str, new: str):
    count = 0
    if isinstance(value, str):
        count = value.count(old)
        return value.replace(old, new), count
    if isinstance(value, list):
        out = []
        for item in value:
            replaced, n = recursive_replace(item, old, new)
            out.append(replaced)
            count += n
        return out, count
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            replaced, n = recursive_replace(item, old, new)
            out[key] = replaced
            count += n
        return out, count
    return value, 0


def main() -> None:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    root = site / "books" / "commercial-law"
    manifest_path = root / "manifest.json"
    questions_path = root / "questions.json"
    search_path = root / "search.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    search = json.loads(search_path.read_text(encoding="utf-8"))
    if manifest.get("version") != OLD_VERSION or questions.get("version") != OLD_VERSION:
        raise AssertionError("unexpected commercial-law source version")

    chapter_files = [root / chapter["file"] for chapter in manifest["chapters"]]
    chapter_text = {path: path.read_text(encoding="utf-8") for path in chapter_files}

    applied = {}
    for label, old, new in TEXT_REPLACEMENTS:
        total = 0
        for path, text in list(chapter_text.items()):
            n = text.count(old)
            if n:
                chapter_text[path] = text.replace(old, new)
                total += n
        search, n = recursive_replace(search, old, new)
        total += n
        if total == 0:
            raise AssertionError(f"reaudit replacement not found: {label}")
        applied[label] = total

    for path, text in chapter_text.items():
        path.write_text(text, encoding="utf-8")

    by_id = {item["id"]: item for item in questions["items"]}
    if set(QUESTION_UPDATES) - set(by_id):
        raise AssertionError(f"missing question ids: {sorted(set(QUESTION_UPDATES) - set(by_id))}")
    for qid, fields in QUESTION_UPDATES.items():
        by_id[qid].update(fields)

    manifest["version"] = NEW_VERSION
    questions["version"] = NEW_VERSION
    if "version" in search:
        search["version"] = NEW_VERSION

    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    questions_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    merged = "\n".join(path.read_text(encoding="utf-8") for path in chapter_files)
    required = [
        "公開發行股票之公司",
        "第 26-3 條",
        "不得少於 5 人",
        "原則於 7 日前通知",
        "不算入已出席董事的表決權數",
        "繼續 1 年以上",
        "中央主管機關得視社會經濟情況及實際需要增加股東人數上限",
        "其他具有股權性質之有價證券",
        "非股權性質公司債",
    ]
    for token in required:
        if token not in merged:
            raise AssertionError(f"missing corrected legal content: {token}")
    forbidden = [
        "非董事但實質執行董事業務或實質控制公司而指揮董事者，也可能負相應責任。",
        "公開發行公司的董事人數另受證券交易法等特別規範。",
    ]
    for token in forbidden:
        if token in merged:
            raise AssertionError(f"stale legal wording remains: {token}")

    if len(questions["items"]) != 90:
        raise AssertionError("question count changed")
    if len(search["entries"]) != 111:
        raise AssertionError("search count changed")

    print("COMMERCIAL_LAW_REAUDIT_PATCH_OK", json.dumps(applied, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
