from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

from patch_intermediate_accounting_v2 import main as apply_v2_patch

BOOK_ID = 'intermediate-accounting'
BASE_VERSION = '2026.07.29-1'
BOOK_VERSION = '2026.07.29-2'
REQUIRED_PRE_IDS = {
    'calculus', 'accounting', 'economics', 'statistics',
    'commercial-law', 'cost-accounting', 'microeconomics',
}
ALLOWED_CHANGED_QUESTION_FIELDS = {
    'ch02-q02': {'explanation'},
    'ch04-q05': {'explanation'},
    'ch11-q04': {'explanation'},
    'ch17-q04': {'question', 'answer', 'explanation'},
}
EXPECTED_CHANGED_CHAPTER_FILES = {
    'ch01.html', 'ch02.html', 'ch04.html', 'ch07.html', 'ch11.html',
    'ch12.html', 'ch17.html', 'ch18.html', 'ch21.html', 'appendix-b.html',
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_tree(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): file_sha256(path)
        for path in sorted(root.rglob('*')) if path.is_file()
    }


def main() -> None:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
    expected_version = os.environ.get('EXPECTED_LIBRARY_VERSION')
    pre_path = os.environ.get('PRE_LIBRARY_JSON')
    if not expected_version or not pre_path:
        raise SystemExit('EXPECTED_LIBRARY_VERSION and PRE_LIBRARY_JSON are required')

    checks = 0

    def ck(condition: bool, message: str) -> None:
        nonlocal checks
        if not condition:
            raise AssertionError(message)
        checks += 1

    pre = json.loads(Path(pre_path).read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    pre_ids = [book['id'] for book in pre['books']]
    post_ids = [book['id'] for book in library['books']]
    ck(REQUIRED_PRE_IDS.issubset(set(pre_ids)), f'pre library missing required ids: {pre_ids}')
    ck(BOOK_ID not in pre_ids, 'intermediate accounting unexpectedly existed before generation')
    ck(post_ids == pre_ids + [BOOK_ID], f'book order drift: {post_ids}')
    ck(library['version'] == expected_version, 'shared library version mismatch')

    existing_tree_before: dict[str, dict[str, str]] = {}
    for existing_id in pre_ids:
        existing_root = site / 'books' / existing_id
        manifest = json.loads((existing_root / 'manifest.json').read_text(encoding='utf-8'))
        questions = json.loads((existing_root / 'questions.json').read_text(encoding='utf-8'))
        search = json.loads((existing_root / 'search.json').read_text(encoding='utf-8'))
        ck(manifest['id'] == existing_id, f'existing manifest id {existing_id}')
        ck(questions['count'] == len(questions['items']) > 0, f'existing questions {existing_id}')
        ck(bool(search['entries']), f'existing search {existing_id}')
        existing_tree_before[existing_id] = snapshot_tree(existing_root)

    root = site / 'books' / BOOK_ID
    manifest_before = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions_before = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    chapter_hashes_before = {
        Path(item['file']).name: file_sha256(root / item['file'])
        for item in manifest_before['chapters']
    }
    shell_hashes_before = {name: file_sha256(site / name) for name in ('app.js', 'styles.css', 'sw.js')}
    first_application = manifest_before['version'] == BASE_VERSION
    ck(manifest_before['version'] in {BASE_VERSION, BOOK_VERSION}, 'unexpected pre-patch manifest version')
    ck(questions_before['version'] in {BASE_VERSION, BOOK_VERSION}, 'unexpected pre-patch question version')

    apply_v2_patch(str(site))

    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    ck(manifest['version'] == questions['version'] == BOOK_VERSION, 'v2 version mismatch')
    chapters = [item for item in manifest['chapters'] if item['kind'] == 'chapter']
    appendices = [item for item in manifest['chapters'] if item['kind'] == 'appendix']
    ck(len(chapters) == 22, '22 chapters')
    ck(len(appendices) == 3, '3 appendices')
    ck(questions['count'] == len(questions['items']) == 110, '110 questions')
    ck(len(search['entries']) == 145, '145 search entries')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(22)}, '5 questions/chapter')
    ck(len({q['id'] for q in questions['items']}) == 110, 'unique question ids')
    ck(any(note.get('version') == BOOK_VERSION for note in manifest.get('releaseNotes', [])), 'v2 release note')

    for question in questions['items']:
        for key in ('id', 'chapterId', 'topic', 'difficulty', 'question', 'answer', 'explanation', 'source'):
            ck(bool(question.get(key)), f'{question.get("id")} missing {key}')

    if first_application:
        before_q = {q['id']: q for q in questions_before['items']}
        after_q = {q['id']: q for q in questions['items']}
        ck(list(before_q) == list(after_q), 'question id/order drift')
        changed_questions = set()
        for qid in before_q:
            fields = set(before_q[qid]) | set(after_q[qid])
            changed_fields = {key for key in fields if before_q[qid].get(key) != after_q[qid].get(key)}
            if changed_fields:
                changed_questions.add(qid)
                ck(qid in ALLOWED_CHANGED_QUESTION_FIELDS, f'unexpected question change {qid}')
                ck(changed_fields <= ALLOWED_CHANGED_QUESTION_FIELDS[qid], f'unexpected changed fields {qid}: {changed_fields}')
        ck(changed_questions == set(ALLOWED_CHANGED_QUESTION_FIELDS), f'changed question set drift: {changed_questions}')

        chapter_hashes_after = {
            Path(item['file']).name: file_sha256(root / item['file'])
            for item in manifest['chapters']
        }
        changed_chapters = {name for name in chapter_hashes_before if chapter_hashes_before[name] != chapter_hashes_after[name]}
        ck(changed_chapters == EXPECTED_CHANGED_CHAPTER_FILES, f'changed chapter set drift: {changed_chapters}')

    for existing_id in pre_ids:
        ck(existing_tree_before[existing_id] == snapshot_tree(site / 'books' / existing_id), f'existing book changed: {existing_id}')
    for name, digest in shell_hashes_before.items():
        ck(digest == file_sha256(site / name), f'correction layer changed {name}')

    for chapter in manifest['chapters']:
        path = root / chapter['file']
        ck(path.is_file() and path.stat().st_size > 300, f'missing/short {path}')
    for chapter in chapters:
        ck(not any(term in chapter['title'] for term in ('企業合併', '合併財務報表', '外幣換算', '分公司會計')), f'advanced boundary drift {chapter["title"]}')

    all_text = '\n'.join((root / item['file']).read_text(encoding='utf-8') for item in manifest['chapters'])
    required_tokens = (
        'IFRS 9', 'IFRS 15', 'IFRS 16', 'IAS 12', 'IFRS 18', '2028',
        '預期信用損失', '有效利率', '可回收金額', '遞延所得稅', '每股盈餘', '現金流量',
        '不是資產定義本身的固定機率門檻', '僅要求在報導日後遵守的條件不影響當日分類',
        '為支應短期現金承諾而持有', '自取得日起原始到期日約三個月內', '依 IAS 2 判斷是否進入存貨成本',
        '不得重分類至損益，但可在權益內移轉', '股利通常列入損益，除非該股利明確代表投資成本的一部分收回',
        '2026 IFRS 9 更新提醒', 'FVTPL 金融負債的交易成本則於發生時認列損益', '2026 電子支付除列提醒',
        '不超過 12 個月且不含購買選擇權', '資產「全新時」的價值判斷', '單一交易的初始認列豁免', '租賃與除役義務是常見例子',
        '以 IFRS 18 的「營業損益」小計作為營業現金流調節起點', '利息收入與股利收入原則列投資活動', '利息支出與股利支付原則列籌資活動',
        'Annual Improvements—Volume 11', '自然條件相依電力合約',
    )
    for token in required_tokens:
        ck(token in all_text, f'missing v2 concept: {token}')
    forbidden = (
        '短期租賃及低價值標的資產租賃可依政策選擇不採一般承租人資產負債認列模式',
        '初始估計現值通常同時增加 PPE 成本與負債準備',
        '股利原則在符合收益定義時列損益',
        '一般按攤銷後成本衡量的金融負債，初始通常按公允價值加減可直接歸屬交易成本',
    )
    for obsolete in forbidden:
        ck(obsolete not in all_text, f'obsolete shorthand survived: {obsolete}')
    ck('\x00' not in all_text and '\x0c' not in all_text, 'control characters in chapter content')

    qmap = {q['id']: q for q in questions['items']}
    ck(qmap['ch17-q04']['question'] == '租賃期間為 12 個月但含購買選擇權，是否屬 IFRS 16 定義的短期租賃？', 'lease q4 wording')
    ck(qmap['ch17-q04']['answer'] == '不屬於。', 'lease q4 answer')
    ck('權益內移轉' in qmap['ch11-q04']['explanation'], 'equity FVOCI explanation')
    ck('後者不影響報導日分類' in qmap['ch02-q02']['explanation'], 'covenant explanation')
    ck('短期現金承諾' in qmap['ch04-q05']['explanation'], 'cash equivalent explanation')

    figures = sorted((site / 'assets/intermediate-accounting-svg').glob('*.svg'))
    ck(len(figures) == 22, '22 figures')
    for figure in figures:
        svg = figure.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox' in svg, f'svg structure {figure.name}')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f'study-library-{expected_version}' in sw, 'service worker library version')
    for path in (
        './books/cost-accounting/manifest.json', './books/microeconomics/manifest.json',
        './books/intermediate-accounting/manifest.json', './books/intermediate-accounting/questions.json', './books/intermediate-accounting/search.json',
        './books/intermediate-accounting/chapters/ch21.html', './books/intermediate-accounting/chapters/appendix-c.html', './assets/intermediate-accounting-svg/ch21.svg',
    ):
        ck(path in sw, f'sw path {path}')

    app = (site / 'app.js').read_text(encoding='utf-8')
    styles = (site / 'styles.css').read_text(encoding='utf-8')
    ck('查看版本與更新內容' in app, 'release UI')
    ck('.release-notes{' in styles, 'release note CSS')

    quantitative = {
        'present_value': math.isclose(110000 / (1.10 ** 2), 90909.090909, rel_tol=1e-9),
        'future_value': 100000 * (1.05 ** 2) == 110250,
        'ecl': 800000 * 0.02 == 16000,
        'ecl_adjustment': 800000 * 0.02 - 5000 == 11000,
        'inventory_nrv': 128000 - 6000 - 5000 == 117000,
        'inventory_write_down': 120000 - (128000 - 6000 - 5000) == 3000,
        'depreciation': (600000 - 100000) / 5 == 100000,
        'disposal_gain': 330000 - (1000000 - 700000) == 30000,
        'decommission_cost': 1000000 + 80000 == 1080000,
        'impairment': 500000 - max(420000, 450000) == 50000,
        'held_for_sale': min(900000, 870000) == 870000,
        'bond_interest': 940000 * 0.06 == 56400,
        'bond_cash_interest': 1000000 * 0.04 == 40000,
        'bond_amortisation': 56400 - 40000 == 16400,
        'bond_ending': 940000 + 16400 == 956400,
        'warranty': 10000 * 0.08 * 500 + 10000 * 0.02 * 2000 == 800000,
        'weighted_shares': 100000 * 3 / 12 + 120000 * 6 / 12 + 108000 * 3 / 12 == 112000,
        'basic_eps': 560000 / 112000 == 5,
        'allocation_a': 9000 * 6000 / 9000 == 6000,
        'allocation_b': 9000 * 3000 / 9000 == 3000,
        'lease_interest': 500000 * 0.05 == 25000,
        'lease_liability': 500000 + 25000 - 120000 == 405000,
        'temporary_difference': 800000 - 700000 == 100000,
        'dtl': (800000 - 700000) * 0.20 == 20000,
        'benefit_liability': 5000000 - 4400000 == 600000,
        'cfo': 500000 + 80000 - 60000 + 30000 + 20000 == 570000,
        'bond_loss_example': 30000 == 30000,
        'inventory_error_effect': 20000 == 20000,
    }
    for label, ok in quantitative.items():
        ck(ok, f'quantitative recomputation {label}')

    numeric_answers = {
        'ch03-q02': 'NT$110,250。', 'ch04-q01': 'NT$16,000。', 'ch04-q02': 'NT$11,000。', 'ch05-q01': 'NT$117,000。', 'ch05-q02': 'NT$3,000。',
        'ch06-q01': 'NT$100,000。', 'ch06-q04': '利益 NT$30,000。', 'ch07-q01': 'NT$1,080,000。', 'ch09-q01': 'NT$50,000。', 'ch10-q03': 'NT$870,000。',
        'ch12-q01': 'NT$56,400。', 'ch12-q02': 'NT$40,000。', 'ch12-q03': '折價攤銷 NT$16,400；期末帳面 NT$956,400。', 'ch12-q05': '清償損失 NT$30,000。',
        'ch13-q02': 'NT$800,000。', 'ch15-q01': '112,000 股。', 'ch15-q02': 'NT$5。', 'ch16-q02': 'NT$6,000 與 NT$3,000。', 'ch17-q01': 'NT$25,000。',
        'ch17-q02': 'NT$405,000。', 'ch18-q01': 'NT$100,000。', 'ch18-q02': 'NT$20,000。', 'ch19-q01': 'NT$600,000。', 'ch21-q01': 'NT$570,000。',
    }
    for qid, answer in numeric_answers.items():
        ck(qmap[qid]['answer'] == answer, f'numeric answer {qid}')

    print(
        'INTERMEDIATE_ACCOUNTING_V2_VALIDATION_OK '
        f'checks={checks} books={len(post_ids)} library={expected_version} chapters=22 appendices=3 '
        'questions=110 search=145 figures=22 corrected_chapters=10 changed_questions=4 quantitative_rechecks=28'
    )


if __name__ == '__main__':
    main()
