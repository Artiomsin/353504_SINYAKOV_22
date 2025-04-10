
from utils import get_valid_input
import random

def input_list_user() -> list:
    """Initialize list with user input."""
    n = get_valid_input("Enter list size: ", int, lambda x: x > 0, "Size must be a positive integer.")
    return [get_valid_input(f"Element {i+1}: ", int) for i in range(n)]


def random_generator(n: int, min_val: int, max_val: int):
    """Generator function yielding random integers."""
    for _ in range(n):
        yield random.randint(min_val, max_val)


def generate_list_random() -> list[int]:
    """Generate list using random generator."""
    n = get_valid_input("Enter the number of elements: ", int, lambda x: x > 0)
    min_val = get_valid_input("Enter minimum value: ", int)
    max_val = get_valid_input("Enter maximum value: ", int)
    return list(random_generator(n, min_val, max_val))