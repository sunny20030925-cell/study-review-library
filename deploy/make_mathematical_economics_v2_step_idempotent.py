#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

PATH=Path('.github/workflows/deploy-pages.yml')

OLD_PRE="""          python - <<'PY'\n          import json\n          d=json.load(open('_site/data/library.json'))\n          ids=[b['id'] for b in d['books']]\n          assert 'mathematical-economics' not in ids, ids\n          json.dump(ids,open('/tmp/pre-math-v2-ids.json','w'))\n          print('MATHEMATICAL_ECONOMICS_V2_BASE',d['version'],len(ids),ids[-1])\n          PY\n\n          BEFORE=\"$(python -c \"import json;print(json.load(open('_site/data/library.json'))['version'])\")\"\n          FINAL_LIBRARY_VERSION=\"$(PYTHONPATH=deploy python deploy/integrate_mathematical_economics_v2.py _site \"$BEFORE\")\"\n          test -n \"$FINAL_LIBRARY_VERSION\"\n"""

NEW_PRE="""          python - <<'PY'\n          import json\n          d=json.load(open('_site/data/library.json'))\n          ids=[b['id'] for b in d['books']]\n          assert ids.count('mathematical-economics') in {0,1}, ids\n          json.dump(ids,open('/tmp/pre-math-v2-ids.json','w'))\n          print('MATHEMATICAL_ECONOMICS_V2_BASE',d['version'],len(ids),ids[-1], 'already_present=' + str('mathematical-economics' in ids).lower())\n          PY\n\n          BEFORE=\"$(python -c \"import json;print(json.load(open('_site/data/library.json'))['version'])\")\"\n          if python - <<'PY'\n          import json,sys\n          ids=[b['id'] for b in json.load(open('_site/data/library.json'))['books']]\n          sys.exit(0 if 'mathematical-economics' in ids else 1)\n          PY\n          then\n            FINAL_LIBRARY_VERSION=\"$BEFORE\"\n          else\n            FINAL_LIBRARY_VERSION=\"$(PYTHONPATH=deploy python deploy/integrate_mathematical_economics_v2.py _site \"$BEFORE\")\"\n          fi\n          test -n \"$FINAL_LIBRARY_VERSION\"\n"""

OLD_POST="""          pre=json.load(open('/tmp/pre-math-v2-ids.json'))\n          assert ids==pre+['mathematical-economics'], (pre,ids)\n          assert lib['version']==os.environ['FINAL_LIBRARY_VERSION']\n"""

NEW_POST="""          pre=json.load(open('/tmp/pre-math-v2-ids.json'))\n          if 'mathematical-economics' in pre:\n              assert ids==pre, (pre,ids)\n          else:\n              assert ids==pre+['mathematical-economics'], (pre,ids)\n          assert ids.count('mathematical-economics')==1\n          assert lib['version']==os.environ['FINAL_LIBRARY_VERSION']\n"""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n=text.count(old)
    if n!=1:
        raise AssertionError(f'{label}: expected 1 match, got {n}')
    return text.replace(old,new,1)


def main() -> None:
    text=PATH.read_text(encoding='utf-8')
    if 'already_present=' in text and "if 'mathematical-economics' in pre:" in text:
        print('MATHEMATICAL_ECONOMICS_V2_IDEMPOTENCY_ALREADY_PRESENT')
        return
    text=replace_once(text,OLD_PRE,NEW_PRE,'math pre/integration block')
    text=replace_once(text,OLD_POST,NEW_POST,'math post registry block')
    PATH.write_text(text,encoding='utf-8')
    print('MATHEMATICAL_ECONOMICS_V2_IDEMPOTENCY_PATCHED')


if __name__=='__main__':
    main()
