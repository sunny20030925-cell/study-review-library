from __future__ import annotations

from copy import deepcopy

import industrial_economics_questions as v1
from industrial_economics_content_v2 import CHAPTERS


OVERRIDES = deepcopy(v1.OVERRIDES)
OVERRIDES.update({
    'ch02-q05': {
        'question': '自然獨占最精確的成本判斷是什麼？',
        'answer': '在相關需求範圍內，單一廠商供應總產量的成本低於把同一總產量拆給多家廠商生產。',
        'explanation': '自然獨占的核心是成本函數在相關產量範圍內具有次可加性（subadditivity）。「市場只剩一家」是市場結果，不是定義本身；平均成本下降是常見背景，也不是唯一正式判準。',
    },
    'ch03-q05': {
        'question': '使用 Lerner index 與需求彈性的關係 L=1/|epsilon| 時，還要注意哪個重要條件？',
        'answer': '它是標準單一產品內點利潤最大化的一階條件，正加價的內點解位於 |epsilon|>1 的需求彈性區段。',
        'explanation': '這個簡單關係不能無條件套到多產品、容量限制、價格管制或不可微需求；epsilon 也應是廠商實際面對的需求彈性。',
    },
    'ch04-q05': {
        'question': '三級價格歧視下，如果總銷量恰好不變，是否就能斷言總福利只是在消費者與廠商之間重新分配？',
        'answer': '不能。',
        'explanation': '總量是重要線索但不是唯一判準。若不同市場間的銷售配置改變，高邊際願付價格者可能被排除而較低邊際願付價格者取得商品，總剩餘仍可能改變。',
    },
    'ch06-q03': {
        'question': '逆需求 P=100-2Q、MC=20。若其他廠商總產量 Q_-i=10，Cournot 廠商 i 的最佳反應產量是多少？',
        'answer': 'q_i=15。',
        'explanation': '正確反應函數是 q_i=(a-c-bQ_-i)/(2b)。代入 a=100、c=20、b=2、Q_-i=10，得 (100-20-20)/4=15。這題刻意使用 b≠1，以避免 v1 漏寫 b 的公式錯誤被 b=1 例題掩蓋。',
    },
    'ch09-q05': {
        'question': 'Hotelling 單位線算出無差異點 x*=1.2 時，可以直接說左廠商服務 120% 市場嗎？',
        'answer': '不可以。',
        'explanation': '標準兩端點、全市場覆蓋的內點需求分割公式要求邊界消費者落在 [0,1]。若 x* 超出線段，要改用角點需求；若市場未完全覆蓋，還要重新考慮不購買選項。',
    },
    'ch11-q05': {
        'question': '為什麼不能直接用「每年進入後利潤 NT$2,000,000 ≥ 一次性進入成本 NT$1,000,000」判定值得進入？',
        'answer': '因為流量利潤與一次性投資成本必須先轉成可比較的現值。',
        'explanation': '進入是跨期投資決策，應把未來各期增量經濟利潤折現成現值，再與不可回收的進入成本比較；同時還要考慮營運期間、退出與其他可避免成本。',
    },
    'ch12-q05': {
        'question': '台灣公平交易法下，沒有書面或口頭直接協議，是否就一定不能成立聯合行為？',
        'answer': '不一定。',
        'explanation': '第 14 條要求具競爭關係事業存在合意並足以影響市場功能，但合意可依市場狀況、商品特性、成本與利潤、行為經濟合理性等相當依據推定。單純平行行為也不能自動等同已有合意。',
    },
    'ch13-q05': {
        'question': '在台灣制度下，能否只因經濟學上某種 RPM 可能改善服務誘因，就直接判定法律上一定合法？',
        'answer': '不能。',
        'explanation': '公平交易法第 19 條原則禁止限制轉售價格，但有正當理由者例外。經濟效率理由可與法律分析相關，但實際是否有正當理由仍須依現行法規與個案事實判斷。',
    },
    'ch18-q04': {
        'question': '兩家競爭者價格長期高度相似，是否僅憑此即可證明聯合行為成立？反過來，沒有直接協議文件是否就一定不成立？',
        'answer': '兩個推論都不可以直接成立。',
        'explanation': '相似價格可能來自共同成本或獨立平行反應，不能單獨完成合意判斷；但公平交易法第 14 條又允許依市場狀況、商品特性、成本及利潤、行為經濟合理性等相當依據推定合意，所以也不能要求一定要有直接協議文件。',
    },
})


def build_questions():
    original_chapters = v1.CHAPTERS
    original_overrides = v1.OVERRIDES
    try:
        v1.CHAPTERS = CHAPTERS
        v1.OVERRIDES = OVERRIDES
        items = v1.build_questions()
    finally:
        v1.CHAPTERS = original_chapters
        v1.OVERRIDES = original_overrides
    assert len(items) == 100
    assert len({x['id'] for x in items}) == 100
    return items
