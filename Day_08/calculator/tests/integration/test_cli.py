import pytest
import subprocess
import sys

# Assuming the main script is run via `python -m src.cli.main`
cli_module = "src.cli.main"

def run_cli_command(expression: str) -> subprocess.CompletedProcess:
    """Helper function to run the CLI command."""
    command = [sys.executable, "-m", cli_module] + expression.split()
    return subprocess.run(command, capture_output=True, text=True, check=False)

def test_cli_basic_arithmetic():
    result = run_cli_command("2+2")
    assert result.returncode == 0
    assert "Result: 4.0" in result.stdout

    result = run_cli_command("10 / 2 - 1")
    assert result.returncode == 0
    assert "Result: 4.0" in result.stdout # 10/2 = 5, 5-1 = 4

def test_cli_division_by_zero():
    result = run_cli_command("10/0")
    assert result.returncode == 1
    assert "Error: Cannot divide by zero." in result.stderr

def test_cli_invalid_expression():
    result = run_cli_command("2++2")
    assert result.returncode == 1
    assert "Error: Consecutive operators are not allowed." in result.stderr

    result = run_cli_command("abc")
    assert result.returncode == 1
    assert "Error: Unsupported character: 'a'" in result.stderr
    
    result = run_cli_command("") # Test empty input
    assert result.returncode == 1
    assert "Usage: python -m src.cli.main <expression>" in result.stdout # CLI usage message

def test_cli_missing_expression():
    result = subprocess.run([sys.executable, "-m", cli_module], capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "Usage: python -m src.cli.main <expression>" in result.stdout