"""Pytest configuration and fixtures for lab-report tests."""
import sys
from pathlib import Path

import pytest

# Add the lab-report package to the path for imports
LAB_REPORT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(LAB_REPORT_ROOT))


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return LAB_REPORT_ROOT


@pytest.fixture
def test_data_dir():
    """Return the test fixtures directory."""
    return LAB_REPORT_ROOT / "tests" / "fixtures"


@pytest.fixture
def references_dir():
    """Return the references directory."""
    return LAB_REPORT_ROOT / "references"
