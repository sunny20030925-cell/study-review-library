from __future__ import annotations

import re
from pathlib import Path

# The chapter source is intentionally kept as a readable data file rather than an
# importable Python module. Escape LaTeX control words before compiling it so Python
# never interprets \t, \r, \u, \a, etc. as string escapes.
raw_path=Path(__file__).with_name('money_banking_content.raw')
source=raw_path.read_text(encoding='utf-8')
source=re.sub(r'\\([A-Za-z]+)',r'\\\\\1',source)
namespace={}
exec(compile(source,str(raw_path),'exec'),namespace)
CHAPTERS=namespace['CHAPTERS']

if len(CHAPTERS)!=20 or [c['id'] for c in CHAPTERS] != [f'ch{i:02d}' for i in range(20)]:
    raise AssertionError('money banking chapter source integrity check failed')
