import pytest
from backend.main import hello_world, calculate_sum


def test_hello_world():
    assert hello_world() == "Hello, World!"


def test_calculate_sum():
    # Test basic addition
    assert calculate_sum(2, 3) == 5  # noqa: PLR2004
    # Test with negative numbers
    assert calculate_sum(-1, 1) == 0
    # Test with zeros
    assert calculate_sum(0, 0) == 0