"""Tests for git_manager.py."""
import subprocess
import sys
from pathlib import Path

# Root-level script
SCRIPT = Path(__file__).parent.parent.parent / "scripts" / "git_manager.py"


class TestNonGitDir:
    def test_non_git_dir(self, temp_dir):
        """In a non-git directory, silently exit 0."""
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--dir", str(temp_dir)],
            capture_output=True, text=True
        )
        assert proc.returncode == 0, \
            f"expected exit 0 in non-git dir, got {proc.returncode}"
        # Should not print errors for non-git dir
        assert "Git error" not in proc.stderr
