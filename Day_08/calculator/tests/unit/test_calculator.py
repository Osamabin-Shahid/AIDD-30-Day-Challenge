import pytest
from src.lib.calculator import evaluate_expression, InvalidExpressionError, DivisionByZeroError

def test_basic_arithmetic():
    assert evaluate_expression("2+2") == 4.0
    assert evaluate_expression("10-5") == 5.0
    assert evaluate_expression("3*4") == 12.0
    assert evaluate_expression("20/4") == 5.0
    assert evaluate_expression("1 + 2 * 3") == 7.0 # Precedence test
    assert evaluate_expression(" (1 + 2) * 3 ") == 9.0 # Parentheses not yet supported, but test to see behavior
    assert evaluate_expression("10 / 2 + 3") == 8.0 # Precedence test (5 + 3)
    assert evaluate_expression("2 * 3 + 4 * 5") == 26.0 # Precedence test (6 + 20)
    assert evaluate_expression("1.5 + 2.5") == 4.0
    assert evaluate_expression("5 - 2 * 2") == 1.0 # Precedence test
    assert evaluate_expression("6 / 2 - 1") == 2.0 # Precedence test


def test_division_by_zero_error():
    with pytest.raises(DivisionByZeroError):
        evaluate_expression("10/0")
    with pytest.raises(DivisionByZeroError):
        evaluate_expression("5 / (2-2)") # Should ideally catch this
        
def test_invalid_expression_error():
    with pytest.raises(InvalidExpressionError):
        evaluate_expression("2++2")
    with pytest.raises(InvalidExpressionError):
        evaluate_expression("abc")
    with pytest.raises(InvalidExpressionError):
        evaluate_expression("")
    with pytest.raises(InvalidExpressionError):
        evaluate_expression("2 +")
    with pytest.raises(InvalidExpressionError):
        evaluate_expression("+ 2")
    with pytest.raises(InvalidExpressionError):
        evaluate_expression("2 (3)")