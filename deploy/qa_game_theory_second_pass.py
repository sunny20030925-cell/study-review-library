#!/usr/bin/env python3
from __future__ import annotations

import math
from collections import Counter

from game_theory_content_a import CHAPTERS_A
from game_theory_content_b import CHAPTERS_B
from game_theory_questions_a import QUESTIONS_A
from game_theory_questions_b import QUESTIONS_B

CHAPTERS = CHAPTERS_A + CHAPTERS_B
QUESTIONS = QUESTIONS_A + QUESTIONS_B
checks = 0
quantitative = 0
conceptual = 0


def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def qcheck(qmap, qid, expected):
    global quantitative
    quantitative += 1
    ck(qmap[qid]['answer'] == expected, f'{qid}: {qmap[qid]["answer"]!r} != {expected!r}')


def ccheck(qmap, qid, expected):
    global conceptual
    conceptual += 1
    ck(qmap[qid]['answer'] == expected, f'{qid}: {qmap[qid]["answer"]!r} != {expected!r}')


def main():
    ck(len(CHAPTERS) == 20, '20 chapters')
    ck([c['id'] for c in CHAPTERS] == [f'ch{i:02d}' for i in range(20)], 'chapter order')
    ck(len({c['title'] for c in CHAPTERS}) == 20, 'unique titles')
    ck(len(QUESTIONS) == 100, '100 questions')
    ck(len({q['id'] for q in QUESTIONS}) == 100, 'unique question ids')
    ck(Counter(q['chapterId'] for q in QUESTIONS) == {f'ch{i:02d}':5 for i in range(20)}, 'five per chapter')
    ck(len({q['question'] for q in QUESTIONS}) == 100, 'unique question text')
    short_explanations = [(q['id'], q['explanation']) for q in QUESTIONS if len(q['explanation']) < 18]
    ck(not short_explanations, f'nontrivial explanations: {short_explanations}')

    for ch in CHAPTERS:
        for key in ('problem','intuition','definitions','formulas','example','traps','exam','checks','figure'):
            ck(bool(ch[key]), f'{ch["id"]} {key}')
        ck(len(ch['intuition']) >= 2, f'{ch["id"]} intuition depth')
        ck(len(ch['definitions']) >= 4, f'{ch["id"]} definitions depth')
        ck(len(ch['example']) >= 3, f'{ch["id"]} worked example depth')
        ck(len(ch['traps']) >= 3 and len(ch['exam']) >= 3, f'{ch["id"]} exam/trap depth')
        ck(len(ch['checks']) >= 2, f'{ch["id"]} checks depth')

    qmap = {q['id']: q for q in QUESTIONS}

    q = 2 / 5
    p = 3 / 5
    ck(math.isclose(q, 0.4) and math.isclose(p, 0.6), 'mixed equilibrium arithmetic')
    qcheck(qmap, 'ch04-q03', f'q={q:.1f}。')
    qcheck(qmap, 'ch04-q04', f'p={p:.1f}。')

    matrix = ((2, -1), (-2, 1))
    row_mins = tuple(min(r) for r in matrix)
    pure_maximin = max(row_mins)
    ck(row_mins == (-1, -2) and pure_maximin == -1, 'zero-sum pure security values')
    qcheck(qmap, 'ch05-q02', '-1 與 -2。')
    qcheck(qmap, 'ch05-q03', f'{pure_maximin}。')
    p_zero = 3 / 6
    q_zero = 2 / 6
    value = 4*p_zero - 2
    ck(math.isclose(p_zero, .5) and math.isclose(q_zero, 1/3) and math.isclose(value, 0), 'zero-sum mixed solution')

    a, c, b = 100, 10, 1
    cournot_q = (a-c)/(3*b)
    price = a - b*(2*cournot_q)
    profit = (price-c)*cournot_q
    ck((cournot_q, price, profit) == (30, 40, 900), 'Cournot reconstruction')
    qcheck(qmap, 'ch06-q03', '30。')
    qcheck(qmap, 'ch06-q04', '總產量60，價格40。')

    d1 = d2 = .9
    proposer_share = (1-d2)/(1-d1*d2)
    ck(math.isclose(proposer_share, 10/19), 'Rubinstein share')
    qcheck(qmap, 'ch09-q02', f'約{proposer_share:.4f}。')
    qcheck(qmap, 'ch09-q03', f'約 NT${100*proposer_share:.2f}。')

    R, T, P = 3, 5, 1
    delta_star = (T-R)/(T-P)
    ck(math.isclose(delta_star, .5), 'grim-trigger threshold')
    qcheck(qmap, 'ch10-q01', 'δ≥0.5。')
    delta = .8
    coop_pv = R/(1-delta)
    dev_pv = T + delta*P/(1-delta)
    ck(math.isclose(coop_pv,15) and math.isclose(dev_pv,9), 'repeated-game PV')
    qcheck(qmap, 'ch10-q02', '15。')
    qcheck(qmap, 'ch10-q03', '9。')

    enter_04 = .4*(-1) + .6*2
    enter_08 = .8*(-1) + .2*2
    ck(math.isclose(enter_04,.8) and math.isclose(enter_08,-.4), 'Bayesian entry expectation')
    qcheck(qmap, 'ch11-q02', '0.8。')
    qcheck(qmap, 'ch11-q03', '-0.4。')

    first_price = (3-1)/3 * .9
    ck(math.isclose(first_price,.6), 'first-price bid')
    qcheck(qmap, 'ch12-q01', '0.6。')
    posterior = .6/(.6 + .4*.25)
    ck(math.isclose(posterior,6/7), 'Bayes posterior')
    qcheck(qmap, 'ch13-q03', '6/7，約0.8571。')

    h_signal = 10 - 2.1
    l_mimic = 10 - 3*2.1
    l_mimic_bad_signal = 10 - 3*1.5
    ck(math.isclose(h_signal,7.9) and math.isclose(l_mimic,3.7) and math.isclose(l_mimic_bad_signal,5.5), 'signaling IC arithmetic')
    qcheck(qmap, 'ch14-q02', '7.9。')
    qcheck(qmap, 'ch14-q03', '3.7。')
    qcheck(qmap, 'ch14-q04', '5.5，會想模仿。')

    h_high_old = 100-80
    h_low = 100*.5-25
    h_high_new = 100-70
    l_high_new = 50-70
    ck((h_high_old,h_low,h_high_new,l_high_new) == (20,25,30,-20), 'screening utilities')
    qcheck(qmap, 'ch15-q02', '20。')
    qcheck(qmap, 'ch15-q03', '25；不是 IC。')
    qcheck(qmap, 'ch15-q04', 'H=30，L=-20。')

    values = [100,80,50]
    vcg_payment = sorted(values, reverse=True)[1]
    winner_utility = max(values)-vcg_payment
    ck((vcg_payment,winner_utility)==(80,20), 'VCG reconstruction')
    qcheck(qmap, 'ch16-q03', 'NT$80。')
    qcheck(qmap, 'ch16-q04', 'NT$20。')

    grand = 90
    pair_value = 60
    equal_share = grand/3
    ck(equal_share*2 == pair_value, 'cooperative-game core reconstruction')
    qcheck(qmap, 'ch17-q04', '(30,30,30)。')

    ccheck(qmap, 'ch02-q03', '是。')
    ccheck(qmap, 'ch03-q05', '不保證。')
    ccheck(qmap, 'ch04-q05', '因 A 的 p 決定 B 面對各純策略的期望報酬。')
    ccheck(qmap, 'ch05-q05', '不能。')
    ccheck(qmap, 'ch08-q01', '是。')
    ccheck(qmap, 'ch08-q02', '不是。')
    ccheck(qmap, 'ch09-q01', '不是。')
    ccheck(qmap, 'ch10-q05', '不是。')
    ccheck(qmap, 'ch11-q01', '型態到行動的映射。')
    ccheck(qmap, 'ch12-q03', '標準私人價值環境。')
    ccheck(qmap, 'ch12-q05', '不是。')
    ccheck(qmap, 'ch13-q01', '完整策略與信念。')
    ccheck(qmap, 'ch13-q05', '不可以。')
    ccheck(qmap, 'ch14-q05', '不一定。')
    ccheck(qmap, 'ch15-q01', 'screening 常由資訊較少的一方先設計選單；signaling 則由有私人資訊的一方先送訊號。')
    ccheck(qmap, 'ch16-q05', '是。')
    ccheck(qmap, 'ch17-q05', '不一定。')
    ccheck(qmap, 'ch18-q05', '不應。')
    ccheck(qmap, 'ch19-q05', '不是。')

    corpus = ' '.join(
        [c['problem'] for c in CHAPTERS]
        + [x for c in CHAPTERS for x in c['intuition']]
        + [d for c in CHAPTERS for _,d in c['definitions']]
        + [x for c in CHAPTERS for x in c['traps']]
        + [x for c in CHAPTERS for x in c['exam']]
    )
    for phrase in [
        '效率', '弱劣勢', '支撐集', '一般總和', '真正子賽局', '折現',
        '共同先驗', '私人價值', 'Bayes', '序列理性', 'off-path',
        '誘因相容', '個別理性', '準線性', '不一定在 core',
    ]:
        ck(phrase in corpus, f'missing caveat {phrase}')

    print(
        f'GAME_THEORY_SECOND_PASS_OK checks={checks} '
        f'chapters=20 questions=100 quantitative_rechecks={quantitative} concept_rechecks={conceptual}'
    )


if __name__ == '__main__':
    main()
