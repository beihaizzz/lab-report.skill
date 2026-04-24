"""Tests for student_info.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

# Root-level script, conftest adds to sys.path
import student_info


# Path to CLI script
STUDENT_INFO_SCRIPT = Path(__file__).parent.parent.parent / "scripts" / "student_info.py"


class TestDiscoverStudentInfo:
    def test_discover_student_info(self, student_info_file):
        """find_student_info should parse the temp file."""
        filepath, info = student_info.find_student_info(student_info_file.parent)
        assert filepath is not None, "should find 学生信息.md"
        assert info is not None, "should parse info"
        assert info.get("姓名") == "张三"
        assert info.get("学号") == "20240001"

    def test_json_output_cli(self, student_info_file):
        """CLI --json should produce valid JSON."""
        proc = subprocess.run(
            [sys.executable, str(STUDENT_INFO_SCRIPT),
             "--dir", str(student_info_file.parent),
             "--json"],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}"
        data = json.loads(proc.stdout)
        assert data["found"] is True
        assert data["data"] is not None
        assert data["data"].get("姓名") == "张三"


class TestNotFound:
    def test_not_found(self, tmp_path):
        """graceful when 学生信息.md is missing."""
        filepath, info = student_info.find_student_info(tmp_path)
        assert filepath is None
        assert info is None

    def test_cli_not_found(self, tmp_path):
        """CLI gracefully exits 0 when file missing."""
        proc = subprocess.run(
            [sys.executable, str(STUDENT_INFO_SCRIPT),
             "--dir", str(tmp_path),
             "--json"],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, "should exit 0 even when not found"
        data = json.loads(proc.stdout)
        assert data["found"] is False
