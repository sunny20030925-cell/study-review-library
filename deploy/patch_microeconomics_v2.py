#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK = "microeconomics"
OLD_VERSION = "2026.07.29-1"
NEW_VERSION = "2026.07.29-2"


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, int]:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1), 1


def patch_html(path: Path, replacements: list[tuple[str, str, str]]) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for old, new, label in replacements:
        text, n = replace_once(text, old, new, f"{path.name}:{label}")
        changed += n
    path.write_text(text, encoding="utf-8")
    return changed


def main(site_root: str) -> None:
    site = Path(site_root)
    book = site / "books" / BOOK
    corrections = 0

    corrections += patch_html(book / "chapters/ch00.html", [(
        "可微的一階條件通常只是必要條件；若目標函數在可行集合上是嚴格凹函數，滿足一階條件的內點解通常就是唯一全域最大值。",
        "可微的一階條件通常只是必要條件；若可行集合為凸集、目標函數在其上嚴格凹，且候選解滿足完整的一階／KKT 條件，則該解是唯一全域最大值。",
        "strict-concavity-sufficiency",
    )])
    corrections += patch_html(book / "chapters/ch02.html", [(
        "若偏好局部非飽和，最適點通常用完預算，因此滿足 \\(p_xx+p_yy=m\\)。",
        "若偏好局部非飽和且最適解存在，任何最適點都會用盡預算，因此滿足 \\(p_xx+p_yy=m\\)。",
        "budget-exhaustion",
    )])
    corrections += patch_html(book / "chapters/ch05.html", [(
        "可微情況下，普通需求的價格反應可寫成：\\[\\frac{\\partial x_i}{\\partial p_j}=\\frac{\\partial h_i}{\\partial p_j}-x_j\\frac{\\partial x_i}{\\partial m}\\] 第一項是補償替代效果；第二項是由購買力變化造成的所得效果。",
        "可微情況下，在補償效用取 \\(\\bar u=v(p,m)\\) 時，普通需求的價格反應可寫成：\\[\\frac{\\partial x_i}{\\partial p_j}=\\left.\\frac{\\partial h_i(p,\\bar u)}{\\partial p_j}\\right|_{\\bar u=v(p,m)}-x_j\\frac{\\partial x_i}{\\partial m}\\] 第一項是在原效用水準評估的 Hicksian 替代效果；第二項是由購買力變化造成的所得效果。",
        "slutsky-evaluation-point",
    )])
    corrections += patch_html(book / "chapters/ch06.html", [(
        "對普通商品，Marshallian demand 下需求曲線與價格之間的面積是常用的消費者剩餘變化。若所得效果很小，消費者剩餘變化會接近 EV 與 CV；所得效果較大時，三者不必相同。",
        "對單一商品價格變動，沿 Marshallian demand 在舊、新價格之間積分，是常用的消費者剩餘變化。若偏好對該商品近似準線性、所得效果為零，這個量測與 EV、CV 一致；所得效果很小時只是近似，所得效果較大時三者不必相同。",
        "consumer-surplus-condition",
    )])
    corrections += patch_html(book / "chapters/ch08.html", [(
        "在 von Neumann–Morgenstern 公理下，風險偏好可用這種期望形式表示。",
        "在 von Neumann–Morgenstern 公理下，風險偏好可用這種期望形式表示。此處的 vNM 效用與確定性消費選擇中的一般序數效用不同：只有正仿射轉換 \\(a u+b,\\ a>0\\) 保留同一個期望效用偏好；任意嚴格遞增轉換可能改變風險態度。",
        "vnm-affine-invariance",
    )])
    corrections += patch_html(book / "chapters/ch12.html", [(
        "在沒有外部性、資訊問題、市場力量等扭曲時，競爭均衡的交易量使願付價格高於邊際成本的交易被完成，而低於邊際成本的交易不發生，因此最大化消費者剩餘加生產者剩餘。",
        "在標準單一市場、準線性偏好或可忽略所得效果，且供給曲線反映邊際成本時，競爭均衡的交易量最大化消費者剩餘加生產者剩餘。更一般的經濟中，第一福利定理給的是 Pareto 效率；不能在沒有額外條件時把任意需求曲線面積直接當成精確福利。",
        "partial-equilibrium-welfare-condition",
    )])
    corrections += patch_html(book / "chapters/ch14.html", [(
        "報酬只需反映偏好排序；數值本身未必代表金額。",
        "若只分析純策略最佳回應與純策略 Nash 均衡，報酬的排序已足夠，數值也不必代表金額；但一旦比較混合策略的期望報酬，只有正仿射轉換會保留同一賽局，不能任意做嚴格遞增轉換。",
        "game-payoff-cardinality",
    )])
    corrections += patch_html(book / "chapters/ch16.html", [(
        "當工資下降，若其他條件不變，企業願意雇用更多勞動，因此 MRP 曲線可作為個別企業的勞動需求基礎。產品價格、技術或其他互補投入改變會移動勞動需求。",
        "在產品價格與其他投入固定、企業是工資接受者的簡化情況下，MRP 曲線可直接作為個別企業的勞動需求曲線。若其他投入會一併調整，仍以 \\(MRP_L=w\\) 為最適條件，但必須聯立其他投入選擇後才得到真正的勞動需求；產品價格、技術或其他投入價格改變都可能移動它。",
        "labor-demand-conditions",
    )])
    corrections += patch_html(book / "chapters/ch17.html", [(
        "若每位消費者都滿足預算限制，總超額需求向量 \\(z(p)\\) 滿足 \\[p\\cdot z(p)=0\\]。",
        "若每位消費者的最適選擇都用盡預算，使個別預算式以等號成立，則總超額需求向量 \\(z(p)\\) 滿足 \\[p\\cdot z(p)=0\\]。只有 \\(p\\cdot x_i\\le p\\cdot \\omega_i\\) 而未保證用盡預算時，不能直接推出等號。",
        "walras-budget-exhaustion",
    )])
    corrections += patch_html(book / "chapters/ch18.html", [(
        "因為同一單位可同時被多人享用，效率條件不是單一人的 MRS=MRT，而是 Samuelson condition：\\[\\sum_i MRS_i=MRT\\] 自願付費下容易出現搭便車，使市場供給不足。",
        "因為同一單位可同時被多人享用，在可微且內點的效率配置中，條件不是單一人的 MRS=MRT，而是 Samuelson condition：\\[\\sum_i MRS_i=MRT\\]；若最適點在角點，應改用相應不等式條件。自願付費下容易出現搭便車，使市場供給不足。",
        "samuelson-interior-condition",
    )])
    corrections += patch_html(book / "chapters/appendix-a.html", [(
        "效用函數本身不必凹，只要偏好凸，通常可用準凹效用表示。成本最小化常利用凸生產集合；利潤最大化與效用最大化則常利用凹目標確保 FOC 足夠。",
        "效用函數本身不必凹；凸偏好通常可用準凹效用表示，而凹性只是更強的充分條件。成本最小化常利用凸的投入需求集合；利潤最大化則常利用凹性，配合凸可行集合使一階／KKT 條件成為充分條件。",
        "quasiconcavity-and-convexity",
    )])
    corrections += patch_html(book / "chapters/appendix-b.html", [(
        "預算：\\(p\\cdot x=m\\)。內點最適：\\(MRS_{ij}=p_i/p_j\\)。Roy：\\(x_i=-(v_{p_i}/v_m)\\)。Shephard：\\(h_i=e_{p_i}\\)。Slutsky：\\(x_{i,p_j}=h_{i,p_j}-x_jx_{i,m}\\)。",
        "預算（局部非飽和且最適解存在）：\\(p\\cdot x=m\\)。內點最適：\\(MRS_{ij}=p_i/p_j\\)。Roy：\\(x_i=-(v_{p_i}/v_m)\\)。Shephard：\\(h_i=e_{p_i}\\)。Slutsky：\\(x_{i,p_j}=h_{i,p_j}|_{\\bar u=v(p,m)}-x_jx_{i,m}\\)。",
        "formula-sheet-conditions",
    )])

    qpath = book / "questions.json"
    qj = json.loads(qpath.read_text(encoding="utf-8"))
    if qj.get("version") != OLD_VERSION:
        raise AssertionError(f"unexpected question version {qj.get('version')}")
    items = {q["id"]: q for q in qj["items"]}

    q = items["ch05-q04"]
    if q["explanation"] != "Hicksian demand 固定效用，隔離相對價格效果。":
        raise AssertionError("ch05-q04 explanation drift")
    q["explanation"] = "Hicksian demand 固定效用；在 Slutsky 方程中，這個偏導要在原最適效用 \\(\\bar u=v(p,m)\\) 處評估。"
    corrections += 1

    q = items["ch06-q05"]
    if q["explanation"] != "所得效果大時三種福利量測可有明顯差異。":
        raise AssertionError("ch06-q05 explanation drift")
    q["explanation"] = "準線性偏好或所得效果為零時三者可一致；一般情況下所得效果愈大，Marshallian 消費者剩餘與 EV、CV 的差異可能愈明顯。"
    corrections += 1

    q = items["ch14-q03"]
    if q["question"] != "某策略不論對手怎麼做都給較高報酬，稱什麼？":
        raise AssertionError("ch14-q03 prompt drift")
    q["question"] = "若某策略不論對手怎麼做，都嚴格優於自己所有其他策略，稱什麼？"
    q["explanation"] = "它在每一種對手策略下，都嚴格優於該玩家的每一個其他可選策略。"
    corrections += 1

    q = items["ch17-q03"]
    if q["question"] != "Walras 法則寫成什麼？":
        raise AssertionError("ch17-q03 prompt drift")
    q["question"] = "在每位消費者都用盡預算的標準交換經濟中，Walras 法則寫成什麼？"
    q["explanation"] = "個別預算等式加總後，價格加權的總超額需求價值為 0；只有預算不等式不足以保證等號。"
    corrections += 1

    qj["version"] = NEW_VERSION
    qpath.write_text(json.dumps(qj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    spath = book / "search.json"
    sj = json.loads(spath.read_text(encoding="utf-8"))
    search_repls = [
        ("若目標函數在可行集合上是嚴格凹函數，滿足一階條件的內點解通常就是唯一全域最大值。", "若可行集合為凸集、目標函數在其上嚴格凹，且候選解滿足完整的一階／KKT 條件，則該解是唯一全域最大值。"),
        ("若偏好局部非飽和，最適點通常用完預算", "若偏好局部非飽和且最適解存在，任何最適點都會用盡預算"),
        ("可微情況下，普通需求的價格反應可寫成：", "可微情況下，在補償效用取 \\(\\bar u=v(p,m)\\) 時，普通需求的價格反應可寫成："),
        ("對普通商品，Marshallian demand 下需求曲線與價格之間的面積是常用的消費者剩餘變化。若所得效果很小，消費者剩餘變化會接近 EV 與 CV；所得效果較大時，三者不必相同。", "對單一商品價格變動，沿 Marshallian demand 在舊、新價格之間積分，是常用的消費者剩餘變化。若偏好對該商品近似準線性、所得效果為零，這個量測與 EV、CV 一致；所得效果很小時只是近似，所得效果較大時三者不必相同。"),
        ("在 von Neumann–Morgenstern 公理下，風險偏好可用這種期望形式表示。", "在 von Neumann–Morgenstern 公理下，風險偏好可用這種期望形式表示。此處的 vNM 效用只有正仿射轉換保留同一個期望效用偏好。"),
        ("在沒有外部性、資訊問題、市場力量等扭曲時，競爭均衡的交易量使願付價格高於邊際成本的交易被完成，而低於邊際成本的交易不發生，因此最大化消費者剩餘加生產者剩餘。", "在標準單一市場、準線性偏好或可忽略所得效果，且供給曲線反映邊際成本時，競爭均衡的交易量最大化消費者剩餘加生產者剩餘；更一般的結論是 Pareto 效率。"),
        ("報酬只需反映偏好排序；數值本身未必代表金額。", "純策略分析只需報酬排序；混合策略的期望報酬則只容許正仿射轉換。數值本身未必代表金額。"),
        ("當工資下降，若其他條件不變，企業願意雇用更多勞動，因此 MRP 曲線可作為個別企業的勞動需求基礎。", "在產品價格與其他投入固定、企業是工資接受者的簡化情況下，MRP 曲線可直接作為個別企業的勞動需求曲線。"),
        ("若每位消費者都滿足預算限制，總超額需求向量", "若每位消費者的最適選擇都用盡預算，使個別預算式以等號成立，則總超額需求向量"),
        ("效率條件不是單一人的 MRS=MRT，而是 Samuelson condition", "在可微且內點的效率配置中，條件不是單一人的 MRS=MRT，而是 Samuelson condition"),
    ]
    for old, new in search_repls:
        found = 0
        for entry in sj["entries"]:
            if old in entry["text"]:
                entry["text"] = entry["text"].replace(old, new, 1)
                found += 1
        if found != 1:
            raise AssertionError(f"search sync expected 1 for {old[:40]!r}, got {found}")
    spath.write_text(json.dumps(sj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    mpath = book / "manifest.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    if manifest.get("version") != OLD_VERSION:
        raise AssertionError(f"unexpected manifest version {manifest.get('version')}")
    manifest["version"] = NEW_VERSION
    manifest["updatedAt"] = "2026-07-29"
    manifest.setdefault("releaseNotes", []).insert(0, {
        "version": NEW_VERSION,
        "date": "2026-07-29",
        "title": "發布後獨立二次複核與條件精確化",
        "changes": [
            "補正 Walras 法則必須由個別預算等式／用盡預算推出，不能只寫預算不等式",
            "明定 Slutsky 方程中的 Hicksian 價格偏導須在原最適效用水準評估",
            "區分確定性序數效用與 vNM 期望效用的轉換規則，修正賽局混合策略報酬的基數條件",
            "補強消費者剩餘、競爭市場總剩餘、勞動需求與公共財效率條件的適用邊界",
            "100 題全部重查；4 題題幹或詳解同步精確化，章節與題目 ID、題數不變",
        ],
        "progressImpact": "章節 ID、題目 ID 與題數不變，既有閱讀進度與錯題紀錄保留。",
    })
    mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if corrections != 16:
        raise AssertionError(f"unexpected correction count {corrections}")
    print(f"MICRO_V2_PATCH_OK corrections={corrections} question_adjustments=4 version={NEW_VERSION}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
