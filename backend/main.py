def hello_world():
    message = "Hello, World!"
    print(message)
    return message


def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    result = a + b
    return result


if __name__ == "__main__":
    hello_world()
    print(f"2 + 3 = {calculate_sum(2, 3)}")