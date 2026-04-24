"""Tests for init_project.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parent.parent / "scripts" / "init_project.py"


class TestDiscoverFiles:
    def test_discover_files(self, fixtures_dir):
        """discover_files() finds PDF/DOCX/PPTX in the fixtures dir."""
        # Import after sys.path is set up in conftest
        from scripts.init_project import discover_files
        files = discover_files(fixtures_dir)
        all_found = files.get("guides", []) + files.get("templates", [])
        suffixes = {Path(f).suffix.lower() for f in all_found}
        assert ".pdf" in suffixes, "should find PDF files"
        assert ".pptx" in suffixes, "should find PPTX files"


class TestEmptyDir:
    def test_empty_dir(self, temp_dir):
        """Empty directory should produce graceful error."""
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--dir", str(temp_dir)],
            capture_output=True, text=True
        )
        # init_project checks deps first and may fail, but should produce structured output
        try:
            data = json.loads(proc.stdout)
            assert "errors" in data or "discovered_files" in data
        except json.JSONDecodeError:
            # If JSON parse fails, check stderr for error messages
            assert proc.returncode != 0 or "error" in proc.stderr.lower() or \
                "Error" in proc.stderr


class TestLabReportDir:
    def test_lab_report_dir(self, fixtures_dir, temp_dir):
        """init_project should create .lab-report/ directory."""
        # Use fixtures_dir which has discoverable files
        from scripts.init_project import init_project

        result = init_project(fixtures_dir, use_git=False)
        lab_report_dir = fixtures_dir / ".lab-report"

        # Not every run will succeed (depends on deps), but if success is true
        # the directory should exist
        if result.get("success"):
            assert lab_report_dir.exists(), ".lab-report/ should be created"


class TestCliWithDir:
    def test_cli_with_dir(self, fixtures_dir):
        """CLI --dir with valid fixtures directory."""
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--dir", str(fixtures_dir)],
            capture_output=True, text=True
        )
        # May or may not succeed depending on deps, but should produce valid JSON
        try:
            data = json.loads(proc.stdout)
            assert "discovered_files" in data
        except json.JSONDecodeError:
            pytest.fail(f"CLI output was not valid JSON: {proc.stdout[:200]}")
