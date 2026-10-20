import math

import pytest

from calculator import AdvancedCalculator


@pytest.fixture
def calculator():
    return AdvancedCalculator()


def test_addition(calculator):
    assert calculator.add(10, 5) == 15


def test_subtraction(calculator):
    assert calculator.subtract(10, 5) == 5


def test_multiplication(calculator):
    assert calculator.multiply(4, 5) == 20


def test_division(calculator):
    assert calculator.divide(10, 2) == 5


def test_division_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)


def test_power(calculator):
    assert calculator.power(2, 3) == 8


def test_square_root(calculator):
    assert calculator.square_root(25) == 5


def test_negative_square_root(calculator):
    with pytest.raises(ValueError):
        calculator.square_root(-4)


def test_factorial(calculator):
    assert calculator.factorial(5) == 120


def test_factorial_rejects_float(calculator):
    with pytest.raises(ValueError):
        calculator.factorial(5.5)


def test_sine(calculator):
    assert math.isclose(calculator.sine(30), 0.5, abs_tol=1e-9)


def test_cosine(calculator):
    assert math.isclose(calculator.cosine(60), 0.5, abs_tol=1e-9)


def test_tangent_at_90_degrees(calculator):
    with pytest.raises(ValueError):
        calculator.tangent(90)


def test_natural_log(calculator):
    assert math.isclose(calculator.natural_log(math.e), 1.0)


def test_log10(calculator):
    assert math.isclose(calculator.log10(100), 2.0)


def test_logarithm_rejects_zero(calculator):
    with pytest.raises(ValueError):
        calculator.log10(0)


def test_calculation_history(calculator):
    calculator.add(2, 3)
    history = calculator.show_history()

    assert len(history) == 1
    assert history[0]["result"] == 5


def test_history_returns_a_copy(calculator):
    calculator.add(2, 3)
    history = calculator.show_history()
    history.clear()

    assert len(calculator.show_history()) == 1
