#!/usr/bin/env python3
"""Student info discovery and creation script."""

import argparse
import json
import os
import sys
from pathlib import Path

# Import schemas if available (optional, for type hints)
try:
    from schemas import StudentInfo  # noqa: F401
except ImportError:
    pass  # Schema not required for this script to function

STUDENT_INFO_FILE = "学生信息.md"
TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "学生信息模板.md"

def find_student_info(start_dir: Path = None) -> tuple[Path, dict]:
    """Search for 学生信息.md from start_dir upwards."""
    if start_dir is None:
        start_dir = Path.cwd()

    current = start_dir.resolve()

    # Search up to 3 parent directories
    for _ in range(4):
        candidate = current / STUDENT_INFO_FILE
        if candidate.exists():
            return candidate, parse_student_info(candidate)
        if current.parent == current:  # Reached root
            break
        current = current.parent

    return None, None

def parse_student_info(filepath: Path) -> dict:
    """Parse 学生信息.md file."""
    content = filepath.read_text(encoding='utf-8')
    info = {}

    for line in content.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            info[key.strip()] = value.strip()

    return info

def create_student_info_template(target_dir: Path = None) -> Path:
    """Copy template to target directory."""
    if target_dir is None:
        target_dir = Path.cwd()

    target_file = target_dir / STUDENT_INFO_FILE

    if target_file.exists():
        print(f"Warning: {STUDENT_INFO_FILE} already exists", file=sys.stderr)
        return None

    if TEMPLATE_PATH.exists():
        content = TEMPLATE_PATH.read_text(encoding='utf-8')
    else:
        # Fallback template content
        content = """# 学生信息

姓名:
学号:
学院:
专业:
班级:
"""

    target_file.write_text(content, encoding='utf-8')
    return target_file

def main():
    parser = argparse.ArgumentParser(description='Student info management')
    parser.add_argument('--create', action='store_true', help='Create template file')
    parser.add_argument('--dir', type=Path, default=None, help='Target directory')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    args = parser.parse_args()

    if args.create:
        result = create_student_info_template(args.dir)
        if result:
            print(f"Created: {result}")
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        filepath, info = find_student_info(args.dir)

        if args.json:
            output = {
                'found': filepath is not None,
                'path': str(filepath) if filepath else None,
                'data': info
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            if info:
                print(f"Found: {filepath}")
                for key, value in info.items():
                    print(f"  {key}: {value}")
            else:
                print(f"{STUDENT_INFO_FILE} not found", file=sys.stderr)
                print(f"Run with --create to create a template", file=sys.stderr)

        sys.exit(0 if info else 0)  # Exit 0 even if not found (graceful)

if __name__ == '__main__':
    main()