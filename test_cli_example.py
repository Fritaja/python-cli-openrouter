import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).with_name("cli_example.py"))


def test_cli_valid_name():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--name", "Ivan"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Ivan!"


def test_cli_missing_name():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 2
    assert "required" in result.stderr
