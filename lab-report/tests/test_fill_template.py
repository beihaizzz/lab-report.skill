"""Tests for fill_template.py."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.fill_template import fill_template, verify_original_unchanged


SCRIPT = Path(__file__).parent.parent / "scripts" / "fill_template.py"


@pytest.fixture
def fill_data(tmp_path):
    """Create a temporary JSON data file for template filling."""
    data = {
        "姓名": "张三",
        "学号": "20240001",
        "学院": "物理学院",
        "专业": "物理学",
        "班级": "物理2101",
        "课程名": "大学物理实验",
        "实验名称": "RC电路研究",
        "实验日期": "2024-03-15",
        "实验地点": "物理实验楼302",
        "实验目的": "理解RC电路的基本工作原理",
        "实验原理": "RC电路由电阻和电容组成",
        "实验器材": "示波器、电阻、电容",
        "实验步骤": "1.连接电路 2.观察波形",
        "实验数据": "测量数据如下",
        "实验结果": "实验成功",
        "实验结论": "验证了指数衰减规律",
    }
    data_path = tmp_path / "data.json"
    data_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data_path


class TestPlaceholderReplacement:
    def test_placeholder_replacement(self, template_path, fill_data, tmp_path):
        output_path = tmp_path / "filled.docx"

        # Compute original hash
        with open(template_path, "rb") as f:
            original_hash = hashlib.sha256(f.read()).hexdigest()

        result = fill_template(template_path, fill_data, output_path)

        assert result["success"], f"fill failed: {result.get('error')}"
        assert output_path.exists(), "output file should exist"

        # Verify {{姓名}} was replaced (no remaining placeholder)
        assert "姓名" not in result.get("placeholders_missing", []), \
            "{{姓名}} should not be in missing placeholders"

        # Verify original unchanged
        assert verify_original_unchanged(template_path, original_hash), \
            "original template SHA256 should be unchanged"


class TestOriginalPreserved:
    def test_original_preserved(self, template_path, fill_data, tmp_path):
        output_path = tmp_path / "filled2.docx"

        with open(template_path, "rb") as f:
            original_hash = hashlib.sha256(f.read()).hexdigest()

        fill_template(template_path, fill_data, output_path)

        assert verify_original_unchanged(template_path, original_hash), \
            "original template SHA256 should be unchanged after fill"


class TestFileNotFound:
    def test_file_not_found(self, tmp_path):
        missing_template = tmp_path / "missing.docx"
        missing_data = tmp_path / "missing.json"

        proc = subprocess.run(
            [sys.executable, str(SCRIPT),
             "--template", str(missing_template),
             "--data", str(missing_data),
             "--output", str(tmp_path / "out.docx")],
            capture_output=True, text=True
        )
        assert proc.returncode == 1, f"expected exit 1, got {proc.returncode}"
