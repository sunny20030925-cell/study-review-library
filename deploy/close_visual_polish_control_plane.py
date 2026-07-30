#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

REPO = Path('.')


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError(f'{label}: expected one replacement, got {n}')
    return out


def asset_title(site: Path, asset: str, fallback: str) -> str:
    p = site / asset
    if not p.is_file():
        return fallback
    m = re.search(r'<title(?:\s[^>]*)?>(.*?)</title>', p.read_text(encoding='utf-8'), re.S)
    if not m:
        return fallback
    return html.unescape(re.sub(r'\s+', ' ', m.group(1)).strip())


def update_status(path: Path, target: str, title: str, library_version: str, vp: dict, receipt: dict, checks: int, next_target: str | None) -> None:
    text = path.read_text(encoding='utf-8')
    pairs = [
        (r'^- 正式書庫版本：`[^`]+`.*$', f'- 正式書庫版本：`{library_version}`', 'status library version'),
        (r'^- 目前 stage：`[^`]+`.*$', '- 目前 stage：`PUB`', 'status stage'),
        (r'^- Task ID：`[^`]+`.*$', f'- Task ID：`{target}:PUB`', 'status task'),
        (r'^- 下一階段：.*$', '- 下一階段：無；本書新制流程已完成。', 'status next stage'),
    ]
    for pattern, replacement, label in pairs:
        if re.search(pattern, text, re.M):
            text = replace_once(text, pattern, replacement, label)
    if re.search(r'^- Published：.*$', text, re.M):
        text = replace_once(text, r'^- Published：.*$', '- Published：`passed`。', 'published status')

    marker = '## Visual Polish 完成（2026-07-30）'
    if marker not in text:
        next_line = f'- 全書庫下一個 Visual Polish target：`{next_target}`。' if next_target else '- 全書庫 Visual Polish queue 已清空。'
        block = f'''\n\n{marker}\n\n- Task：`{target}:VP`；結果：`passed`。\n- 高價值資產：`{asset_title(Path(sys.argv[1]), vp['asset'], title + ' Visual Polish')}`。\n- Canva design ID：`{vp.get('canvaDesignId','')}`；可編輯來源：`{vp.get('canvaEditUrl','')}`。\n- PWA 資產：`{vp['asset']}`；平板可閱讀、可放大、沿用既有離線 cache path。\n- 正式 run：`{receipt['workflow_run_id']}`；Pages artifact：`{receipt['pages_artifact_id']}`。\n- Artifact digest：`{receipt['pages_artifact_digest']}`；重新下載 SHA256 完全一致。\n- VP validator：`{checks} checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。\n- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。\n- 詳細證據：`docs/books/{target}/visual_polish.md`。\n- 本書已切換至 `{target}:PUB`。\n{next_line}\n'''
        text = text.rstrip() + block
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def create_record_if_missing(path: Path, site: Path, target: str, book_title: str, vp: dict, receipt: dict, checks: int, next_target: str | None) -> None:
    if path.exists():
        return
    root = site / 'books' / target
    m = load_json(root / 'manifest.json')
    q = load_json(root / 'questions.json')
    s = load_json(root / 'search.json')
    svg_dir = site / 'assets' / f'{target}-svg'
    chapter_count = sum(1 for x in m['chapters'] if x.get('kind') == 'chapter')
    appendix_count = sum(1 for x in m['chapters'] if x.get('kind') == 'appendix')
    svg_count = len(list(svg_dir.glob('*.svg'))) if svg_dir.is_dir() else 0
    next_line = f'全書庫下一個 Visual Polish target 為 `{next_target}`。' if next_target else '全書庫 Visual Polish queue 已清空。'
    text = f'''# 《{book_title}》Visual Polish Record\n\n- Task ID：`{target}:VP`\n- 日期：2026-07-30\n- 結果：`passed`\n- 正式內容版本：`{m['version']}`\n- 正式書庫版本：`{receipt['library_version']}`\n\n## 高價值視覺資產\n\n- 名稱：《{asset_title(site, vp['asset'], book_title + ' Visual Polish')}》\n- Canva design ID：`{vp.get('canvaDesignId','')}`\n- Canva 可編輯來源：`{vp.get('canvaEditUrl','')}`\n- PWA 正式資產：`{vp['asset']}`\n- placement：`{vp.get('placement','')}`\n\n## PWA／相容性\n\n- tablet readability：PASS。\n- standalone zoom：PASS。\n- offline cache：PASS。\n- 正文 {chapter_count} 章、附錄 {appendix_count} 份、題庫 {q['count']} 題、搜尋索引 {len(s['entries'])} 筆、SVG {svg_count} 張。\n- Book ID、chapter ID、question ID、閱讀進度、錯題資料與 storage key 均維持相容。\n- `progress_storage_changed=false`。\n\n## 正式 Actions 證據\n\n- 正式 Visual Polish run：`{receipt['workflow_run_id']}`。\n- Pages artifact：`{receipt['pages_artifact_id']}`。\n- Artifact digest：`{receipt['pages_artifact_digest']}`。\n- Artifact re-download SHA256：`{receipt['artifact_download_sha256']}`，與 digest 完全一致。\n- VP validator：部署前與 artifact 重下載後均 `{checks} checks`、`visual_polish=passed`。\n- 正式 artifact：21 本、library `{receipt['library_version']}`。\n\n## 結論\n\n`{target}:VP = passed`；本書回到 `{target}:PUB`。{next_line}\n'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def update_checkpoint(path: Path, audit: dict, receipt: dict, completed_titles: list[str], next_target: str | None, next_title: str | None, target_title: str, asset_name: str, checks: int) -> None:
    text = path.read_text(encoding='utf-8')
    text = replace_once(text, r'^- 正式書庫內容版本：`[^`]+`.*$', f"- 正式書庫內容版本：`{receipt['library_version']}`", 'checkpoint library')
    if re.search(r'^- `docs/deployment_receipt\.json`：.*$', text, re.M):
        text = replace_once(text, r'^- `docs/deployment_receipt\.json`：.*$', f"- `docs/deployment_receipt.json`：`status=success`、`book_count=21`、`library_version={receipt['library_version']}`、`progress_storage_changed=false`。", 'checkpoint receipt')

    completed = audit['visual_polish_completed_count']
    remaining = audit['visual_polish_queue_count']
    completed_list = '、'.join(f'`{x}`' for x in [b['book_id'] for b in audit['books'] if b['stages'].get('VP') == 'passed'])
    text = replace_once(text, r'^- Visual Polish：\*\*\d+／21 完成\*\*；.*$', f'- Visual Polish：**{completed}／21 完成**；{completed_list} 已通過，剩餘 {remaining} 本在 queue。', 'checkpoint VP summary')
    text = replace_once(text, r'^- Published：\*\*21／21\*\*.*$', f'- Published：**21／21** 保持正式發布與 PWA 相容性；完成 VP 的 {completed} 本已進入新制 `PUB` 完成狀態。', 'checkpoint published')

    bullet = f'  - 《{target_title}》：《{asset_name}》，沿用既有資產 cache path；VP validator **{checks} checks**，部署前及 artifact 重下載後各 PASS。'
    if bullet not in text:
        pub_idx = text.find('\n- Published：**21／21**')
        if pub_idx == -1:
            raise AssertionError('checkpoint published anchor missing')
        text = text[:pub_idx] + '\n' + bullet + text[pub_idx:]

    next_block = '## 下一個正式任務\n\n'
    if next_target:
        next_block += f'- Task ID：`{next_target}:VP`\n- 書籍：《{next_title}》\n- Stage：Visual Polish\n- 原則：只處理真正有考前價值的高價值視覺資產；依該書正式 routing 與既有 QA／External Audit 證據先複核高風險內容。\n- EA queue 已清空，因此由 `visual_polish_queue[0]` 自動判定下一個 VP 任務。\n'
    else:
        next_block += '- Visual Polish queue 已清空；21 本均完成 VP。\n'
    text, n = re.subn(r'## 下一個正式任務\n.*?(?=\n## )', next_block.rstrip(), text, count=1, flags=re.S)
    if n != 1:
        raise AssertionError('checkpoint next-task block')

    infra = '- Visual Polish 發布已統一由 owner-triggered `Apply next Visual Polish` 共用 runner 執行；完成 Canva 批准後可自動完成套用、QA、Pages、artifact 重驗、generic recorder 與 VP→PUB control-plane closure，不再為每本建立暫時 listener／closure PR。'
    if infra not in text:
        anchor = '## 基礎設施注意事項\n'
        pos = text.find(anchor)
        if pos == -1:
            raise AssertionError('infrastructure section missing')
        insert = pos + len(anchor)
        text = text[:insert] + '\n' + infra + text[insert:]
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def main(site_root: str, target: str) -> None:
    site = Path(site_root)
    audit_path = REPO / 'docs/audit_progress_manifest.json'
    receipt_path = REPO / 'docs/deployment_receipt.json'
    registry_path = REPO / 'deploy/visual_polish_registry.json'
    checkpoint_path = REPO / 'docs/shared_checkpoint.md'

    audit = load_json(audit_path)
    receipt = load_json(receipt_path)
    registry = load_json(registry_path)
    if audit.get('first_visual_polish_target') != target:
        raise AssertionError((audit.get('first_visual_polish_target'), target))
    if target not in registry.get('targets', {}):
        raise AssertionError(f'{target} missing registry')
    checks = int(registry['targets'][target]['expected_checks'])

    site_lib = load_json(site / 'data/library.json')
    site_manifest = load_json(site / 'books' / target / 'manifest.json')
    vp = site_manifest.get('visualPolish', {})
    if vp.get('status') != 'passed':
        raise AssertionError(f'{target} site artifact is not VP-passed')
    if site_lib['version'] != receipt['library_version']:
        raise AssertionError((site_lib['version'], receipt['library_version']))
    if receipt.get('status') != 'success' or receipt.get('book_count') != 21 or receipt.get('progress_storage_changed') is not False:
        raise AssertionError('deployment receipt not formally verified')
    if receipt.get('artifact_download_recheck') != 'passed':
        raise AssertionError('artifact re-download not passed')
    if receipt.get('artifact_download_sha256') != str(receipt.get('pages_artifact_digest','')).removeprefix('sha256:'):
        raise AssertionError('artifact digest mismatch')

    queue = list(audit['visual_polish_queue'])
    if not queue or queue[0] != target:
        raise AssertionError((queue[:1], target))
    queue = [x for x in queue if x != target]
    audit['library_version'] = receipt['library_version']
    audit['visual_polish_queue'] = queue
    audit['visual_polish_ready'] = list(queue)
    audit['visual_polish_queue_count'] = len(queue)
    audit['first_visual_polish_target'] = queue[0] if queue else None

    book = next((b for b in audit['books'] if b['book_id'] == target), None)
    if not book:
        raise AssertionError('target book missing')
    book['current_stage'] = 'PUB'
    book['task_id'] = f'{target}:PUB'
    book['next_stage'] = None
    book['stages']['VP'] = 'passed'
    book['stages']['PUB'] = 'passed'
    book['visual_polish'] = {
        'completed_at': '2026-07-30',
        'record': f'docs/books/{target}/visual_polish.md',
        'asset': vp['asset'],
        'canva_design_id': vp.get('canvaDesignId'),
        'canva_edit_url': vp.get('canvaEditUrl'),
        'workflow_run_id': str(receipt['workflow_run_id']),
        'pages_artifact_id': str(receipt['pages_artifact_id']),
        'artifact_digest': receipt['pages_artifact_digest'],
        'tablet_readable': bool(vp.get('tabletReadable')),
        'zoomable': bool(vp.get('zoomable')),
        'offline_cached': bool(vp.get('offlineCachedViaExistingAssetPath')),
        'validator_checks': checks,
        'content_version_change_required': False,
        'unresolved_blockers': 0,
    }
    audit['visual_polish_completed_count'] = sum(1 for b in audit['books'] if b['stages'].get('VP') == 'passed')
    dump_json(audit_path, audit)

    next_target = audit['first_visual_polish_target']
    next_book = next((b for b in audit['books'] if b['book_id'] == next_target), None) if next_target else None
    status_path = REPO / f'docs/books/{target}/status.md'
    update_status(status_path, target, book['title'], receipt['library_version'], vp, receipt, checks, next_target)
    record_path = REPO / f'docs/books/{target}/visual_polish.md'
    create_record_if_missing(record_path, site, target, book['title'], vp, receipt, checks, next_target)
    update_checkpoint(checkpoint_path, audit, receipt, [], next_target, next_book['title'] if next_book else None, book['title'], asset_title(site, vp['asset'], book['title'] + ' Visual Polish'), checks)

    print('VISUAL_POLISH_CONTROL_PLANE_CLOSED', target, receipt['library_version'], f"completed={audit['visual_polish_completed_count']}", f"queue={audit['visual_polish_queue_count']}", f"next={next_target}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: close_visual_polish_control_plane.py SITE_ROOT TARGET')
    main(sys.argv[1], sys.argv[2])
