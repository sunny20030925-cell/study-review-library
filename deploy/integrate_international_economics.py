#!/usr/bin/env python3
from __future__ import annotations
import base64, contextlib, gzip, hashlib, importlib.util, io, json, os, sys, tempfile
from pathlib import Path

GENERATOR_SHA256='877c4f92f5cb914a6ba0ca900dd9ef6e4c7bbe4ae2eac9db80741ae29a5c5192'
BOOK='international-economics'

def load_module(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise AssertionError(f'cannot load {path}')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def emit_stderr(buf: io.StringIO):
    txt=buf.getvalue()
    if txt: print(txt,end='',file=sys.stderr)

def integrate(site_root: str, expected_before: str) -> str:
    site=Path(site_root); deploy=Path(__file__).resolve().parent
    libp=site/'data/library.json'; pre=json.loads(libp.read_text(encoding='utf-8'))
    if pre['version']!=expected_before: raise AssertionError(f'international pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in [b['id'] for b in pre['books']]: raise AssertionError('international economics already present before integration')
    if len(pre['books'])!=9 or pre['books'][-1]['id']!='macroeconomics': raise AssertionError('international integration requires the nine-book macroeconomics tail')

    parts=sorted(deploy.glob('generate-international-economics.py.gz.b64.part*'))
    if not parts: raise AssertionError('international economics generator parts missing')
    encoded=''.join(p.read_text(encoding='utf-8').strip() for p in parts)
    gz=base64.b64decode(encoded,validate=True)
    if hashlib.sha256(gz).hexdigest()!=GENERATOR_SHA256: raise AssertionError('international generator sha256 mismatch')
    source=gzip.decompress(gz)
    tmpgen=Path(tempfile.gettempdir())/'generate-international-economics.py'
    tmpgen.write_bytes(source)
    compile(source,str(tmpgen),'exec')

    pre_path=Path(tempfile.gettempdir())/'pre-international-economics-library.json'
    pre_path.write_text(json.dumps(pre,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    gen=load_module(tmpgen,'generate_international_economics_runtime')
    fin=load_module(deploy/'finalize_international_economics_library.py','finalize_international_economics_library_runtime')
    qa1=load_module(deploy/'validate_international_economics.py','validate_international_economics_runtime')
    qa2=load_module(deploy/'qa_international_economics.py','qa_international_economics_runtime')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): gen.main(str(site))
    emit_stderr(buf); buf=io.StringIO()
    with contextlib.redirect_stdout(buf): fin.main(str(site),str(pre_path))
    final=json.loads(libp.read_text(encoding='utf-8'))['version']
    emit_stderr(buf)
    old_expected=os.environ.get('EXPECTED_LIBRARY_VERSION'); old_pre=os.environ.get('PRE_LIBRARY_JSON')
    os.environ['EXPECTED_LIBRARY_VERSION']=final; os.environ['PRE_LIBRARY_JSON']=str(pre_path)
    try:
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf): qa1.main(str(site))
        emit_stderr(buf); buf=io.StringIO()
        with contextlib.redirect_stdout(buf): qa2.main(str(site),final)
        emit_stderr(buf)
    finally:
        if old_expected is None: os.environ.pop('EXPECTED_LIBRARY_VERSION',None)
        else: os.environ['EXPECTED_LIBRARY_VERSION']=old_expected
        if old_pre is None: os.environ.pop('PRE_LIBRARY_JSON',None)
        else: os.environ['PRE_LIBRARY_JSON']=old_pre
    return final

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: integrate_international_economics.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
