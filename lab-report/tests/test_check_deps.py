"""Tests for check_deps.py."""
import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).parent.parent / "scripts" / "check_deps.py"


class TestJsonOutput:
    def test_json_output(self):
        """--json produces valid JSON with expected keys."""
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            capture_output=True, text=True
        )
        # check_deps exits 1 if deps missing but still prints JSON
        data = json.loads(proc.stdout)
        assert isinstance(data, dict), "should be a dict"
        expected_keys = ["uv", "python", "pdfplumber", "python-docx", "docxtpl", "python-pptx"]
        for key in expected_keys:
            assert key in data, f"missing key: {key}"
            assert "ok" in data[key], f"key {key} missing 'ok' field"
            assert "detail" in data[key], f"key {key} missing 'detail' field"
