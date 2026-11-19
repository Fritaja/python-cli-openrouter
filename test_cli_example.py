import subprocess
import sys


def test_cli_valid_name():
    result = subprocess.run(
        [sys.executable, "cli_example.py", "--name", "Ivan"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, Ivan!"


def test_cli_missing_name():
    result = subprocess.run(
        [sys.executable, "cli_example.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "required" in result.stderr
