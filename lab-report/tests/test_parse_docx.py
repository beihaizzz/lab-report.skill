"""Tests for parse_docx.py."""
import subprocess
import sys
from pathlib import Path

from scripts.parse_docx import parse_docx


SCRIPT = Path(__file__).parent.parent / "scripts" / "parse_docx.py"


class TestPlaceholderDetection:
    def test_placeholder_detection(self, template_path):
        result = parse_docx(template_path)
        assert "error" not in result, f"unexpected error: {result.get('error')}"
        placeholders = result.get("placeholders", [])
        assert len(placeholders) >= 10, \
            f"expected >=10 placeholders, got {len(placeholders)}: {placeholders}"


class TestTableExtraction:
    def test_table_extraction(self, template_path):
        result = parse_docx(template_path)
        assert result["structure"]["table_count"] >= 1, \
            "should extract at least 1 table"
        assert len(result["tables"]) >= 1, "tables list should be non-empty"


class TestFileNotFound:
    def test_file_not_found(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", "nonexistent_file.docx"],
            capture_output=True, text=True
        )
        assert proc.returncode == 1, f"expected exit 1, got {proc.returncode}"
        assert "File not found" in proc.stderr
