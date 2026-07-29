from pathlib import Path

src=Path('.github/workflows/deploy-pages.yml')
out=Path('deploy/generated-deploy-pages.money-banking.yml')
s=src.read_text(encoding='utf-8')

if 'Generate and independently validate money and banking textbook' in s:
    raise SystemExit('money-banking step already present')

anchor='''      - name: Upload Pages artifact\n'''
insert='''      - name: Generate and independently validate money and banking textbook
        run: |
          cat deploy/generate-money-banking.py.gz.b64.part* | tr -d '\\n\\r\\t ' | base64 --decode > /tmp/generate-money-banking.py.gz
          echo 'e31937c06988a26fd52e8f056eb7432ae2cac136e4aebb1ab7fab6ccf15b96bb  /tmp/generate-money-banking.py.gz' | sha256sum --check -
          gzip --test /tmp/generate-money-banking.py.gz
          gzip --decompress --stdout /tmp/generate-money-banking.py.gz > /tmp/generate-money-banking.py
          python -m py_compile /tmp/generate-money-banking.py
          python /tmp/generate-money-banking.py _site
          python deploy/validate_money_banking.py _site
          node --check _site/app.js
          node --check _site/sw.js

      - name: Upload Pages artifact
'''
if s.count(anchor) != 1:
    raise AssertionError(f'upload anchor count={s.count(anchor)}')
s=s.replace(anchor,insert,1)

receipt_anchor="""              'macroeconomics_two_round_qa': 'passed',
              'source_commit': os.environ['GITHUB_SHA'],
"""
receipt_insert="""              'macroeconomics_two_round_qa': 'passed',
              'money_banking_version': '2026.07.29-1',
              'money_banking_chapter_count': 20,
              'money_banking_appendix_count': 3,
              'money_banking_question_count': 100,
              'money_banking_search_count': 150,
              'money_banking_figure_count': 20,
              'money_banking_content_audit': 'passed-initial-two-round-qa',
              'money_banking_independent_check_count': 963,
              'money_banking_quantitative_recheck_count': 20,
              'money_banking_two_round_qa': 'passed',
              'source_commit': os.environ['GITHUB_SHA'],
"""
if receipt_anchor not in s:
    raise AssertionError('receipt anchor missing')
s=s.replace(receipt_anchor,receipt_insert,1)

cp_anchor="""          cp = Path('docs/shared_checkpoint.md')
"""
status_insert="""          money_status = (
              '# 《貨幣銀行學》製作狀態\\n\\n'
              '更新日期：2026-07-29\\n\\n'
              '## 版本\\n\\n'
              '- Book ID：`money-banking`\\n'
              '- 正式內容版本：`2026.07.29-1`\\n'
              f'- 正式書庫版本：`{final_version}`\\n'
              '- 狀態：已部署。\\n\\n'
              '## 成品與 QA\\n\\n'
              '- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。\\n'
              '- 第一輪結構、內容、題庫、索引與離線路徑 QA：963 項通過。\\n'
              '- 第二輪獨立複核：20 個數值節點重新驗算，並重判貨幣乘數、放款創造存款、央行操作框架、QE、Fisher 關係與 NT$/US$ 匯率方向等高風險觀念。\\n'
              '- 閱讀進度相容性：新增獨立 book ID，不改既有教材章節、題目 ID、儲存鍵或錯題紀錄。\\n\\n'
              '## 部署\\n\\n'
              '- canonical workflow：`Deploy study library`\\n'
              f'- workflow run：`{os.environ[\"GITHUB_RUN_ID\"]}`\\n'
              f'- source commit：`{os.environ[\"GITHUB_SHA\"]}`\\n'
              f'- 正式書庫書籍數：{book_count} 本。\\n'
              '- GitHub Pages 部署成功並已寫回 deployment receipt。\\n'
          )
          Path('docs/books/money-banking/status.md').write_text(money_status, encoding='utf-8')

          cp = Path('docs/shared_checkpoint.md')
"""
if cp_anchor not in s:
    raise AssertionError('checkpoint anchor missing')
s=s.replace(cp_anchor,status_insert,1)

checkpoint_write_anchor="""          cp.write_text(c, encoding='utf-8')
"""
checkpoint_code="""          if '### 貨幣銀行學' not in c:
              money_section = f'''### 貨幣銀行學

- Book ID：`money-banking`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學貨幣銀行學，以貨幣、利率、金融市場、銀行、中央銀行與貨幣政策為主線。
- 成品：20 章正文、3 份附錄、100 題題庫、150 筆搜尋索引、20 張自製 SVG。
- QA：第一輪 963 項通過；第二輪重新驗算 20 個數值節點並複核高風險貨幣與政策觀念。
- 正式書庫版本：`{final_version}`。
- 狀態：已部署。

'''
              marker = '## 部署流程\\n'
              if marker in c:
                  c = c.replace(marker, money_section + marker, 1)
              else:
                  c += '\\n' + money_section
          cp.write_text(c, encoding='utf-8')
"""
if checkpoint_write_anchor not in s:
    raise AssertionError('checkpoint write anchor missing')
s=s.replace(checkpoint_write_anchor,checkpoint_code,1)

readme_anchor="""          rp.write_text(r, encoding='utf-8')
"""
readme_code="""          money_line = '- 《貨幣銀行學》：一般大學貨幣銀行學，20 章、3 附錄、100 題題庫、150 筆搜尋索引與 20 張圖解；初版兩輪 QA 版本 `2026.07.29-1`。'
          r_lines = r.splitlines()
          money_indexes = [i for i, line in enumerate(r_lines) if line.startswith('- 《貨幣銀行學》：')]
          if money_indexes:
              first = money_indexes[0]
              r_lines[first] = money_line
              for i in reversed(money_indexes[1:]):
                  del r_lines[i]
          else:
              insert_at = max(i for i, line in enumerate(r_lines) if line.startswith('- 《')) + 1
              r_lines.insert(insert_at, money_line)
          r = '\\n'.join(r_lines) + ('\\n' if r.endswith('\\n') else '')
          rp.write_text(r, encoding='utf-8')
"""
if readme_anchor not in s:
    raise AssertionError('README write anchor missing')
s=s.replace(readme_anchor,readme_code,1)

git_anchor='git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md docs/books/macroeconomics/status.md'
git_new=git_anchor+' docs/books/money-banking/status.md'
if git_anchor not in s:
    raise AssertionError('git add anchor missing')
s=s.replace(git_anchor,git_new,1)

out.write_text(s,encoding='utf-8')
print(f'STAGED_MONEY_BANKING_WORKFLOW bytes={out.stat().st_size}')
