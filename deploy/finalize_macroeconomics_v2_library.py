#!/usr/bin/env python3
from __future__ import annotations
import contextlib,io,json,re,sys
from pathlib import Path
BOOK='macroeconomics'

def next_version(v):
 m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
 if not m: raise AssertionError(v)
 return f'{m.group(1)}-{int(m.group(2))+1}'

def emit_stderr(buf):
 text=buf.getvalue()
 if text: print(text,end='',file=sys.stderr)

def main(site_root, expected_before):
 site=Path(site_root); lp=site/'data/library.json'; d=json.loads(lp.read_text())
 if d['version']!=expected_before: raise AssertionError(f'expected {expected_before}, got {d["version"]}')
 if [x['id'] for x in d['books']].count(BOOK)!=1: raise AssertionError('macro book count')
 macro_version=next_version(expected_before); d['version']=macro_version
 lp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 swp=site/'sw.js'; sw=swp.read_text(); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{macro_version}';",sw,count=1)
 if n!=1: raise AssertionError('sw version marker')
 swp.write_text(sw,encoding='utf-8')
 # Canonical serialized tail:
 # macroeconomics -> international economics v1 -> public finance -> international economics v2
 # -> money & banking v2 -> computer fundamentals v1.
 # Keep stdout clean because the workflow captures this script's single final-version line.
 from integrate_international_economics import integrate as integrate_international
 from integrate_public_finance import integrate as integrate_public_finance
 from patch_international_economics_v2 import main as patch_international_v2
 from finalize_international_economics_v2_library import main as finalize_international_v2
 from qa_international_economics_v2 import main as qa_international_v2
 from integrate_money_banking import integrate as integrate_money_banking
 from integrate_computer_fundamentals import integrate as integrate_computer_fundamentals
 international_version=integrate_international(site_root,macro_version)
 public_finance_version=integrate_public_finance(site_root,international_version)
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf): patch_international_v2(site_root)
 emit_stderr(buf)
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf): finalize_international_v2(site_root,public_finance_version)
 international_v2_version=json.loads(lp.read_text(encoding='utf-8'))['version']
 emit_stderr(buf)
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf): qa_international_v2(site_root,international_v2_version)
 emit_stderr(buf)
 money_version=integrate_money_banking(site_root,international_v2_version)
 final_version=integrate_computer_fundamentals(site_root,money_version)
 print(final_version)
if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: finalize_macroeconomics_v2_library.py SITE_ROOT EXPECTED_BEFORE')
 main(sys.argv[1],sys.argv[2])
