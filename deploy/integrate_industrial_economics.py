#!/usr/bin/env python3
from __future__ import annotations
import contextlib,copy,hashlib,io,json,re,sys
from pathlib import Path
from generate_industrial_economics import main as generate
from qa_industrial_economics import main as qa2
from validate_industrial_economics import main as qa1
BOOK='industrial-economics'; VERSION='2026.07.29-1'; TEMPLATE_BOOK='money-banking'

def next_version(v:str)->str:
 m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
 if not m: raise AssertionError(f'invalid library version: {v}')
 return f'{m.group(1)}-{int(m.group(2))+1}'

def book_hashes(site:Path,ids:list[str])->dict[str,str]:
 out={}
 for bid in ids:
  root=site/'books'/bid
  if not root.is_dir(): raise AssertionError(f'missing existing book directory: {bid}')
  h=hashlib.sha256()
  for p in sorted(x for x in root.rglob('*') if x.is_file()): h.update(p.relative_to(root).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
  out[bid]=h.hexdigest()
 return out

def emit(buf:io.StringIO):
 if buf.getvalue(): print(buf.getvalue(),end='',file=sys.stderr)

def integrate(site_root:str,expected_before:str)->str:
 site=Path(site_root); lp=site/'data/library.json'; pre=json.loads(lp.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in pre['books']]
 if pre['version']!=expected_before: raise AssertionError(f'pre-version expected {expected_before}, got {pre["version"]}')
 if BOOK in pre_ids: raise AssertionError(f'{BOOK} already present')
 if TEMPLATE_BOOK not in pre_ids: raise AssertionError('money-banking template book missing')
 before=book_hashes(site,pre_ids); target=next_version(expected_before)
 # Legacy generator uses the stable 12-book money-banking tail as a schema template. Narrow only the registry temporarily;
 # no existing book directory or asset is removed, then restore the full formal registry plus the new book.
 money_index=pre_ids.index(TEMPLATE_BOOK)
 core_books=copy.deepcopy(pre['books'][:money_index+1])
 if len(core_books)!=12 or core_books[-1]['id']!=TEMPLATE_BOOK: raise AssertionError(f'unexpected stable template segment: {[b["id"] for b in core_books]}')
 staged=copy.deepcopy(pre); staged['books']=core_books; lp.write_text(json.dumps(staged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 buf=io.StringIO()
 try:
  with contextlib.redirect_stdout(buf): generate(str(site))
 finally:
  emit(buf)
 generated=json.loads(lp.read_text(encoding='utf-8')); new=[b for b in generated['books'] if b.get('id')==BOOK]
 if len(new)!=1: raise AssertionError('generator did not produce exactly one industrial economics registry entry')
 final=copy.deepcopy(pre); final['version']=target; final['books']=copy.deepcopy(pre['books'])+[new[0]]; final['books'][-1]['status']='available';
 if 'version' in final['books'][-1]: final['books'][-1]['version']=VERSION
 lp.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
 if n!=1: raise AssertionError('service-worker version marker'); swp.write_text(sw,encoding='utf-8')
 # Keep write outside the one-line if for Python clarity.
 swp.write_text(sw,encoding='utf-8')
 buf=io.StringIO();
 with contextlib.redirect_stdout(buf): qa1(str(site),target)
 emit(buf); buf=io.StringIO()
 with contextlib.redirect_stdout(buf): qa2(str(site),target)
 emit(buf)
 after=book_hashes(site,pre_ids)
 if after!=before: raise AssertionError(f'existing book content changed: {[bid for bid in pre_ids if before.get(bid)!=after.get(bid)]}')
 check=json.loads(lp.read_text(encoding='utf-8')); check_ids=[b['id'] for b in check['books']]
 if check['version']!=target or check_ids!=pre_ids+[BOOK]: raise AssertionError('final library state drift')
 print(f'INDUSTRIAL_ECONOMICS_INTEGRATION_OK books={len(check_ids)} library={target} preserved_existing_books={len(pre_ids)}',file=sys.stderr); return target

if __name__=='__main__':
 if len(sys.argv)!=3: raise SystemExit('usage: integrate_industrial_economics.py SITE_ROOT EXPECTED_BEFORE')
 print(integrate(sys.argv[1],sys.argv[2]))
