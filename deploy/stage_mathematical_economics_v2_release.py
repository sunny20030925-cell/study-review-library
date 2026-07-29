#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

PATH=Path('.github/workflows/deploy-pages.yml')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old)!=1:
        raise AssertionError(f'{label}: expected exactly one marker, got {text.count(old)}')
    return text.replace(old,new,1)


def replace_last(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise AssertionError(f'{label}: marker missing')
    head,tail=text.rsplit(old,1)
    return head+new+tail


def main() -> None:
    text=PATH.read_text(encoding='utf-8')
    if 'Integrate mathematical economics v2 audited release' in text:
        print('MATHEMATICAL_ECONOMICS_V2_CANONICAL_STAGE_ALREADY_PRESENT')
        return

    math_step=r'''      - name: Integrate mathematical economics v2 audited release
        run: |
          set -euo pipefail
          python -m py_compile \
            deploy/mathematical_economics_content.py \
            deploy/mathematical_economics_questions.py \
            deploy/generate_mathematical_economics.py \
            deploy/mathematical_economics_v2_corrections.py \
            deploy/mathematical_economics_v2_enrichment.py \
            deploy/mathematical_economics_v2_questions.py \
            deploy/generate_mathematical_economics_v2.py \
            deploy/qa_mathematical_economics_v2.py \
            deploy/integrate_mathematical_economics_v2.py \
            deploy/record_mathematical_economics_v2_deployment.py

          python - <<'PY'
          import json
          d=json.load(open('_site/data/library.json'))
          ids=[b['id'] for b in d['books']]
          assert 'mathematical-economics' not in ids, ids
          json.dump(ids,open('/tmp/pre-math-v2-ids.json','w'))
          print('MATHEMATICAL_ECONOMICS_V2_BASE',d['version'],len(ids),ids[-1])
          PY

          BEFORE="$(python -c "import json;print(json.load(open('_site/data/library.json'))['version'])")"
          FINAL_LIBRARY_VERSION="$(PYTHONPATH=deploy python deploy/integrate_mathematical_economics_v2.py _site "$BEFORE")"
          test -n "$FINAL_LIBRARY_VERSION"
          QA_LINE="$(PYTHONPATH=deploy python deploy/qa_mathematical_economics_v2.py _site "$FINAL_LIBRARY_VERSION" | tail -n 1)"
          echo "$QA_LINE"
          MATHEMATICAL_ECONOMICS_V2_QA_CHECKS="$(printf '%s\n' "$QA_LINE" | sed -n 's/^MATHEMATICAL_ECONOMICS_V2_QA_OK checks=\([0-9][0-9]*\).*/\1/p')"
          MATHEMATICAL_ECONOMICS_V2_NUMERIC_RECHECKS="$(printf '%s\n' "$QA_LINE" | grep -oE 'quantitative_rechecks=[0-9]+' | head -n 1 | cut -d= -f2)"
          MATHEMATICAL_ECONOMICS_V2_LOGIC_GATES="$(printf '%s\n' "$QA_LINE" | grep -oE 'high_risk_logic_gates=[0-9]+' | head -n 1 | cut -d= -f2)"
          test "$MATHEMATICAL_ECONOMICS_V2_QA_CHECKS" = "855"
          test "$MATHEMATICAL_ECONOMICS_V2_NUMERIC_RECHECKS" = "23"
          test "$MATHEMATICAL_ECONOMICS_V2_LOGIC_GATES" = "10"

          export FINAL_LIBRARY_VERSION MATHEMATICAL_ECONOMICS_V2_QA_CHECKS MATHEMATICAL_ECONOMICS_V2_NUMERIC_RECHECKS MATHEMATICAL_ECONOMICS_V2_LOGIC_GATES
          echo "FINAL_LIBRARY_VERSION=$FINAL_LIBRARY_VERSION" >> "$GITHUB_ENV"
          echo "MATHEMATICAL_ECONOMICS_V2_QA_CHECKS=$MATHEMATICAL_ECONOMICS_V2_QA_CHECKS" >> "$GITHUB_ENV"
          echo "MATHEMATICAL_ECONOMICS_V2_NUMERIC_RECHECKS=$MATHEMATICAL_ECONOMICS_V2_NUMERIC_RECHECKS" >> "$GITHUB_ENV"
          echo "MATHEMATICAL_ECONOMICS_V2_LOGIC_GATES=$MATHEMATICAL_ECONOMICS_V2_LOGIC_GATES" >> "$GITHUB_ENV"

          python - <<'PY'
          import json,os
          from pathlib import Path
          site=Path('_site')
          lib=json.load(open(site/'data/library.json'))
          ids=[b['id'] for b in lib['books']]
          pre=json.load(open('/tmp/pre-math-v2-ids.json'))
          assert ids==pre+['mathematical-economics'], (pre,ids)
          assert lib['version']==os.environ['FINAL_LIBRARY_VERSION']
          root=site/'books/mathematical-economics'
          m=json.load(open(root/'manifest.json')); q=json.load(open(root/'questions.json')); s=json.load(open(root/'search.json'))
          assert m['version']==q['version']=='2026.07.30-2'
          assert len(m['chapters'])==23 and q['count']==100 and len(s['entries'])==150
          assert [x['id'] for x in m['chapters']]==[f'ch{i:02d}' for i in range(20)]+['appendix-a','appendix-b','appendix-c']
          assert [x['id'] for x in q['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)]
          assert len(list((site/'assets/mathematical-economics-svg').glob('*.svg')))==20
          print('MATHEMATICAL_ECONOMICS_V2_FORMAL_CANDIDATE_OK',lib['version'],len(ids))
          PY
          node --check _site/app.js
          node --check _site/sw.js

'''
    marker='      - uses: actions/upload-pages-artifact@v3'
    text=replace_once(text,marker,math_step+marker,'upload insertion')

    old="          assert ids[-1]=='industry-trade' and ids.count('industry-trade')==1"
    new="          assert ids[-2:]==['industry-trade','mathematical-economics'] and ids.count('industry-trade')==1 and ids.count('mathematical-economics')==1"
    text=replace_last(text,old,new,'deployed tail')

    print_marker="          print('DEPLOYED_ARTIFACT_RECHECK_OK',lib['version'],len(ids),'computer-fundamentals=2026.07.30-2')"
    math_verify=r'''          mathroot=site/'books/mathematical-economics'
          mm=json.load(open(mathroot/'manifest.json')); mq=json.load(open(mathroot/'questions.json')); ms=json.load(open(mathroot/'search.json'))
          assert mm['version']==mq['version']=='2026.07.30-2'
          assert len(mm['chapters'])==23 and mq['count']==100 and len(ms['entries'])==150
          assert [x['id'] for x in mm['chapters']]==[f'ch{i:02d}' for i in range(20)]+['appendix-a','appendix-b','appendix-c']
          assert [x['id'] for x in mq['items']]==[f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1,6)]
          assert len(list((site/'assets/mathematical-economics-svg').glob('*.svg')))==20
          print('DEPLOYED_ARTIFACT_RECHECK_OK',lib['version'],len(ids),'mathematical-economics=2026.07.30-2')'''
    text=replace_once(text,print_marker,math_verify,'artifact verifier')

    qa_marker='          echo "PAGES_ARTIFACT_ID=$ARTIFACT_ID" >> "$GITHUB_ENV"'
    qa_insert='          PYTHONPATH=deploy python deploy/qa_mathematical_economics_v2.py /tmp/deployed-site "$FINAL_LIBRARY_VERSION"\n'
    text=replace_once(text,qa_marker,qa_insert+qa_marker,'post-deploy math QA')

    recorder_marker='          git config user.name github-actions[bot]'
    recorder_insert='          PYTHONPATH=deploy python deploy/record_mathematical_economics_v2_deployment.py _site\n'
    text=replace_once(text,recorder_marker,recorder_insert+recorder_marker,'recorder invocation')

    add_marker='            docs/books/computer-fundamentals/qa_report.md'
    add_new='            docs/books/computer-fundamentals/qa_report.md \\\n            docs/books/mathematical-economics/status.md \\\n            docs/books/mathematical-economics/qa_report.md'
    text=replace_once(text,add_marker,add_new,'git add math docs')

    PATH.write_text(text,encoding='utf-8')
    print('MATHEMATICAL_ECONOMICS_V2_CANONICAL_STAGE_OK')


if __name__=='__main__':
    main()
