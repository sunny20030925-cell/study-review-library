#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

LIBRARY_VERSION = "2026.07.29-7"
BOOK_ORDER = ["calculus", "accounting", "economics", "statistics", "commercial-law", "macroeconomics"]
EXPECTED_QUESTIONS = {
    "calculus": 73,
    "accounting": 70,
    "economics": 100,
    "statistics": 95,
    "commercial-law": 90,
    "macroeconomics": 100,
}

RELEASE_DATA = {
    "calculus": {"updatedAt": "2026-07-27", "releaseNotes": [{"version": "2026.07.27-3", "date": "2026-07-27", "title": "改回標準大一微積分本位", "changes": ["移除經濟學取向副標題與經濟專屬核心題型", "新增或強化中值定理、洛必達法則、弧長、旋轉曲面與純數學限制最佳化", "73 題題庫重新驗算；181 項 QA 全數通過"], "progressImpact": "章節 ID 與章節數未變，既有閱讀進度保留。"}]},
    "accounting": {"updatedAt": "2026-07-27", "releaseNotes": [{"version": "2026.07.27-2", "date": "2026-07-27", "title": "二次內容複核與錯誤修正", "changes": ["修正損益表名稱與存貨成本公式", "區分定期加權平均與永續移動平均", "補強約當現金、折舊、流動負債與現金流量分類條件", "70 題題庫重新驗算並同步搜尋索引與圖解"], "progressImpact": "章節與題目 ID 未變，既有閱讀進度與錯題紀錄保留。"}]},
    "economics": {"updatedAt": "2026-07-27", "releaseNotes": [{"version": "2026.07.27-2", "date": "2026-07-27", "title": "發布後獨立糾錯複核", "changes": ["修正補貼價格楔與福利效果的敘述", "區分規模經濟、規模不經濟與規模報酬", "補正正消費與正生產外部性的社會曲線關係", "明定儲蓄與稅乘數公式中的 T 為淨稅收", "區分簡單存款乘數與現實廣義貨幣乘數", "補上總合需求與國際收支恆等式的模型條件", "同步修正 6 道題庫詳解與搜尋索引"], "progressImpact": "章節與題目 ID 未變，既有閱讀進度與錯題紀錄保留。"}]},
    "statistics": {"updatedAt": "2026-07-29", "releaseNotes": [{"version": "2026.07.29-2", "date": "2026-07-29", "title": "發布後獨立二次校錯", "changes": ["修正隨機分派、不等組距直方圖、變異係數與柴比雪夫不等式的成立條件", "補正變異數加總的 2Cov(X,Y)、比例區間與檢定標準誤，以及 p 值的極端方向定義", "補強平均數區間、單一比例檢定、非參數方法與含截距簡單迴歸的解讀邊界", "95 題全數複核；44 個計算／公式判斷獨立重算，169 筆搜尋索引重新建立"], "progressImpact": "章節 ID、題目 ID 與題數不變，既有閱讀進度與錯題紀錄保留。"}, {"version": "2026.07.28-1", "date": "2026-07-29", "title": "新增大學入門統計學", "changes": ["新增 19 章正文與 3 份附錄，從資料描述一路到統計推論、ANOVA 與簡單線性迴歸", "新增 95 題題庫，每章 5 題，涵蓋概念、計算、判讀、綜合與常見陷阱", "新增 169 筆搜尋索引與 19 張自製統計圖解", "完成初版兩輪 QA，並修正 HTML 小於符號與不等號公式顯示問題"], "progressImpact": "新增獨立書籍，不改動既有書籍的章節、題目 ID 或閱讀進度。"}]},
    "commercial-law": {"updatedAt": "2026-07-29", "releaseNotes": [{"version": "2026.07.29-2", "date": "2026-07-29", "title": "公司法第 8 條現行法版本回修", "changes": ["最終法規交叉核對發現前版誤採舊法「公開發行股票之公司」限制，立即依現行公司法第 8 條第 3 項回修", "改回現行法的一般規則：公司之非董事符合實質執行董事業務或實質控制並指揮董事等要件時，原則上與董事同負相應責任", "同步修正 ch02-q05、法律 gate 與禁止誤述檢查；其餘發布後二次複核修正全部保留"], "progressImpact": "章節 ID、題目 ID 與題數不變，既有閱讀進度與錯題紀錄保留。"}, {"version": "2026.07.29-1", "date": "2026-07-29", "title": "發布後獨立內容複核與法律精確化", "changes": ["限縮公司法第 8 條實質董事規則至公開發行股票之公司，補正第 194 條繼續持股 1 年門檻", "補入已依證交法發行股票公司董事至少 5 人、公開發行公司董事會原則 7 日前通知與利害關係董事表決排除", "補正閉鎖性公司股東人數上限例外，以及技術與勞務出資的同意、章程與比例條件", "補足短線交易其他股權性質證券、證券商營業處所準用及內線交易非股權公司債路線；90 題全數重新複核"], "progressImpact": "章節 ID、題目 ID 與題數不變，既有閱讀進度與錯題紀錄保留。"}, {"version": "2026.07.28-1", "date": "2026-07-29", "title": "新增商事法重點整理", "changes": ["以公司法與證券交易法為核心，新增 18 章正文與 3 份附錄", "新增 90 題題庫，每章 5 題，涵蓋法條、要件、責任、程序與常見陷阱", "新增 111 筆搜尋索引、18 張自製圖解與法條速查功能", "完成初版兩輪內容與題庫 QA"], "progressImpact": "新增獨立書籍，不改動既有書籍的章節、題目 ID 或閱讀進度。"}]},
}

def read_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write_json(path: Path, obj): path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def finalize(site: Path):
    for book_id, extra in RELEASE_DATA.items():
        path = site / f"books/{book_id}/manifest.json"; obj = read_json(path); obj.update(extra); write_json(path, obj)
    library_path = site / "data/library.json"; library = read_json(library_path); library["version"] = LIBRARY_VERSION; write_json(library_path, library)
    app_path = site / "app.js"; app = app_path.read_text(encoding="utf-8")
    helper = '''  function renderReleaseNotes(manifest) {\n    const notes = Array.isArray(manifest.releaseNotes) ? manifest.releaseNotes : [];\n    if (!notes.length) return '';\n    return `<details class="release-notes"><summary>查看版本與更新內容</summary><div class="release-notes-body">${notes.map(note => `<section class="release-entry"><div class="release-entry-head"><strong>${escapeHtml(note.version || manifest.version || '')}</strong><span>${escapeHtml(note.date || manifest.updatedAt || '')}</span></div><h3>${escapeHtml(note.title || '內容更新')}</h3><ul>${(note.changes || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>${note.progressImpact ? `<p class="progress-impact">閱讀進度：${escapeHtml(note.progressImpact)}</p>` : ''}</section>`).join('')}</div></details>`;\n  }\n\n'''
    if "function renderReleaseNotes(manifest)" not in app:
        app = app.replace("  async function renderLibrary() {", helper + "  async function renderLibrary() {")
        app = app.replace("            <h3>${escapeHtml(book.title)}</h3>\n            <p>${escapeHtml(book.subtitle)}</p>\n            <div class=\"progress-track\">", "            <h3>${escapeHtml(book.title)}</h3>\n            <p>${escapeHtml(book.subtitle)}</p>\n            <div class=\"version-line\">內容版本 ${escapeHtml(manifest.version || '未標示')}</div>\n            <div class=\"progress-track\">", 1)
        app = app.replace("          <h1>${escapeHtml(manifest.title)}</h1>\n          <p class=\"muted\">${escapeHtml(manifest.subtitle)}</p>\n          <div class=\"progress-track\">", "          <h1>${escapeHtml(manifest.title)}</h1>\n          <p class=\"muted\">${escapeHtml(manifest.subtitle)}</p>\n          <div class=\"version-line version-line-strong\">內容版本 ${escapeHtml(manifest.version || '未標示')}・最後更新 ${escapeHtml(manifest.updatedAt || '未標示')}</div>\n          <div class=\"progress-track\">", 1)
        app = app.replace("        </div>\n      </section>\n      <div class=\"section-title\"><h2>搜尋內容</h2></div>", "        </div>\n        ${renderReleaseNotes(manifest)}\n      </section>\n      <div class=\"section-title\"><h2>搜尋內容</h2></div>", 1)
    app_path.write_text(app, encoding="utf-8")
    css_path = site / "styles.css"; css = css_path.read_text(encoding="utf-8")
    if ".release-notes{" not in css:
        css += """\n.version-line{font-size:.86rem;color:var(--muted);margin:.25rem 0 .7rem;font-weight:600}\n.version-line-strong{display:inline-block;padding:.35rem .65rem;border:1px solid var(--line);border-radius:999px;background:var(--surface);color:var(--text)}\n.release-notes{grid-column:1/-1;margin-top:.75rem;border:1px solid var(--line);border-radius:14px;background:var(--surface);overflow:hidden}\n.release-notes summary{cursor:pointer;padding:12px 14px;font-weight:700;color:var(--text)}\n.release-notes-body{border-top:1px solid var(--line);padding:0 14px}.release-entry{padding:14px 0}.release-entry+.release-entry{border-top:1px solid var(--line)}\n.release-entry-head{display:flex;gap:12px;justify-content:space-between;color:var(--muted);font-size:.9rem}.release-entry h3{margin:.45rem 0}.release-entry ul{margin:.4rem 0 .6rem;padding-left:1.25rem}.release-entry li{margin:.3rem 0}\n.progress-impact{margin:.6rem 0 0;padding:.65rem .75rem;border-radius:10px;background:var(--soft);color:var(--text)}\n"""; css_path.write_text(css, encoding="utf-8")
    sw_path = site / "sw.js"; sw = sw_path.read_text(encoding="utf-8"); sw = re.sub(r"const VERSION = 'study-library-[^']+';", f"const VERSION = 'study-library-{LIBRARY_VERSION}';", sw, count=1); sw_path.write_text(sw, encoding="utf-8")

def require_any(compact: str, label: str, *tokens: str):
    normalized = ["".join(token.split()).replace("％", "%") for token in tokens]
    if not any(token in compact for token in normalized): raise AssertionError(f"missing fact: {label}; accepted={tokens}")

def validate(site: Path):
    library = read_json(site / "data/library.json"); assert library["version"] == LIBRARY_VERSION; assert [book["id"] for book in library["books"]] == BOOK_ORDER; assert len(set(BOOK_ORDER)) == len(BOOK_ORDER)
    for book_id, count in EXPECTED_QUESTIONS.items():
        root = site / "books" / book_id; manifest, questions, search = map(read_json, [root/"manifest.json", root/"questions.json", root/"search.json"])
        assert manifest["id"] == book_id and manifest.get("updatedAt") and manifest.get("releaseNotes"); assert questions["count"] == count == len(questions["items"]); assert search["entries"]
        for chapter in manifest["chapters"]:
            path = root / chapter["file"]; assert path.is_file() and path.stat().st_size > 100
    econ = "\n".join((site/"books/economics"/c["file"]).read_text(encoding="utf-8") for c in read_json(site/"books/economics/manifest.json")["chapters"])
    for token in ("與租稅相反的價格楔", "兩者不是同一個定義", "資源稟賦", "正生產外部性", "T 表示淨稅收", "簡單存款乘數", "實質貨幣餘額", "定額淨稅收乘數", "完整國際收支中", "非競爭性且非排他性"): assert token in econ
    for obsolete in ("補貼降低買賣雙方的有效成本", "平均成本不變為規模報酬不變", "資源禀賦", "非敵對且難排他的財"): assert obsolete not in econ
    stats_root = site/"books/statistics"; stats_manifest = read_json(stats_root/"manifest.json"); stats_text = "\n".join((stats_root/c["file"]).read_text(encoding="utf-8") for c in stats_manifest["chapters"])
    for token in ("單一實驗仍可能偶然不平衡", "次數密度或相對次數密度", "CV 雖然沒有單位，也不能因此直接比較性質完全不同的變數", "Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)", "依對立假設方向定義之「同等或更極端」", "SE_{CI}", "SE_0", "兩組分布形狀相近、主要差在位置時"): assert token in stats_text
    law_root = site/"books/commercial-law"; law_manifest = read_json(law_root/"manifest.json"); law_html = "\n".join((law_root/c["file"]).read_text(encoding="utf-8") for c in law_manifest["chapters"]); law_compact = "".join(re.sub(r"<[^>]+>", " ", law_html).split()).replace("％", "%")
    for label, tokens in {"公司法第23條": ("公司法第23條", "公司法第二十三條"), "股東提案300字": ("300字", "三百字"), "代表訴訟六個月": ("6個月", "六個月"), "代表訴訟持股1%": ("1%", "百分之一"), "代表訴訟30日": ("30日", "三十日"), "證交法第43-6條": ("第43-6條", "第43條之6", "第四十三條之六"), "私募35人": ("35人", "三十五人"), "大量持股5%": ("5%", "百分之五"), "內線交易10%": ("10%", "百分之十"), "內線交易18小時": ("18小時", "十八小時"), "公司法第8條現行實質董事主體": ("公司之非董事",), "公司法第8條現行實質執行董事業務": ("實質上執行董事業務",), "公司法第194條一年持有期間": ("繼續1年以上", "繼續一年以上"), "短線交易其他股權性質證券": ("其他具有股權性質之有價證券",), "內線交易非股權公司債": ("非股權性質公司債",), "獨立董事": ("獨立董事",)}.items(): require_any(law_compact, label, *tokens)
    for obsolete in ("私募對象一律不得超過35人", "短線交易只適用上市股票", "公司法第8條第3項只針對公開發行股票之公司", "第8條第3項只針對公開發行股票之公司"): assert obsolete not in law_compact
    macro_root = site/"books/macroeconomics"; macro_manifest = read_json(macro_root/"manifest.json"); macro_questions = read_json(macro_root/"questions.json"); macro_search = read_json(macro_root/"search.json")
    assert macro_manifest["version"] == macro_questions["version"] == "2026.07.29-1"; assert len([x for x in macro_manifest["chapters"] if x["kind"] == "chapter"]) == 20; assert len([x for x in macro_manifest["chapters"] if x["kind"] == "appendix"]) == 3; assert len(macro_search["entries"]) == 143; assert Counter(q["chapterId"] for q in macro_questions["items"]) == {f"ch{i:02d}": 5 for i in range(20)}
    macro_text = "\n".join((macro_root/c["file"]).read_text(encoding="utf-8") for c in macro_manifest["chapters"])
    for token in ("Solow", "黃金律", "Keynesian Cross", "IS–LM", "總合需求", "Phillips", "初級盈餘", "Taylor", "Mundell", "不可能三角", "恆常所得", "Tobin", "預期通膨固定", "\\Delta b\\approx(r-g)b-ps"): assert token in macro_text, token
    for forbidden in ("Ramsey–Cass–Koopmans 的正式推導", "OLG 的正式推導", "DSGE 的完整推導"): assert forbidden not in macro_text
    assert "\f" not in macro_text and "\t" not in macro_text
    for folder, expected in (("economics-svg",20),("statistics-svg",19),("commercial-law-svg",18),("macroeconomics-svg",20)):
        figs = sorted((site/"assets"/folder).glob("*.svg")); assert len(figs) == expected
        for fig in figs:
            svg = fig.read_text(encoding="utf-8"); assert "<title" in svg and "<desc" in svg and "viewBox" in svg
    app, css, sw = (site/"app.js").read_text(encoding="utf-8"), (site/"styles.css").read_text(encoding="utf-8"), (site/"sw.js").read_text(encoding="utf-8")
    assert "查看版本與更新內容" in app and ".release-notes{" in css and f"study-library-{LIBRARY_VERSION}" in sw
    for token in ("./books/macroeconomics/manifest.json", "./books/macroeconomics/chapters/ch19.html", "./assets/macroeconomics-svg/solow.svg"): assert token in sw, token
    print("LIBRARY_VALIDATION_OK books=6 macro_chapters=20 macro_questions=100 macro_search=143 macro_figures=20")

def main():
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site"); finalize(site); validate(site)

if __name__ == "__main__": main()
