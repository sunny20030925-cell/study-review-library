from __future__ import annotations

from copy import deepcopy

VERSION = '2026.07.30-1'
UPDATED_AT = '2026-07-30'


def _chapter(chapters, chapter_id):
    return next(ch for ch in chapters if ch['id'] == chapter_id)


def _question(questions, question_id):
    return next(q for q in questions if q['id'] == question_id)


def build_v2(chapters, questions):
    """Apply the post-publication econometrics precision corrections.

    IDs and question counts are intentionally preserved so tablet reading progress and
    wrong-answer history remain compatible with the published v1 book.
    """
    chapters = deepcopy(chapters)
    questions = deepcopy(questions)

    # ch13 Panel data: FE/FD remove time-invariant alpha_i, but this alone does not
    # identify beta. State the standard static-panel strict-exogeneity condition.
    ch = _chapter(chapters, 'ch13')
    ch['intuition'].append(
        '但把 alpha_i 消掉不等於 X 自動外生。在標準靜態 FE／FD 模型裡，常用的充分條件是 strict exogeneity：給定個體效果與該個體整段 X 歷史後，每一期 idiosyncratic error 的條件平均為 0。若當期衝擊會回頭影響未來 X、存在 time-varying confounder，或模型含落後依變數，基本 FE／FD 的識別與推論就需要重新檢查。'
    )
    ch['definitions'].append(
        ('Strict exogeneity（嚴格外生性）', '標準靜態 panel 模型常用的條件：給定個體效果與整段解釋變數歷史後，每一期 idiosyncratic error 的條件平均為 0；它比「FE 已消掉 alpha_i」更進一步。')
    )
    ch['formulas'].append(
        (r'E(u_{it}\mid x_{i1},\ldots,x_{iT},\alpha_i)=0', '標準靜態 FE／FD 常用的 strict-exogeneity 表示；若誤差會影響未來 X 或含動態依變數，需改用相應的弱外生／動態 panel 方法。')
    )
    ch['traps'].append('以為做了 FE／FD 就不必再檢查 idiosyncratic error 與時間變動 X 的外生性。')
    ch['exam'].append('若題目問 FE 是否能作因果解讀，除了 alpha_i 被消除，還要補一句「time-varying X 對 idiosyncratic error 需要合適的外生性條件」。')
    ch['checks'].append('FE 消掉 alpha_i 後，是否就不再需要任何關於 u_it 與 X 的外生性條件？')

    q = _question(questions, 'ch13-q04')
    q['question'] = '個體 FE 已經消掉時間不變的 alpha_i，是否因此就自動足以識別 beta 的因果效果？'
    q['answer'] = '不能。仍需要 X 與 idiosyncratic error 之間合適的外生性條件；標準靜態 FE 常使用 strict exogeneity。'
    q['explanation'] = 'FE 只處理時間不變的 alpha_i。若 time-varying confounder 存在，或當期衝擊會影響未來 X，基本 FE 仍可能失去因果識別；常見靜態模型條件寫成 E(u_it|x_i1,...,x_iT,alpha_i)=0。'

    # ch15 Experiments: random assignment gives internal validity for the experimental
    # units; population generalization is a separate sampling/external-validity step.
    ch = _chapter(chapters, 'ch15')
    ch['intuition'][1] = (
        '隨機分派讓 treatment assignment 在設計上與實驗單位的潛在結果獨立，因此 treatment 與 control 的差均值可在隨機化設計下識別「這批實驗單位」的平均處置效果（SATE）。它不要求樣本內每一個協變數都恰好完全平衡；但若要把結果直接推廣成更大母體的 PATE，還需要代表性抽樣、外部效度或其他可運輸性假設，不能只靠 random assignment。'
    )
    ch['definitions'].extend([
        ('SATE（Sample Average Treatment Effect）', '實驗樣本／有限個體集合中的平均處置效果；隨機分派直接提供的是對這批實驗單位的內部因果識別。'),
        ('PATE（Population Average Treatment Effect）', '更大目標母體的平均處置效果；從實驗樣本推廣到 PATE 還需要抽樣代表性或其他外部效度／transportability 條件。'),
    ])
    ch['formulas'].append(
        (r'SATE=\frac{1}{n}\sum_{i=1}^{n}[Y_i(1)-Y_i(0)]', '有限實驗樣本的平均處置效果；是否能外推成目標母體 PATE 是另一個問題。')
    )
    ch['example'][1] = (
        '差均值為 75-70=5 分；在設計與執行有效的隨機實驗中，這保留了 assignment 的因果識別。完整遵從時，可把它視為這批實驗單位平均處置效果（SATE）的直接估計；若要宣稱更大母體 PATE 也是 5，還需說明樣本如何代表該母體或提供其他外推依據。'
    )
    ch['traps'].append('把 random assignment 和 random sampling 混為一談：前者主要建立內部因果識別，後者／代表性條件才關係到能否直接外推母體。')
    ch['exam'].append('看到「隨機分派」先回答內部效度；題目若再問能否推廣到全國／母體，另外檢查 sampling 與 external validity。')
    ch['checks'].append('只有 random assignment、沒有代表性抽樣資訊時，結果是否能無條件外推成更大母體 PATE？')

    q = _question(questions, 'ch15-q02')
    q['question'] = '只有 random assignment、但沒有代表性抽樣或其他外推資訊時，能否直接把實驗差均值解讀成更大目標母體的 PATE？'
    q['answer'] = '不能無條件這樣外推。'
    q['explanation'] = 'Random assignment 主要確保實驗單位內部的因果可比性並支持 SATE；從實驗樣本推到更大母體 PATE，還需要代表性／隨機抽樣、外部效度或其他 transportability 假設。'

    q = _question(questions, 'ch15-q03')
    q['explanation'] = 'E[Y(1)-Y(0)] 常用來表示目標母體的平均處置效果；若只固定在實驗樣本，對應的是 sample／finite-sample average effect。從 SATE 推到 PATE 需要另外的外部效度條件。'

    return chapters, questions
