from __future__ import annotations

from econometrics_v2_corrections import build_v2

VERSION = '2026.07.30-2'
UPDATED_AT = '2026-07-30'


def _chapter(chapters, chapter_id):
    return next(ch for ch in chapters if ch['id'] == chapter_id)


def _question(questions, question_id):
    return next(q for q in questions if q['id'] == question_id)


def build_v3(chapters, questions):
    """Apply the second independent post-publication econometrics content audit.

    The v3 layer starts from the already-corrected v2 content. Chapter IDs, question
    IDs and question counts are intentionally preserved for tablet progress/history
    compatibility.
    """
    chapters, questions = build_v2(chapters, questions)

    ch = _chapter(chapters, 'ch14')
    ch['intuition'].append(
        '若 treatment effect 因人而異，二元工具變數的 Wald／2SLS 比率不能無條件叫作整體 ATE 或 ATT。在標準二元 IV 架構下，若工具外生、滿足 exclusion、確實改變 treatment，並採用 monotonicity（沒有 defiers）等條件，最典型的因果 estimand 是被工具推動而改變 treatment 狀態之 compliers 的 Local Average Treatment Effect（LATE／CACE）。'
    )
    ch['definitions'].extend([
        ('Complier（遵從型）', '在二元工具 Z 下，Z=1 時接受 treatment、Z=0 時不接受 treatment 的單位；以潛在 treatment 表示為 D(1)=1、D(0)=0。'),
        ('LATE / CACE', 'Local Average Treatment Effect／Complier Average Causal Effect；標準二元 IV 假設下，工具所影響的 compliers 之平均處置效果。'),
        ('Monotonicity（單調性）', '常見二元 IV 條件 D(1)>=D(0)：工具不會讓某些人朝與其他人相反方向改變 treatment；亦即排除 defiers。'),
    ])
    ch['formulas'].append(
        (r'LATE=E[Y(1)-Y(0)\mid D(1)>D(0)]', '在二元 treatment／instrument 且工具外生、relevance、exclusion、monotonicity 等標準條件下，Wald 比率可解讀為 compliers 的平均因果效果，而非自動等於全母體 ATE／ATT。')
    )
    ch['traps'].append('在 treatment effects 異質時，把二元 IV／Wald 估計量不加條件地稱為整體 ATE、ATT 或「所有實際接受 treatment 者的效果」。')
    ch['exam'].append('若題目出現二元 IV、noncompliance 與異質 treatment effects，除了 relevance／exclusion，再檢查 monotonicity，並把典型因果範圍寫成 compliers 的 LATE／CACE。')
    ch['checks'].append('標準二元 IV 在效果異質且滿足 LATE 條件時，Wald ratio 最典型識別哪一群人的平均效果？')

    q = _question(questions, 'ch14-q05')
    q['question'] = '在二元 IV、treatment effects 異質，且 relevance、工具外生／exclusion 與 monotonicity 等標準條件成立時，Wald ratio 最典型識別哪個效果？'
    q['answer'] = 'Compliers 的 Local Average Treatment Effect（LATE／CACE）。'
    q['explanation'] = '工具只提供由 Z 所誘發的 treatment 變動。加入 monotonicity（無 defiers）等標準 LATE 條件後，Wald ratio 對應被工具推動而改變 treatment 狀態之 compliers 的平均效果；除非另有更強條件，不能直接改稱全母體 ATE 或所有 treated 的 ATT。'

    ch = _chapter(chapters, 'ch15')
    ch['example'][2] = (
        '若 treatment 組有人未參加、control 組有人自行參加，把大家依「實際參加」重分組就不再保證隨機。此時仍先報 ITT；若以原始 assignment 作為實際 treatment 的工具，在 relevance、exclusion、monotonicity 等相應條件下，可進一步識別 compliers 的 LATE／CACE。這不是把所有實際接受 treatment 者直接當成一個仍然隨機的群組，也不自動等於 ATT／TOT。'
    )
    ch['definitions'].append(
        ('LATE under noncompliance', '隨機 assignment 作 IV 且相應工具變數假設成立時，實際 treatment 的典型局部因果 estimand 是會因 assignment 改變 treatment 狀態之 compliers 的平均效果。')
    )
    ch['traps'].append('有 noncompliance 時，把 assignment-as-IV 的 estimand 說成「所有實際接受 treatment 者的效果」；標準異質效果架構通常是 complier LATE／CACE。')
    ch['exam'].append('Noncompliance 題要分三件事：assignment 的 ITT、actual treatment 的非隨機比較、以及在額外 IV 假設下可識別的 complier LATE／CACE。')

    q = _question(questions, 'ch15-q04')
    q['explanation'] = 'ITT 依原始隨機 assignment 分組，保留隨機化提供的可比性；不能把 actual treatment takers 直接重分組後仍宣稱隨機。若進一步把 assignment 當 IV，還需 relevance、exclusion、monotonicity 等條件，典型識別的是 compliers 的 LATE／CACE。'

    ch = _chapter(chapters, 'ch16')
    ch['intuition'].append(
        '另一個常被省略的條件是 no anticipation：被標成「處置前」的期間不應已因預期政策而改變結果。若企業或個人在政策正式生效前就提前調整，這些 pre-period observations 已受 treatment timing 影響，標準 pre／post DiD 與 event-study 基準期就要重新界定或明確建模 anticipation window。'
    )
    ch['definitions'].append(
        ('No anticipation（無預期／無提前反應）', '在標準 DiD 設定中，處置正式發生前的潛在結果不因未來 treatment 而先行改變；若有已知提前反應，需調整 treatment timing 或明確處理 anticipation period。')
    )
    ch['traps'].append('只寫 parallel trends，卻把已受政策預期影響的期間仍當成乾淨的 pre-treatment 基準。')
    ch['exam'].append('DiD 因果題除 parallel trends 外，再問政策是否可能提前被預期；若 pre-period 已受影響，標準前後切分需要修正。')
    ch['checks'].append('若政策宣布後、正式生效前企業已提前調整，這段期間還能無條件當作乾淨 pre-treatment 嗎？')

    ch = _chapter(chapters, 'ch17')
    ch['intuition'].append(
        'Fuzzy RDD 的 treatment probability 只在 cutoff 跳動，因此本質上可把「跨過 cutoff」視為局部工具變數。若 treatment effects 異質，除了 cutoff 附近的連續性與 first-stage jump，還需要相應 exclusion／monotonicity 等條件；此時局部 Wald ratio 的標準解讀是 cutoff 處 compliers 的 LATE，而不是整體 ATE。'
    )
    ch['definitions'].append(
        ('Local complier in fuzzy RDD', '在 cutoff 附近，因 crossing／eligibility 狀態改變而改變實際 treatment 的單位；fuzzy RDD 的標準局部因果效果針對這群 compliers。')
    )
    for i, (formula, note) in enumerate(ch['formulas']):
        if r'\tau_{FRD}' in formula:
            ch['formulas'][i] = (
                formula,
                'Fuzzy RDD 的局部 Wald ratio；在 cutoff 連續性、first-stage jump、exclusion、monotonicity 等標準條件下，因果解讀是 cutoff 處 local compliers 的 LATE，而非無條件的全體 ATE。',
            )
            break
    else:
        raise AssertionError('fuzzy RDD formula not found')
    ch['traps'].append('看到 fuzzy RDD 的 outcome jump／treatment jump 比率，就直接稱為所有人的 ATE；異質效果下其標準因果範圍是 cutoff 處 local compliers。')
    ch['exam'].append('Fuzzy RDD 題除了算兩個 jump 的比率，還要寫清楚「cutoff 附近、compliers、需要相應 IV／連續性假設」。')

    q = _question(questions, 'ch17-q05')
    q['explanation'] = '局部 Wald ratio 把 cutoff 對 outcome 的 reduced-form 跳躍除以 cutoff 對 treatment 的 first-stage 跳躍；在 continuity、exclusion、monotonicity 等標準條件下，異質 treatment effects 時它識別的是 cutoff 處 local compliers 的 LATE，而不是整體 ATE。'

    ch = _chapter(chapters, 'ch18')
    ch['example'][1] = (
        '若一個複雜模型 training RMSE=0.5、validation RMSE=3，而簡單模型 training RMSE=1.2、validation RMSE=1.8，應在尚未打開 final test set 前依 validation／cross-validation 結果選擇後者。模型與超參數固定後，才用保留的 test set 做一次最後樣本外評估。'
    )
    ch['example'].append(
        '若反覆比較多個模型的 test RMSE，再挑 test 表現最好的那一個，test 已參與 model selection；之後同一 test RMSE 會對真正泛化能力過度樂觀。此時需要新的未使用資料，或重新建立嚴格的 validation／test 流程。'
    )
    ch['checks'].append('若用 test RMSE 在多個候選模型中挑勝者，之後還能把同一 test 當完全未碰過的最終評估嗎？')

    q = _question(questions, 'ch18-q03')
    q['question'] = '一模型 training RMSE=0.5、validation RMSE=3；另一模型 training RMSE=1.2、validation RMSE=1.8。在尚未打開 final test set 前，哪個較適合被選為候選最終模型？'
    q['answer'] = '第二個模型。'
    q['explanation'] = '模型選擇應依 validation／cross-validation 的樣本外近似表現；1.8 小於 3，所以先選第二個模型。選模與調參完成後才使用 untouched test set 做最後評估，不能用 test 一邊選模型一邊又宣稱它是純 final holdout。'

    return chapters, questions


def appendix_b_v3(base_html: str) -> str:
    old_iv = '<h2 id="內生性與IV">內生性與 IV</h2>\n<ol><li>先找 OVB、反向因果、同時性或測量誤差來源。</li><li>有 instrument 時分 relevance 與 exclusion／exogeneity。</li><li>二元 IV 可先算 reduced form／first stage 的 Wald ratio。</li><li>檢查 weak instrument；強 first stage 仍不等於 instrument 外生。</li></ol>'
    new_iv = '<h2 id="內生性與IV">內生性與 IV</h2>\n<ol><li>先找 OVB、反向因果、同時性或測量誤差來源。</li><li>有 instrument 時分 relevance 與 exclusion／exogeneity。</li><li>二元 IV 可先算 reduced form／first stage 的 Wald ratio。</li><li>若 treatment effects 異質，再檢查 monotonicity／complier 架構；標準因果解讀通常是 LATE／CACE，而非自動等於 ATE／ATT。</li><li>檢查 weak instrument；強 first stage 仍不等於 instrument 外生。</li></ol>'
    if old_iv not in base_html:
        raise AssertionError('appendix B IV block drift')
    out = base_html.replace(old_iv, new_iv, 1)

    old_causal = '<h2 id="因果設計">實驗、DiD 與 RDD</h2>\n<ol><li>實驗：assignment 是否隨機？有 noncompliance 先分 ITT 與 actual treatment。</li><li>DiD：先算兩組 post-pre，再相減；核心寫 parallel trends。</li><li>RDD：找 running variable、cutoff 與局部跳躍；答案寫 local effect。</li></ol>'
    new_causal = '<h2 id="因果設計">實驗、DiD 與 RDD</h2>\n<ol><li>實驗：assignment 是否隨機？有 noncompliance 先報 ITT；若以 assignment 作 IV，需額外 IV 假設，典型 estimand 是 compliers 的 LATE／CACE。</li><li>DiD：先算兩組 post-pre，再相減；核心寫 parallel trends，並檢查 no anticipation／提前反應。</li><li>RDD：找 running variable、cutoff 與局部跳躍；sharp RDD 寫 cutoff local effect，fuzzy RDD 在相應條件下寫 local complier LATE。</li></ol>'
    if old_causal not in out:
        raise AssertionError('appendix B causal block drift')
    out = out.replace(old_causal, new_causal, 1)

    marker = '<h2 id="最後檢查">最後檢查</h2>'
    prediction = '<h2 id="預測與樣本外評估">預測與樣本外評估</h2>\n<ol><li>Training 用來估模型。</li><li>Validation／cross-validation 用來比較候選模型與調參。</li><li>Final test set 保留到選模完成後再做最後評估；不能一邊用 test 選模型，一邊再把同一 test 當未碰過的 holdout。</li></ol>\n'
    if marker not in out:
        raise AssertionError('appendix B final-check marker drift')
    return out.replace(marker, prediction + marker, 1)


def appendix_c_v3(base_html: str) -> str:
    rows = (
        '<tr><td>Sample Average Treatment Effect (SATE)</td><td>樣本平均處置效果</td></tr>'
        '<tr><td>Population Average Treatment Effect (PATE)</td><td>母體平均處置效果</td></tr>'
        '<tr><td>Complier</td><td>遵從型／受工具影響而改變處置狀態者</td></tr>'
        '<tr><td>Local Average Treatment Effect (LATE / CACE)</td><td>局部平均處置效果／遵從型平均因果效果</td></tr>'
        '<tr><td>Monotonicity</td><td>單調性／無 defiers 條件</td></tr>'
        '<tr><td>No Anticipation</td><td>無預期／無提前反應</td></tr>'
        '<tr><td>Validation Set</td><td>驗證集／模型選擇與調參用資料</td></tr>'
    )
    marker = '</tbody></table>'
    idx = base_html.rfind(marker)
    if idx < 0:
        raise AssertionError('appendix C glossary table drift')
    return base_html[:idx] + rows + base_html[idx:]
