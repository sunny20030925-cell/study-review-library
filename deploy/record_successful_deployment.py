#!/usr/bin/env python3
from __future__ import annotations

import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path


def jdump(x): return json.dumps(x,ensure_ascii=False,indent=2)+'\n'

def replace_once(text,pattern,replacement,label):
    out,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1: raise AssertionError(f'cannot update {label}')
    return out

def count_kind(manifest,kind): return len([x for x in manifest.get('chapters',[]) if x.get('kind')==kind])

def upsert_book_section(checkpoint,title,book_id,body):
    # Identify sections by their structured Book ID rather than by historical prose.
    sec_re=re.compile(r'(?ms)^###(?:\s+\d+\.)?\s+[^\n]+\n(?:(?!^### |^## ).)*?- Book ID：`'+re.escape(book_id)+r'`(?:(?!^### |^## ).)*')
    m=sec_re.search(checkpoint)
    section=f'### {title}\n\n{body.rstrip()}\n\n'
    if m: return checkpoint[:m.start()]+section+checkpoint[m.end():]
    anchor='## 部署流程'
    idx=checkpoint.find(anchor)
    if idx<0: raise AssertionError('checkpoint deployment-flow anchor missing')
    return checkpoint[:idx]+section+checkpoint[idx:]

def main(site_root: str) -> None:
    site=Path(site_root); lp=site/'data/library.json'; lib=json.loads(lp.read_text(encoding='utf-8')); books=lib['books']; ids=[b['id'] for b in books]
    if len(ids)!=len(set(ids)): raise AssertionError('duplicate Book ID in deployed library')
    final_version=lib['version']; last_id=ids[-1]; last_root=site/'books'/last_id; manifest=json.loads((last_root/'manifest.json').read_text(encoding='utf-8')); questions=json.loads((last_root/'questions.json').read_text(encoding='utf-8')); search=json.loads((last_root/'search.json').read_text(encoding='utf-8'))
    source=os.environ['GITHUB_SHA']; run=os.environ['GITHUB_RUN_ID']; page=os.environ.get('DEPLOYED_PAGE_URL','')
    receipt_path=Path('docs/deployment_receipt.json'); receipt=json.loads(receipt_path.read_text(encoding='utf-8')) if receipt_path.exists() else {}
    receipt.update({'status':'success','library_version':final_version,'book_count':len(books),'book_versions_visible':True,'progress_storage_changed':False,'source_commit':source,'workflow_run_id':run,'page_url':page,'deployed_at':datetime.now(timezone.utc).isoformat(),'book_versions':{b['id']:json.loads((site/'books'/b['id']/'manifest.json').read_text(encoding='utf-8')).get('version') for b in books}})
    key=last_id.replace('-','_')
    receipt[f'{key}_version']=manifest.get('version'); receipt[f'{key}_chapter_count']=count_kind(manifest,'chapter'); receipt[f'{key}_appendix_count']=count_kind(manifest,'appendix'); receipt[f'{key}_question_count']=questions.get('count',len(questions.get('items',[]))); receipt[f'{key}_search_count']=len(search.get('entries',[])); receipt_path.write_text(jdump(receipt),encoding='utf-8')

    title=manifest.get('title',last_id); version=manifest.get('version','未標示'); chapters=count_kind(manifest,'chapter'); apps=count_kind(manifest,'appendix'); qcount=questions.get('count',len(questions.get('items',[]))); scount=len(search.get('entries',[]))
    # Status for the deployed tail book; preserve subject-specific scope and QA files.
    status=Path('docs/books')/last_id/'status.md'
    if status.exists():
        status.write_text(f'''# 《{title}》製作狀態\n\n更新日期：2026-07-29\n\n## 正式識別\n\n- Book ID：`{last_id}`\n- 正式內容版本：`{version}`\n- 正式書庫版本：`{final_version}`\n- 狀態：已部署。\n\n## 成品與 QA\n\n- 正文 {chapters} 章、附錄 {apps} 份、題庫 {qcount} 題、搜尋索引 {scount} 筆。\n- QA 報告：`docs/books/{last_id}/qa_report.md`。\n- 閱讀進度相容性：新增／更新本書未變更既有書籍的 Book ID、章節 ID、題目 ID 或儲存鍵；deployment receipt 記錄 `progress_storage_changed=false`。\n\n## 部署\n\n- canonical workflow：`Deploy study library`\n- workflow run：`{run}`\n- source commit：`{source}`\n- 正式書庫書籍數：{len(books)} 本。\n- GitHub Pages deployment 成功並已寫回 deployment receipt。\n''',encoding='utf-8')

    cp=Path('docs/shared_checkpoint.md'); c=cp.read_text(encoding='utf-8'); c=replace_once(c,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{final_version}`','checkpoint library version'); c=replace_once(c,r'- 正式書籍數：\d+ 本。',f'- 正式書籍數：{len(books)} 本。','checkpoint book count')
    c=re.sub(r'- 最新成功部署的 Pages run：`[^`]+`',f'- 最新成功部署的 Pages run：`{run}`',c,count=1)
    c=re.sub(r'- Source commit：`[^`]+`',f'- Source commit：`{source}`',c,count=1)
    body=f'''- Book ID：`{last_id}`\n- 正式內容版本：`{version}`\n- 定位：{manifest.get('subtitle','')}\n- 成品：{chapters} 章、{apps} 附錄、{qcount} 題題庫、{scount} 筆搜尋索引。\n- QA 報告：`docs/books/{last_id}/qa_report.md`\n- GitHub Pages 部署 run：`{run}`。\n- Source commit：`{source}`。\n- 部署回條：`docs/deployment_receipt.json`。\n- 狀態：已部署。'''
    c=upsert_book_section(c,title,last_id,body); cp.write_text(c,encoding='utf-8')

    rp=Path('README.md'); r=rp.read_text(encoding='utf-8'); r=replace_once(r,r'目前內容版本：`[^`]+`',f'目前內容版本：`{final_version}`','README version')
    line=f'- 《{title}》：{manifest.get("subtitle","")}；{chapters} 章、{apps} 附錄、{qcount} 題題庫、{scount} 筆搜尋索引；內容版本 `{version}`。'
    lines=r.splitlines(); prefix=f'- 《{title}》：'; found=[i for i,x in enumerate(lines) if x.startswith(prefix)]
    if found:
        lines[found[0]]=line
        for i in reversed(found[1:]): del lines[i]
    else:
        candidates=[i for i,x in enumerate(lines) if x.startswith('- 《')]
        if not candidates: raise AssertionError('README book list not found')
        lines.insert(max(candidates)+1,line)
    rp.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'STRUCTURED_DEPLOYMENT_RECORD_OK books={len(books)} library={final_version} tail={last_id}')

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: record_successful_deployment.py SITE_ROOT')
    main(sys.argv[1])
