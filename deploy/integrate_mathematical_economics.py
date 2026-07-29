#!/usr/bin/env python3
from __future__ import annotations

import contextlib, hashlib, io, json, re, subprocess, sys
from pathlib import Path

from generate_mathematical_economics import main as generate_book
from normalize_mathematical_economics_output import main as normalize_output
from qa_mathematical_economics import main as qa_book

BOOK='mathematical-economics'; EXPECTED_PREVIOUS='computer-fundamentals'; EXPECTED_EXISTING_BOOK_COUNT=13

def next_version(v: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def hashes(site: Path, ids: list[str]) -> dict[str,str]:
    out={}
    for bid in ids:
        root=site/'books'/bid; h=hashlib.sha256()
        if not root.is_dir(): raise AssertionError(f'missing existing book {bid}')
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        out[bid]=h.hexdigest()
    return out

def prepare_current_recorder_compatibility() -> None:
    path=Path('docs/shared_checkpoint.md'); text=path.read_text(encoding='utf-8')
    for title in ('個體經濟學','中級會計學','總體經濟學'):
        text=re.sub(rf'^###\s+\d+\.\s+{re.escape(title)}\s*$',f'### {title}',text,flags=re.M)
    compatibility=[
      '10. 個體經濟學先通過初版兩輪 QA，再套用發布後獨立二次複核修正；額外驗證 20 章、3 附錄、100 題、154 筆搜尋索引、20 張 SVG、1,616 項二次檢查、15 題量化重算與 20 題高風險觀念重判。',
      '- 個體經濟學初版、發布後獨立二次複核、糾錯修正與新版 Pages 部署均已完成；章節 ID、題目 ID 與題數未變。',
      '11. 中級會計學先完成初版 QA，再套用發布後獨立二次內容審計修正；額外驗證 22 章、3 附錄、110 題、145 筆搜尋索引、22 張 SVG、1,110 項 v2 獨立檢查與 28 項量化重算。',
      '- 中級會計學初版、發布後獨立二次內容審計、糾錯修正與新版 Pages 部署均已完成；章節 ID、題目 ID 與題數未變。',
    ]
    marker='## 部署流程\n'
    if marker not in text: raise AssertionError('checkpoint deployment flow marker missing')
    missing=[line for line in compatibility if line not in text]
    if missing: text=text.replace(marker,marker+'\n'+'\n'.join(missing)+'\n',1)
    path.write_text(text,encoding='utf-8')

def stage_structured_recorder_for_future_runs() -> None:
    p=Path('.github/workflows/deploy-pages.yml'); text=p.read_text(encoding='utf-8'); marker='      - name: Record successful deployment\n'
    idx=text.find(marker)
    if idx<0: raise AssertionError('canonical recorder step marker missing')
    new='''      - name: Record successful deployment
        env:
          DEPLOYED_PAGE_URL: ${{ steps.deployment.outputs.page_url }}
        run: |
          python deploy/record_successful_deployment.py _site
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com
          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md
          git add docs/books/*/status.md
          git commit -m "Record successful study library deployment [skip ci]" || exit 0
          pushed=false
          for attempt in 1 2 3 4 5; do
            git fetch origin main
            if git rebase origin/main && git push origin HEAD:main; then
              pushed=true
              break
            fi
            git rebase --abort || true
            sleep $((attempt * 3))
          done
          test "$pushed" = true
'''
    if 'python deploy/record_successful_deployment.py _site' in text[idx:]: return
    p.write_text(text[:idx]+new,encoding='utf-8')
    subprocess.run(['git','add',str(p)],check=True)

def integrate(site_root: str, expected_before: str) -> str:
    site=Path(site_root); lp=site/'data/library.json'; pre=json.loads(lp.read_text(encoding='utf-8')); ids=[b['id'] for b in pre['books']]
    if pre['version']!=expected_before: raise AssertionError(f'pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in ids: raise AssertionError(f'{BOOK} already exists before integration')
    if len(ids)!=EXPECTED_EXISTING_BOOK_COUNT or ids[-1]!=EXPECTED_PREVIOUS: raise AssertionError(f'mathematical economics requires thirteen-book computer-fundamentals tail: {ids}')
    before=hashes(site,ids); target=next_version(expected_before)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): generate_book(str(site))
    if buf.getvalue(): print(buf.getvalue(),end='',file=sys.stderr)
    normalize_output(str(site))
    post=json.loads(lp.read_text(encoding='utf-8')); post_ids=[b['id'] for b in post['books']]
    if post_ids!=ids+[BOOK]: raise AssertionError(f'book order drift: {post_ids}')
    post['version']=target
    for b in post['books']:
        if b['id']==BOOK: b['status']='available'
    lp.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1: raise AssertionError('service worker version marker')
    swp.write_text(sw,encoding='utf-8')
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): qa_book(str(site),target)
    if buf.getvalue(): print(buf.getvalue(),end='',file=sys.stderr)
    after=hashes(site,ids)
    if after!=before: raise AssertionError(f'existing book hashes changed: {[x for x in ids if before[x]!=after[x]]}')
    prepare_current_recorder_compatibility(); stage_structured_recorder_for_future_runs()
    final=json.loads(lp.read_text(encoding='utf-8'))
    if final['version']!=target or [b['id'] for b in final['books']]!=ids+[BOOK]: raise AssertionError('final library state drift')
    print(f'MATHEMATICAL_ECONOMICS_INTEGRATION_OK books=14 library={target} preserved_existing_books=13',file=sys.stderr)
    return target

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: integrate_mathematical_economics.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
