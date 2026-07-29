#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

PATH = Path('.github/workflows/deploy-pages.yml')
# This file is also an explicit trigger path for the one-shot v2 staging workflow.


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, n = re.subn(pattern, replacement, text, count=1, flags=re.M | re.S)
    if n != 1:
        raise AssertionError(f'{label}: expected one replacement, got {n}')
    return out


def main() -> None:
    text = PATH.read_text(encoding='utf-8')

    if 'Apply or validate industrial economics v2 independent audit' not in text:
        pattern = (
            r'      - name: Validate industrial economics already in formal base\n'
            r'.*?'
            r'(?=      - name: Integrate or validate industry and trade\n)'
        )
        replacement = '''      - name: Apply or validate industrial economics v2 independent audit
        run: |
          set -euo pipefail
          python -m py_compile \\
            deploy/industrial_economics_content_v2.py \\
            deploy/industrial_economics_questions_v2.py \\
            deploy/patch_industrial_economics_v2.py \\
            deploy/validate_industrial_economics_v2.py \\
            deploy/qa_industrial_economics_v2.py \\
            deploy/integrate_industrial_economics_v2.py \\
            deploy/record_industrial_economics_v2_deployment.py
          BEFORE="$(python -c "import json;print(json.load(open('_site/data/library.json'))['version'])")"
          INDUSTRIAL_LIBRARY_VERSION="$(PYTHONPATH=deploy python deploy/integrate_industrial_economics_v2.py _site "$BEFORE")"
          QA1="$(PYTHONPATH=deploy python deploy/validate_industrial_economics_v2.py _site "$INDUSTRIAL_LIBRARY_VERSION" | tee /tmp/industrial-v2-qa1.log | grep -oE '(^| )checks=[0-9]+' | head -n 1 | cut -d= -f2)"
          QA2="$(PYTHONPATH=deploy python deploy/qa_industrial_economics_v2.py _site "$INDUSTRIAL_LIBRARY_VERSION" | tee /tmp/industrial-v2-qa2.log | grep -oE '(^| )checks=[0-9]+' | head -n 1 | cut -d= -f2)"
          test "$QA1" -ge 150
          test "$QA2" -ge 450
          INDUSTRIAL_LIBRARY_VERSION="$INDUSTRIAL_LIBRARY_VERSION" python - <<'PY'
          import json,os
          from pathlib import Path
          site=Path('_site')
          lib=json.load(open(site/'data/library.json'))
          ids=[b['id'] for b in lib['books']]
          base=json.load(open('/tmp/base_ids.json'))
          assert ids==base
          assert ids.count('industrial-economics')==1
          assert ids.index('econometrics') < ids.index('industrial-economics') < ids.index('industry-trade')
          assert lib['version']==os.environ['INDUSTRIAL_LIBRARY_VERSION']
          root=site/'books/industrial-economics'
          m=json.load(open(root/'manifest.json')); q=json.load(open(root/'questions.json')); s=json.load(open(root/'search.json'))
          assert m['version']==q['version']=='2026.07.30-2'
          assert len(m['chapters'])==23 and q['count']==100 and len(s['entries'])==150
          assert len(list((site/'assets/industrial-economics-svg').glob('*.svg')))==20
          assert [x['id'] for x in m['chapters']]==[f'ch{i:02d}' for i in range(20)]+['appendix-a','appendix-b','appendix-c']
          assert [x['id'] for x in q['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)]
          print('INDUSTRIAL_ECONOMICS_V2_IN_PLACE_OK',lib['version'],len(ids))
          PY
          node --check _site/app.js
          node --check _site/sw.js
          echo "INDUSTRIAL_V2_QA1_CHECKS=$QA1" >> "$GITHUB_ENV"
          echo "INDUSTRIAL_V2_QA2_CHECKS=$QA2" >> "$GITHUB_ENV"
          echo "INDUSTRIAL_LIBRARY_VERSION=$INDUSTRIAL_LIBRARY_VERSION" >> "$GITHUB_ENV"

'''
        text = replace_once(text, pattern, replacement, 'replace v1 industrial validation step')

    old_artifact = '''          industrial=site/'books/industrial-economics'
          assert len(json.load(open(industrial/'manifest.json'))['chapters'])==23
          assert json.load(open(industrial/'questions.json'))['count']==100
          assert len(json.load(open(industrial/'search.json'))['entries'])==150
          assert len(list((site/'assets/industrial-economics-svg').glob('*.svg')))==20
'''
    new_artifact = '''          industrial=site/'books/industrial-economics'
          im=json.load(open(industrial/'manifest.json')); iq=json.load(open(industrial/'questions.json')); isearch=json.load(open(industrial/'search.json'))
          assert im['version']==iq['version']=='2026.07.30-2'
          assert len(im['chapters'])==23 and iq['count']==100 and len(isearch['entries'])==150
          assert len(list((site/'assets/industrial-economics-svg').glob('*.svg')))==20
          assert [x['id'] for x in im['chapters']]==[f'ch{i:02d}' for i in range(20)]+['appendix-a','appendix-b','appendix-c']
          assert [x['id'] for x in iq['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)]
'''
    if old_artifact in text:
        text = text.replace(old_artifact, new_artifact, 1)
    elif "assert im['version']==iq['version']=='2026.07.30-2'" not in text:
        raise AssertionError('cannot locate deployed industrial artifact block')

    after_econ = '          PYTHONPATH=deploy python deploy/qa_econometrics_reaudit_v2.py /tmp/deployed-site "$FINAL_LIBRARY_VERSION"\n'
    industrial_verify = (
        '          PYTHONPATH=deploy python deploy/validate_industrial_economics_v2.py /tmp/deployed-site "$FINAL_LIBRARY_VERSION"\n'
        '          PYTHONPATH=deploy python deploy/qa_industrial_economics_v2.py /tmp/deployed-site "$FINAL_LIBRARY_VERSION"\n'
    )
    if industrial_verify not in text:
        if after_econ not in text:
            raise AssertionError('cannot locate post-deploy econometrics QA line')
        text = text.replace(after_econ, after_econ + industrial_verify, 1)

    recorder_anchor = '          python deploy/record_econometrics_v2_deployment.py _site\n'
    recorder_line = '          python deploy/record_industrial_economics_v2_deployment.py _site\n'
    if recorder_line not in text:
        if recorder_anchor not in text:
            raise AssertionError('cannot locate recorder anchor')
        text = text.replace(recorder_anchor, recorder_anchor + recorder_line, 1)

    git_anchor = '''            docs/books/econometrics/status.md \\
            docs/books/econometrics/qa_report.md
'''
    git_replacement = '''            docs/books/econometrics/status.md \\
            docs/books/econometrics/qa_report.md \\
            docs/books/industrial-economics/status.md \\
            docs/books/industrial-economics/qa_report.md \\
            docs/books/industrial-economics/v2_audit_report.md
'''
    if 'docs/books/industrial-economics/v2_audit_report.md' not in text:
        if git_anchor not in text:
            raise AssertionError('cannot locate git-add document anchor')
        text = text.replace(git_anchor, git_replacement, 1)

    PATH.write_text(text, encoding='utf-8')
    print('INDUSTRIAL_V2_CANONICAL_WORKFLOW_PATCH_OK')


if __name__ == '__main__':
    main()
