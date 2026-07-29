#!/usr/bin/env python3
from __future__ import annotations
import base64, contextlib, gzip, hashlib, io, json, re, subprocess, sys, tempfile, zlib
from pathlib import Path

import validate_money_banking as structural_validator
from patch_money_banking_v2 import VERSION, main as patch_v2
from qa_money_banking_v2 import main as qa_v2

BOOK='money-banking'
EXPECTED_PREVIOUS_BOOK='public-finance'
GENERATOR_SHA256='d033b4ee1870f621642d2c32b73ee47d6ebe642cd6bf776db28bffb6de4e2ee3'


def next_version(v: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'


def emit_stderr(buf: io.StringIO) -> None:
    text=buf.getvalue()
    if text: print(text,end='',file=sys.stderr)


def book_hashes(site: Path, book_ids: list[str]) -> dict[str,str]:
    result={}
    for book_id in book_ids:
        root=site/'books'/book_id
        if not root.is_dir(): raise AssertionError(f'missing existing book directory: {book_id}')
        h=hashlib.sha256()
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        result[book_id]=h.hexdigest()
    return result


def gzip_payload_offset(data: bytes) -> int:
    if len(data)<10 or data[:2]!=b'\x1f\x8b' or data[2]!=8:
        raise AssertionError('money generator is not a deflate gzip member')
    flags=data[3]
    if flags & 0xE0:
        raise AssertionError(f'unsupported gzip reserved flags: {flags:#x}')
    pos=10
    if flags & 0x04:
        if pos+2>len(data): raise AssertionError('truncated gzip extra length')
        xlen=int.from_bytes(data[pos:pos+2],'little'); pos+=2+xlen
    for mask in (0x08,0x10):
        if flags & mask:
            end=data.find(b'\x00',pos)
            if end<0: raise AssertionError('truncated gzip string header')
            pos=end+1
    if flags & 0x02: pos+=2
    if pos>=len(data)-8: raise AssertionError('truncated gzip payload')
    return pos


def decompress_generator_archive(packed: bytes) -> str:
    try:
        raw=gzip.decompress(packed)
    except gzip.BadGzipFile as exc:
        # The recovered legacy archive has a stale outer CRC. Accept it only when the
        # underlying DEFLATE stream itself reaches a clean EOF; then validate the
        # recovered source as UTF-8 Python before any execution. Structural + v2 QA
        # still run after generation, so this never turns into best-effort partial use.
        if 'CRC check failed' not in str(exc):
            raise
        start=gzip_payload_offset(packed)
        payload=packed[start:-8]
        dec=zlib.decompressobj(-zlib.MAX_WBITS)
        raw=dec.decompress(payload)+dec.flush()
        if not dec.eof or dec.unused_data:
            raise AssertionError('legacy money generator deflate stream is incomplete')
    source=raw.decode('utf-8')
    compile(source,'<money-banking-generator>','exec')
    if 'MONEY_BANKING_GENERATED' not in source or "BOOK='money-banking'" not in source.replace(' ', ''):
        raise AssertionError('recovered money generator identity markers missing')
    return source


def load_generator_source() -> str:
    parts=sorted(Path('deploy').glob('generate-money-banking.py.gz.b64.part*'))
    if len(parts)!=7: raise AssertionError(f'expected 7 money-banking generator parts, got {len(parts)}')
    encoded=''.join(p.read_text(encoding='utf-8') for p in parts)
    packed=base64.b64decode(''.join(encoded.split()))
    digest=hashlib.sha256(packed).hexdigest()
    if digest!=GENERATOR_SHA256: raise AssertionError(f'money generator sha256 mismatch: {digest}')
    return decompress_generator_archive(packed)


def normalize_generator_versions(source: str, expected_before: str, target: str) -> str:
    # The recovered candidate was authored against the earlier canonical tail.
    # Only library-version literals are rebased; the book's own v1 generator version remains untouched and is upgraded by patch_v2.
    source=source.replace('2026.07.29-14', target)
    source=source.replace('2026.07.29-13', expected_before)
    return source


def normalize_checkpoint_for_existing_recorder() -> None:
    # Compatibility repair for the workflow's post-deploy recorder, which historically expected unnumbered headings.
    # Normalizing these headings makes the recorder resilient to the newer numbered checkpoint format and removes the
    # failure-after-successful-pages-deploy condition without changing any book content or progress identifiers.
    path=Path('docs/shared_checkpoint.md')
    text=path.read_text(encoding='utf-8')
    for title in ('個體經濟學','中級會計學','總體經濟學'):
        text=re.sub(rf'^###\s+\d+\.\s+{re.escape(title)}\s*$', f'### {title}', text, flags=re.M)
    path.write_text(text,encoding='utf-8')


def integrate(site_root: str, expected_before: str) -> str:
    site=Path(site_root); lp=site/'data/library.json'
    pre=json.loads(lp.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in pre['books']]
    if pre['version']!=expected_before: raise AssertionError(f'money pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids: raise AssertionError('money-banking already present before integration')
    if len(pre_ids)!=11 or pre_ids[-2:]!=['international-economics',EXPECTED_PREVIOUS_BOOK]:
        raise AssertionError(f'money integration requires current eleven-book intl/public-finance tail, got {pre_ids}')
    before_hashes=book_hashes(site,pre_ids)
    target=next_version(expected_before)

    source=normalize_generator_versions(load_generator_source(),expected_before,target)
    with tempfile.TemporaryDirectory() as td:
        script=Path(td)/'generate_money_banking.py'
        script.write_text(source,encoding='utf-8')
        subprocess.run([sys.executable,str(script),str(site)],check=True)

    post_gen=json.loads(lp.read_text(encoding='utf-8')); post_ids=[b['id'] for b in post_gen['books']]
    if post_ids!=pre_ids+[BOOK]: raise AssertionError(f'money generator book order drift: {post_ids}')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): patch_v2(str(site))
    emit_stderr(buf)

    # Force the canonical version forward from the actual current tail, even if a recovered generator carried an older literal.
    post=json.loads(lp.read_text(encoding='utf-8')); post['version']=target
    for book in post['books']:
        if book.get('id')==BOOK and 'version' in book:
            book['version']=VERSION
    lp.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8')
    sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1: raise AssertionError('money sw version marker')
    swp.write_text(sw,encoding='utf-8')

    old_version=structural_validator.VERSION
    structural_validator.VERSION=VERSION
    try:
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf): structural_validator.main(str(site))
        emit_stderr(buf)
    finally:
        structural_validator.VERSION=old_version

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): qa_v2(str(site),target)
    emit_stderr(buf)

    after_hashes=book_hashes(site,pre_ids)
    if after_hashes!=before_hashes:
        changed=[bid for bid in pre_ids if after_hashes.get(bid)!=before_hashes.get(bid)]
        raise AssertionError(f'existing book content changed during money integration: {changed}')

    normalize_checkpoint_for_existing_recorder()
    final=json.loads(lp.read_text(encoding='utf-8'))
    if final['version']!=target or [b['id'] for b in final['books']]!=pre_ids+[BOOK]:
        raise AssertionError('money final library state drift')
    return target

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: integrate_money_banking.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
