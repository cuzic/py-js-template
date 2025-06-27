def hello_world():
    return "Hello, World!"


def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b


if __name__ == "__main__":
    message = hello_world()
    result = calculate_sum(2, 3)
    # Print statements are used for demonstration purposes
    print(message)  # noqa: T201
    print(f"2 + 3 = {result}")  # noqa: T201
