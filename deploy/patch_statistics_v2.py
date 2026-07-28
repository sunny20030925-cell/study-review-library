from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
from collections import Counter
import json, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_statistics_v2.py <site-root>')
site = Path(sys.argv[1])
root = site / 'books/statistics'
if not root.is_dir():
    raise SystemExit(f'statistics root not found: {root}')

NEW_VERSION = '2026.07.29-2'
changes = []

def replace(rel, old, new, label):
    path = root / rel
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise AssertionError(f'missing replacement {label} in {rel}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
    changes.append((str(rel), label))

replace(Path('chapters/ch01.html'),
        '隨機分派可在長期上平衡已知與未知混雜因子，是支持因果推論的關鍵。',
        '隨機分派讓處理分派不系統性偏向某些已知或未知混雜因子；在重複隨機化的意義下，各組平均而言具有可比性，但單一實驗仍可能偶然不平衡。這是支持因果推論的關鍵。',
        '隨機分派不保證單次完全平衡')

replace(Path('chapters/ch02.html'),
        '分組時組距應一致、邊界不重疊，並涵蓋全部資料。',
        '入門直方圖通常採等組距，且邊界不重疊並涵蓋全部資料；若使用不等組距，柱高應改用次數密度或相對次數密度，使柱面積而不是單純高度對應次數或比例。',
        '不等組距直方圖密度規則')
replace(Path('chapters/ch02.html'),
        '截斷縱軸、改變長寬比、使用不等組距卻畫等寬柱，都可能誇大或淡化差異。',
        '截斷縱軸、改變長寬比，或使用不等組距卻仍以原始次數當柱高，都可能誇大或淡化差異。',
        '不等組距圖形誤導措辭')

replace(Path('chapters/ch04.html'),
        '變異係數（coefficient of variation, CV）用標準差除以平均數，適合比較具有真實零點之比率尺度資料的相對散布：',
        '變異係數（coefficient of variation, CV）用標準差除以平均數，適合比較同類、具有真實零點之比率尺度資料在不同平均水準下的相對散布；同一變數做正比例單位換算時 CV 不變：',
        'CV 適用範圍')
replace(Path('chapters/ch04.html'),
        '平均數接近 0、可能為負，或量尺沒有真實零點時，不宜使用 CV。',
        '平均數接近 0、可能為負，或量尺沒有真實零點時，不宜使用 CV。CV 雖然沒有單位，也不能因此直接比較性質完全不同的變數。',
        'CV 不可跨不同性質變數濫比')
replace(Path('chapters/ch04.html'),
        r'對任意具有有限變異數的分布，柴比雪夫不等式保證至少 \(1-1/k^2\) 的資料落在平均數正負 \(k\) 個標準差內，但界限較保守。',
        r'對任意具有有限變異數的分布，當 \(k>1\) 時，柴比雪夫不等式保證至少 \(1-1/k^2\) 的資料落在平均數正負 \(k\) 個標準差內，但界限較保守。',
        '柴比雪夫 k 條件')

replace(Path('chapters/ch05.html'),
        '加法處理「或」，乘法處理「且／依序」，排列組合處理結果數；互斥與獨立要分清楚。',
        '加法處理「或」；乘法規則處理「且／依序」，一般要用條件機率，只有獨立時才可簡化為邊際機率直接相乘；排列組合處理結果數。互斥與獨立要分清楚。',
        '乘法規則條件機率前提')

replace(Path('chapters/ch07.html'),
        r'期望值具有線性：\(E(X+Y)=E(X)+E(Y)\)，不需要獨立。若 X、Y 獨立，則 \(Var(X+Y)=Var(X)+Var(Y)\)；不獨立時還要加上協方差項。',
        r'期望值具有線性：\(E(X+Y)=E(X)+E(Y)\)，不需要獨立。一般而言，\(Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)\)。若 X、Y 獨立，則 \(Cov(X,Y)=0\)，才可簡化為兩個變異數相加；反過來，協方差為 0 並不保證一般情況下的獨立。',
        '變異數加總協方差係數')

replace(Path('chapters/ch09.html'),
        r'在 \([a,b]\) 上的連續均勻分配具有固定密度 \(1/(b-a)\)。區間機率等於區間長度除以總長度。',
        r'在 \([a,b]\) 上的連續均勻分配具有固定密度 \(1/(b-a)\)。當 \(a\le c\le d\le b\) 時，區間機率等於區間長度除以總長度。',
        '均勻分配區間公式條件')

replace(Path('chapters/ch11.html'),
        '母體標準差已知且條件適合時用 z 區間：',
        r'樣本觀察獨立，且母體近似常態或樣本數足以使用常態近似時；若母體標準差 \(\sigma\) 已知，可用 z 區間：',
        '平均數 z 區間條件')
replace(Path('chapters/ch11.html'),
        '小樣本 t 區間特別需要母體近似常態、沒有嚴重離群。',
        't 區間同樣要求觀察值獨立；小樣本時特別需要母體近似常態且沒有嚴重離群。',
        't 區間獨立性條件')
replace(Path('chapters/ch11.html'),
        '成功與失敗期望次數要足夠。極端比例或小樣本時，課程可能使用較穩健的 Wilson 或精確區間。',
        r'使用這個基本常態近似時，成功與失敗數要足夠；常見教學檢查是 \(n\hat p\) 與 \(n(1-\hat p)\) 都至少約 10。極端比例或小樣本時，Wilson 或精確區間通常較穩健；實際門檻依課程規範。',
        '比例區間近似條件')

replace(Path('chapters/ch12.html'),
        r'p 值是在 \(H_0\) 成立且模型條件正確時，得到目前或更極端統計量的機率。p 小表示資料與 \(H_0\) 較不相容，但 p 不是 \(H_0\) 為真的機率，也不是效果大小。',
        r'p 值是在 \(H_0\) 成立且模型條件正確時，得到觀察到的檢定統計量或依對立假設方向定義之「同等或更極端」結果的機率。p 小表示資料與 \(H_0\) 較不相容，但 p 不是 \(H_0\) 為真的機率，也不是效果大小。',
        'p 值極端方向定義')

replace(Path('chapters/ch13.html'),
        r'檢定的標準誤用 \(p_0\)，信賴區間的基本標準誤用 \(\hat p\)。這是常考差別。',
        r'檢定的標準誤用 \(p_0\)，而且常態近似條件也在 \(H_0\) 下檢查，例如 \(np_0\) 與 \(n(1-p_0)\) 都要足夠大；信賴區間的基本標準誤則用 \(\hat p\)。這是常考差別。',
        '單一比例檢定近似條件')

old_two_prop = r'''<h2 id="兩母體比例">兩母體比例</h2><p>估計 \(p_1-p_2\) 的區間通常使用各組 \(\hat p_i\) 的未合併標準誤。檢定 \(H_0:p_1=p_2\) 時，因虛無假設認為共同比例相同，基本 z 檢定使用合併比例：</p><p class="math display">\[\hat p_{pool}=\frac{x_1+x_2}{n_1+n_2}\]</p>'''
new_two_prop = r'''<h2 id="兩母體比例">兩母體比例</h2><p>估計 \(p_1-p_2\) 的區間通常使用各組 \(\hat p_i\) 的未合併標準誤：</p><p class="math display">\[SE_{CI}=\sqrt{\frac{\hat p_1(1-\hat p_1)}{n_1}+\frac{\hat p_2(1-\hat p_2)}{n_2}}\]</p><p>檢定 \(H_0:p_1=p_2\) 時，因虛無假設認為共同比例相同，基本 z 檢定改用合併比例與虛無標準誤：</p><p class="math display">\[\hat p_{pool}=\frac{x_1+x_2}{n_1+n_2},\qquad SE_0=\sqrt{\hat p_{pool}(1-\hat p_{pool})\left(\frac1{n_1}+\frac1{n_2}\right)}\]</p>'''
replace(Path('chapters/ch14.html'), old_two_prop, new_two_prop, '兩比例區間與檢定標準誤')

replace(Path('chapters/ch18.html'),
        '符號檢定處理單一中位數或成對差的方向；Wilcoxon 符號等級檢定使用成對差的大小與方向；Mann–Whitney 檢定比較兩獨立組的秩；Kruskal–Wallis 比較三組以上；Spearman 相關衡量單調秩關係。',
        '符號檢定處理單一位置或成對差的正負方向；Wilcoxon 符號等級檢定同時使用成對差的大小與方向，常見位置解讀需要差值分布近似對稱；Mann–Whitney 檢定比較兩獨立組的秩分布，只有在兩組分布形狀相近、主要差在位置時才可直接解讀成位置或中位數差；Kruskal–Wallis 是三組以上的秩方法；Spearman 相關衡量單調秩關係。',
        '非參數方法解讀條件')

replace(Path('chapters/appendix-a.html'),
        r'\[P(A\mid B)=\frac{P(A\cap B)}{P(B)},\quad E(X)=\sum xp(x),\quad Var(X)=E(X^2)-[E(X)]^2\]',
        r'\[P(A\mid B)=\frac{P(A\cap B)}{P(B)},\quad E(X)=\sum xp(x),\quad Var(X)=E(X^2)-[E(X)]^2\]\[Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)\]',
        '附錄協方差公式')
replace(Path('chapters/appendix-a.html'),
        r'\[SE(\bar X)=\sigma/\sqrt n,\quad SE(\hat p)=\sqrt{p(1-p)/n}\]',
        r'\[SE(\bar X)=\sigma/\sqrt n,\quad SE(\hat p)=\sqrt{p(1-p)/n}\]<p>比例區間常以 \(\hat p\) 代入未知 \(p\)；檢定 \(H_0:p=p_0\) 時則用 \(p_0\) 建立虛無標準誤。</p>',
        '附錄比例標準誤用途')

replace(Path('chapters/appendix-b.html'),
        '<tr><td>估計或檢定一個平均數</td><td>數量</td><td>單一樣本 t 或 z</td></tr>',
        '<tr><td>估計或檢定一個平均數</td><td>數量</td><td>通常用單一樣本 t；只有母體 σ 已知等特定條件才用 z</td></tr>',
        '附錄平均數方法選擇')

qpath = root / 'questions.json'
q = json.loads(qpath.read_text(encoding='utf-8'))
byid = {item['id']: item for item in q['items']}
byid['ch01-q03']['answer'] = '讓處理分派在隨機機制下不系統性偏向某些混雜因子，使各組平均而言更可比。'
byid['ch01-q03']['explanation'] = '隨機分派支持因果比較，但單一實驗仍可能偶然出現組間不平衡。'
byid['ch04-q05']['answer'] = '同類、具有真實零點的比率尺度資料在不同平均水準下的相對散布。'
byid['ch04-q05']['explanation'] = 'CV=標準差÷平均數；同一變數做正比例單位換算時 CV 不變，但不應只因無單位就比較性質完全不同的變數。'
byid['ch17-q02']['question'] = '在含截距的簡單線性迴歸中，r=0.8 時，R² 是多少？'
byid['ch17-q02']['answer'] = '0.64 或 64%。'
byid['ch17-q02']['explanation'] = '含截距的簡單線性迴歸中，R²=r²=0.8²=0.64。'
q['version'] = NEW_VERSION
qpath.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changes.append(('questions.json', '3 題答案／題幹／詳解精確化'))

mpath = root / 'manifest.json'
m = json.loads(mpath.read_text(encoding='utf-8'))
m['version'] = NEW_VERSION
mpath.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changes.append(('manifest.json', '統計學版本提升'))

def section_text(nodes):
    container = BeautifulSoup('<div></div>', 'html.parser').div
    for node in nodes:
        frag = BeautifulSoup(str(node), 'html.parser')
        for child in list(frag.contents):
            container.append(child)
    return ' '.join(container.stripped_strings)

entries = []
for ch in m['chapters']:
    html_path = root / ch['file']
    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'html.parser')
    children = [c for c in soup.contents if not (isinstance(c, NavigableString) and not str(c).strip())]
    headings = [i for i,c in enumerate(children) if isinstance(c, Tag) and c.name == 'h2']
    first = headings[0] if headings else len(children)
    lead = section_text(children[:first])
    if lead:
        entries.append({'chapterId': ch['id'], 'chapterTitle': ch['title'], 'page': 0, 'title': ch['title'], 'text': lead})
    page = 1
    for pos_idx, start in enumerate(headings):
        end = headings[pos_idx+1] if pos_idx+1 < len(headings) else len(children)
        title = ' '.join(children[start].stripped_strings)
        text = section_text(children[start:end])
        entries.append({'chapterId': ch['id'], 'chapterTitle': ch['title'], 'page': page, 'title': title, 'text': text})
        page += 1
(root / 'search.json').write_text(json.dumps({'entries': entries}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changes.append(('search.json', '依修正文重建全文搜尋索引'))

assert q['count'] == 95 == len(q['items'])
assert len({item['id'] for item in q['items']}) == 95
assert Counter(item['chapterId'] for item in q['items']) == {f'ch{i:02d}': 5 for i in range(19)}
assert len([x for x in m['chapters'] if x['kind'] == 'chapter']) == 19
assert len([x for x in m['chapters'] if x['kind'] == 'appendix']) == 3
assert len(entries) == 169
assert m['version'] == q['version'] == NEW_VERSION

blob = '\n'.join((root / ch['file']).read_text(encoding='utf-8') for ch in m['chapters'])
required = [
    '單一實驗仍可能偶然不平衡', '次數密度或相對次數密度',
    'CV 雖然沒有單位，也不能因此直接比較性質完全不同的變數',
    r'當 \(k>1\) 時', '只有獨立時才可簡化為邊際機率直接相乘',
    'Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)', r'a\le c\le d\le b',
    r'n\hat p', '依對立假設方向定義之「同等或更極端」', 'np_0',
    'SE_{CI}', 'SE_0', '只有在兩組分布形狀相近、主要差在位置時',
]
for token in required:
    assert token in blob, token
for token in ['分組時組距應一致、邊界不重疊', '不獨立時還要加上協方差項', '得到目前或更極端統計量的機率']:
    assert token not in blob, token
assert '不同平均水準或不同單位但比率尺度資料的相對散布' not in json.dumps(q, ensure_ascii=False)

expected_answers = {
    'ch03-q03': '約 76.67 分。', 'ch04-q01': 's²=4，s=2。', 'ch05-q02': '0.7。',
    'ch06-q05': '約 30.8%。', 'ch07-q04': '20。', 'ch08-q02': '3/8=0.375。',
    'ch09-q05': '125.6。', 'ch10-q02': '約 0.0214。', 'ch11-q01': '約 [46.08,53.92]。',
    'ch11-q02': '約 0.048。', 'ch13-q01': '2。', 'ch13-q02': '1。',
    'ch14-q03': '約 0.640。', 'ch15-q01': '12。', 'ch15-q02': '6。',
    'ch16-q02': '16。', 'ch17-q02': '0.64 或 64%。',
}
for qid, ans in expected_answers.items():
    assert byid[qid]['answer'] == ans, (qid, byid[qid]['answer'])

for ch in m['chapters']:
    p = root / ch['file']
    soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    assert soup.get_text(strip=True)
    for tag in soup.find_all(['a','img']):
        attr = 'href' if tag.name == 'a' else 'src'
        if tag.has_attr(attr):
            assert str(tag[attr]).strip(), (ch['id'], tag)

print(json.dumps({
    'statistics_version': NEW_VERSION,
    'content_replacements': len(changes),
    'questions': len(q['items']), 'search_entries': len(entries),
    'chapters': len([x for x in m['chapters'] if x['kind'] == 'chapter']),
    'appendices': len([x for x in m['chapters'] if x['kind'] == 'appendix']),
}, ensure_ascii=False, indent=2))
for rel, label in changes:
    print(f'{rel}: {label}')
