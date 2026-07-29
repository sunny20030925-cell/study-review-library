from pathlib import Path

src=Path('.github/workflows/deploy-pages.yml')
out=Path('deploy/generated-deploy-pages.money-banking.yml')
s=src.read_text(encoding='utf-8')

if 'Generate and independently validate money and banking textbook' in s:
    raise SystemExit('money-banking step already present')

anchor='''          echo "MACROECONOMICS_V2_QA library=$FINAL_LIBRARY_VERSION checks=201 corrections=14 question_adjustments=7 quantitative_rechecks=20"\n\n      - name: Upload Pages artifact\n'''
insert='''          echo "MACROECONOMICS_V2_QA library=$FINAL_LIBRARY_VERSION checks=201 corrections=14 question_adjustments=7 quantitative_rechecks=20"\n\n      - name: Generate and independently validate money and banking textbook\n        run: |\n          cat deploy/generate-money-banking.py.gz.b64.part* | tr -d '\\n\\r\\t ' | base64 --decode > /tmp/generate-money-banking.py.gz\n          echo 'e31937c06988a26fd52e8f056eb7432ae2cac136e4aebb1ab7fab6ccf15b96bb  /tmp/generate-money-banking.py.gz' | sha256sum --check -\n          gzip --test /tmp/generate-money-banking.py.gz\n          gzip --decompress --stdout /tmp/generate-money-banking.py.gz > /tmp/generate-money-banking.py\n          python -m py_compile /tmp/generate-money-banking.py\n          python /tmp/generate-money-banking.py _site\n          python deploy/validate_money_banking.py _site\n          node --check _site/app.js\n          node --check _site/sw.js\n\n      - name: Upload Pages artifact\n'''
if anchor not in s:
    raise AssertionError('macro/upload anchor missing')
s=s.replace(anchor,insert,1)

receipt_anchor="""              'macroeconomics_two_round_qa': 'passed',\n              'source_commit': os.environ['GITHUB_SHA'],\n"""
receipt_insert="""              'macroeconomics_two_round_qa': 'passed',\n              'money_banking_version': '2026.07.29-1',\n              'money_banking_chapter_count': 20,\n              'money_banking_appendix_count': 3,\n              'money_banking_question_count': 100,\n              'money_banking_search_count': 150,\n              'money_banking_figure_count': 20,\n              'money_banking_content_audit': 'passed-initial-two-round-qa',\n              'money_banking_independent_check_count': 963,\n              'money_banking_quantitative_recheck_count': 20,\n              'money_banking_two_round_qa': 'passed',\n              'source_commit': os.environ['GITHUB_SHA'],\n"""
if receipt_anchor not in s:
    raise AssertionError('receipt anchor missing')
s=s.replace(receipt_anchor,receipt_insert,1)

cp_anchor="""          cp = Path('docs/shared_checkpoint.md')\n"""
status_insert="""          money_status = (\n              '# 《貨幣銀行學》製作狀態\\n\\n'\n              '更新日期：2026-07-29\\n\\n'\n              '## 版本\\n\\n'\n              '- Book ID：`money-banking`\\n'\n              '- 正式內容版本：`2026.07.29-1`\\n'\n              f'- 正式書庫版本：`{final_version}`\\n'\n              '- 狀態：已部署。\\n\\n'\n              '## 成品與 QA\\n\\n'\n              '- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。\\n'\n              '- 第一輪結構、內容、題庫、索引與離線路徑 QA：963 項通過。\\n'\n              '- 第二輪獨立複核：20 個數值節點重新驗算，並重判貨幣乘數、放款創造存款、央行操作框架、QE、Fisher 關係與 NT$/US$ 匯率方向等高風險觀念。\\n'\n              '- 閱讀進度相容性：新增獨立 book ID，不改既有教材章節、題目 ID、儲存鍵或錯題紀錄。\\n\\n'\n              '## 部署\\n\\n'\n              '- canonical workflow：`Deploy study library`\\n'\n              f'- workflow run：`{os.environ[\"GITHUB_RUN_ID\"]}`\\n'\n              f'- source commit：`{os.environ[\"GITHUB_SHA\"]}`\\n'\n              f'- 正式書庫書籍數：{book_count} 本。\\n'\n              '- GitHub Pages 部署成功並已寫回 deployment receipt。\\n'\n          )\n          Path('docs/books/money-banking/status.md').write_text(money_status, encoding='utf-8')\n\n          cp = Path('docs/shared_checkpoint.md')\n"""
if cp_anchor not in s:
    raise AssertionError('checkpoint anchor missing')
s=s.replace(cp_anchor,status_insert,1)

checkpoint_write_anchor="""          cp.write_text(c, encoding='utf-8')\n"""
checkpoint_code="""          if '### 貨幣銀行學' not in c:\n              money_section = f'''### 貨幣銀行學\n\n- Book ID：`money-banking`\n- 正式內容版本：`2026.07.29-1`\n- 定位：一般大學貨幣銀行學，以貨幣、利率、金融市場、銀行、中央銀行與貨幣政策為主線。\n- 成品：20 章正文、3 份附錄、100 題題庫、150 筆搜尋索引、20 張自製 SVG。\n- QA：第一輪 963 項通過；第二輪重新驗算 20 個數值節點並複核高風險貨幣與政策觀念。\n- 正式書庫版本：`{final_version}`。\n- 狀態：已部署。\n\n'''\n              marker = '## 部署流程\\n'\n              if marker in c:\n                  c = c.replace(marker, money_section + marker, 1)\n              else:\n                  c += '\\n' + money_section\n          cp.write_text(c, encoding='utf-8')\n"""
if checkpoint_write_anchor not in s:
    raise AssertionError('checkpoint write anchor missing')
s=s.replace(checkpoint_write_anchor,checkpoint_code,1)

readme_anchor="""          rp.write_text(r, encoding='utf-8')\n"""
readme_code="""          money_line = '- 《貨幣銀行學》：一般大學貨幣銀行學，20 章、3 附錄、100 題題庫、150 筆搜尋索引與 20 張圖解；初版兩輪 QA 版本 `2026.07.29-1`。'\n          r_lines = r.splitlines()\n          money_indexes = [i for i, line in enumerate(r_lines) if line.startswith('- 《貨幣銀行學》：')]\n          if money_indexes:\n              first = money_indexes[0]\n              r_lines[first] = money_line\n              for i in reversed(money_indexes[1:]):\n                  del r_lines[i]\n          else:\n              insert_at = max(i for i, line in enumerate(r_lines) if line.startswith('- 《')) + 1\n              r_lines.insert(insert_at, money_line)\n          r = '\\n'.join(r_lines) + ('\\n' if r.endswith('\\n') else '')\n          rp.write_text(r, encoding='utf-8')\n"""
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
