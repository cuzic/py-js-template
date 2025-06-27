from backend.main import calculate_sum, hello_world


def test_hello_world() -> None:
    assert hello_world() == "Hello, World!"


def test_calculate_sum() -> None:
    # Test basic addition
    assert calculate_sum(2, 3) == 5
    # Test with negative numbers
    assert calculate_sum(-1, 1) == 0
    # Test with zeros
    assert calculate_sum(0, 0) == 0
