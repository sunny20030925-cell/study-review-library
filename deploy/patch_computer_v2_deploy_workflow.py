#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

WORKFLOW = Path('.github/workflows/deploy-pages.yml')
STEP_NAME = 'Apply or validate computer fundamentals post-publication v2 reaudit'
RECORDER = 'python deploy/record_computer_fundamentals_v2_deployment.py _site'
POST_QA = 'PYTHONPATH=deploy python deploy/qa_computer_fundamentals_v2.py /tmp/deployed-site "$FINAL_LIBRARY_VERSION"'

COMPUTER_STEP = r'''      - name: Apply or validate computer fundamentals post-publication v2 reaudit
        run: |
          set -euo pipefail
          python -m py_compile \
            deploy/patch_computer_fundamentals_v2.py \
            deploy/finalize_computer_fundamentals_v2_library.py \
            deploy/qa_computer_fundamentals_v2.py \
            deploy/apply_computer_fundamentals_v2.py \
            deploy/record_computer_fundamentals_v2_deployment.py

          python - <<'PY'
          import json
          d=json.load(open('_site/data/library.json'))
          json.dump([b['id'] for b in d['books']],open('/tmp/pre-computer-v2-ids.json','w'))
          print('COMPUTER_V2_BASE',d['version'],len(d['books']))
          PY
          find _site/books -type f ! -path '*/computer-fundamentals/*' -print0 | sort -z | xargs -0 sha256sum > /tmp/pre-computer-v2-other-books.sha256

          BEFORE="$(python -c "import json;print(json.load(open('_site/data/library.json'))['version'])")"
          FINAL_LIBRARY_VERSION="$(PYTHONPATH=deploy python deploy/apply_computer_fundamentals_v2.py _site "$BEFORE")"
          QA_LINE="$(PYTHONPATH=deploy python deploy/qa_computer_fundamentals_v2.py _site "$FINAL_LIBRARY_VERSION" | tee /tmp/computer-v2-qa.log | tail -n 1)"
          echo "$QA_LINE"
          COMPUTER_V2_QA_CHECKS="$(printf '%s\n' "$QA_LINE" | grep -oE 'checks=[0-9]+' | cut -d= -f2)"
          COMPUTER_V2_NUMERIC_RECHECKS="$(printf '%s\n' "$QA_LINE" | grep -oE 'numeric_rechecks=[0-9]+' | cut -d= -f2)"
          test "$COMPUTER_V2_QA_CHECKS" = "128"
          test "$COMPUTER_V2_NUMERIC_RECHECKS" = "36"

          find _site/books -type f ! -path '*/computer-fundamentals/*' -print0 | sort -z | xargs -0 sha256sum > /tmp/post-computer-v2-other-books.sha256
          diff -u /tmp/pre-computer-v2-other-books.sha256 /tmp/post-computer-v2-other-books.sha256

          export FINAL_LIBRARY_VERSION COMPUTER_V2_QA_CHECKS COMPUTER_V2_NUMERIC_RECHECKS
          echo "FINAL_LIBRARY_VERSION=$FINAL_LIBRARY_VERSION" >> "$GITHUB_ENV"
          echo "COMPUTER_V2_QA_CHECKS=$COMPUTER_V2_QA_CHECKS" >> "$GITHUB_ENV"
          echo "COMPUTER_V2_NUMERIC_RECHECKS=$COMPUTER_V2_NUMERIC_RECHECKS" >> "$GITHUB_ENV"
          python - <<'PY'
          import json,os
          from pathlib import Path
          site=Path('_site')
          lib=json.load(open(site/'data/library.json'))
          ids=[b['id'] for b in lib['books']]
          pre=json.load(open('/tmp/pre-computer-v2-ids.json'))
          assert ids==pre, (pre,ids)
          assert lib['version']==os.environ['FINAL_LIBRARY_VERSION']
          assert ids.count('computer-fundamentals')==1
          root=site/'books/computer-fundamentals'
          m=json.load(open(root/'manifest.json')); q=json.load(open(root/'questions.json')); s=json.load(open(root/'search.json'))
          assert m['version']==q['version']=='2026.07.30-2'
          assert len(m['chapters'])==23 and q['count']==100 and len(s['entries'])==150
          assert len({x['id'] for x in q['items']})==100
          assert len(list((site/'assets/computer-fundamentals-svg').glob('*.svg')))==20
          assert '章節 ID、題目 ID、Book ID、題數與進度儲存鍵均未變' in m['releaseNotes'][0]['progressImpact']
          print('COMPUTER_FUNDAMENTALS_V2_IN_PLACE_OK',lib['version'],len(ids))
          PY
          node --check _site/app.js
          node --check _site/sw.js

'''

POST_DEPLOY_BLOCK = r'''          comp=site/'books/computer-fundamentals'
          cm=json.load(open(comp/'manifest.json')); cq=json.load(open(comp/'questions.json')); cs=json.load(open(comp/'search.json'))
          assert cm['version']==cq['version']=='2026.07.30-2'
          assert len(cm['chapters'])==23 and cq['count']==100 and len(cs['entries'])==150
          assert len({x['id'] for x in cq['items']})==100
          assert len(list((site/'assets/computer-fundamentals-svg').glob('*.svg')))==20
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise AssertionError(f'cannot locate workflow anchor: {label}')
    return text.replace(old, new, 1)


def main() -> None:
    text = WORKFLOW.read_text(encoding='utf-8')

    if STEP_NAME not in text:
        text = replace_once(
            text,
            '      - uses: actions/upload-pages-artifact@v3\n',
            COMPUTER_STEP + '      - uses: actions/upload-pages-artifact@v3\n',
            'upload-pages step',
        )

    if "computer-fundamentals=2026.07.30-2" not in text:
        marker = "          print('DEPLOYED_ARTIFACT_RECHECK_OK'"
        idx = text.find(marker)
        if idx < 0:
            raise AssertionError('cannot locate deployed-artifact recheck print')
        text = text[:idx] + POST_DEPLOY_BLOCK + text[idx:]
        line_end = text.find('\n', idx + len(POST_DEPLOY_BLOCK))
        if line_end < 0:
            raise AssertionError('unterminated deployed-artifact recheck print')
        marker_line = "          print('COMPUTER_FUNDAMENTALS_DEPLOYED_V2_OK','computer-fundamentals=2026.07.30-2')\n"
        text = text[:line_end+1] + marker_line + text[line_end+1:]

    if POST_QA not in text:
        qa_anchor = '          echo "PAGES_ARTIFACT_ID=$ARTIFACT_ID" >> "$GITHUB_ENV"\n'
        text = replace_once(
            text,
            qa_anchor,
            f'          {POST_QA}\n' + qa_anchor,
            'post-deploy QA anchor',
        )

    if RECORDER not in text:
        recorder_anchor = '          git config user.name github-actions[bot]\n'
        text = replace_once(
            text,
            recorder_anchor,
            f'          {RECORDER}\n' + recorder_anchor,
            'structured recorder anchor',
        )

    if 'docs/books/computer-fundamentals/status.md' not in text:
        add_anchor = '            docs/deployment_receipt.json \\\n'
        text = replace_once(
            text,
            add_anchor,
            add_anchor + '            docs/books/computer-fundamentals/status.md \\\n            docs/books/computer-fundamentals/qa_report.md \\\n',
            'git add receipt anchor',
        )

    WORKFLOW.write_text(text, encoding='utf-8')
    print('COMPUTER_FUNDAMENTALS_V2_DEPLOY_WORKFLOW_PATCH_OK')


if __name__ == '__main__':
    main()
