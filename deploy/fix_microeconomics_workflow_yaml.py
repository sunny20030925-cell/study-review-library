#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(' '))


def main(src_path: str, dst_path: str) -> None:
    src = Path(src_path)
    dst = Path(dst_path)
    lines = src.read_text(encoding='utf-8').splitlines()
    out: list[str] = []
    i = 0
    fixed_status = False
    fixed_section = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("status = f'''# 《個體經濟學》狀態"):
            yaml_indent = leading_spaces(line)
            out.append(line)
            i += 1
            while i < len(lines):
                current = lines[i]
                current_stripped = current.strip()
                if current_stripped == "'''":
                    out.append(' ' * yaml_indent + "'''")
                    fixed_status = True
                    i += 1
                    break
                if not current_stripped:
                    out.append(' ' * yaml_indent)
                elif leading_spaces(current) < yaml_indent:
                    out.append(' ' * yaml_indent + current.lstrip(' '))
                else:
                    out.append(current)
                i += 1
            else:
                raise AssertionError('unterminated microeconomics status triple-quoted string')
            continue

        if stripped.startswith("section = f'''### 個體經濟學"):
            code_indent = leading_spaces(line)
            yaml_indent = 10
            if code_indent < yaml_indent:
                raise AssertionError(f'unexpected section indent: {code_indent}')
            out.append(line)
            i += 1
            while i < len(lines):
                current = lines[i]
                current_stripped = current.strip()
                if current_stripped == "'''":
                    out.append(' ' * code_indent + "'''")
                    fixed_section = True
                    i += 1
                    break
                if not current_stripped:
                    out.append(' ' * yaml_indent)
                elif leading_spaces(current) < yaml_indent:
                    out.append(' ' * yaml_indent + current.lstrip(' '))
                else:
                    out.append(current)
                i += 1
            else:
                raise AssertionError('unterminated microeconomics checkpoint triple-quoted string')
            continue

        out.append(line)
        i += 1

    if not fixed_status or not fixed_section:
        raise AssertionError(f'expected blocks not fixed: status={fixed_status} section={fixed_section}')

    text = '\n'.join(out) + '\n'
    dst.write_text(text, encoding='utf-8')
    print(f'MICRO_WORKFLOW_YAML_BLOCKS_FIXED status={fixed_status} section={fixed_section}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: fix_microeconomics_workflow_yaml.py INPUT OUTPUT')
    main(sys.argv[1], sys.argv[2])
