"""Tests for parse_pdf.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.parse_pdf import parse_pdf


SCRIPT = Path(__file__).parent.parent / "scripts" / "parse_pdf.py"


class TestParseNormalPdf:
    def test_parse_normal_pdf(self, sample_pdf):
        result = parse_pdf(sample_pdf)
        assert result["page_count"] > 0, "page_count should be > 0"
        assert result["is_scanned"] is False, "normal PDF should not be scanned"
        assert result["markdown"], "markdown should have content"
        assert "error" not in result, f"unexpected error: {result.get('error')}"


class TestDetectScannedPdf:
    def test_detect_scanned_pdf(self, sample_scanned_pdf):
        result = parse_pdf(sample_scanned_pdf)
        assert result["is_scanned"] is True, "should detect as scanned"
        assert result["warning"] == "SCANNED_PDF_DETECTED", "should set warning"


class TestJsonOutput:
    def test_json_output(self, sample_pdf):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(sample_pdf), "--format", "json"],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}"
        data = json.loads(proc.stdout)
        assert "page_count" in data
        assert "markdown" in data
        assert "is_scanned" in data


class TestMarkdownOutput:
    def test_markdown_output(self, sample_pdf):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(sample_pdf), "--format", "markdown"],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}"
        assert "# " in proc.stdout or "## " in proc.stdout, \
            "markdown output should contain headings"


class TestFileNotFound:
    def test_file_not_found(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", "nonexistent_file.pdf"],
            capture_output=True, text=True
        )
        assert proc.returncode == 1, f"expected exit 1, got {proc.returncode}"
        assert "File not found" in proc.stderr
