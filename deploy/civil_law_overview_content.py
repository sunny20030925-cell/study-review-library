from __future__ import annotations

# 法規基準：2026-07-29。第 166-1 條施行日尚待另定。
from civil_law_overview_content_a import CHAPTERS_A
from civil_law_overview_content_b import CHAPTERS_B
from civil_law_overview_content_c import CHAPTERS_C

CHAPTERS = CHAPTERS_A + CHAPTERS_B + CHAPTERS_C
assert len(CHAPTERS) == 20
assert [c['id'] for c in CHAPTERS] == [f'ch{i:02d}' for i in range(20)]
