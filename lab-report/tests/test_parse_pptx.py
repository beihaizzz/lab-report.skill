"""Tests for parse_pptx.py."""
import json
import subprocess
import sys
from pathlib import Path


# Root-level script
SCRIPT = Path(__file__).parent.parent.parent / "scripts" / "parse_pptx.py"


class TestSlideCount:
    def test_slide_count(self, sample_pptx):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(sample_pptx), "--format", "json"],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}"
        data = json.loads(proc.stdout)
        assert data["slide_count"] >= 5, \
            f"expected >=5 slides, got {data['slide_count']}"


class TestJsonOutput:
    def test_json_output(self, sample_pptx):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(sample_pptx), "--format", "json"],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}"
        data = json.loads(proc.stdout)
        assert "slide_count" in data
        assert "slides" in data
        assert len(data["slides"]) == data["slide_count"]
        # At least one slide should have content
        slides_with_content = [
            s for s in data["slides"]
            if s.get("title") or s.get("content")
        ]
        assert len(slides_with_content) > 0, "at least one slide should have content"


class TestFileNotFound:
    def test_file_not_found(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", "nonexistent_file.pptx"],
            capture_output=True, text=True
        )
        assert proc.returncode == 1, f"expected exit 1, got {proc.returncode}"
        assert "File not found" in proc.stderr
