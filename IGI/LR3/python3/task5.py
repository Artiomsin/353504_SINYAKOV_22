from initialization import input_list_user, generate_list_random
from utils import get_valid_input

def display_list(lst: list[float]):
    """Display the list elements."""
    print("List elements:", lst)

def count_elements_greater_than_c(lst: list[float], c: float) -> int:
    """
    Count elements in the list that are greater than C.
    
    Args:
        lst (list[float]): List of numbers.
        c (float): The threshold value.
    
    Returns:
        int: Count of elements greater than C.
    """
    return sum(1 for x in lst if x > c)

def compute_product_before_max(lst: list[float]) -> float:
    """
    Compute product of elements before the maximum by absolute value.
    
    Args:
        lst (list[float]): List of numbers.
    
    Returns:
        float: Product of elements before max absolute element.
    """
    if not lst:
        return 0

    max_index = max(range(len(lst)), key=lambda i: abs(lst[i]))
    
    if max_index == 0:
        return 1  # Если max abs элемент первый, то перед ним нет элементов
    
    product = 1
    for i in range(max_index):
        product *= lst[i]
    
    return product

def task5_main():
    """Main function for Task 5: handles list initialization and processing."""
    print("Initialize list:")
    print("1. User input")
    print("2. Random generator")
    choice = get_valid_input("Select method (1/2): ", int, lambda x: x in (1, 2))
    
    lst = input_list_user() if choice == 1 else generate_list_random()
    display_list(lst)

    c = get_valid_input("Enter C: ", float)
    
    count = count_elements_greater_than_c(lst, c)
    product = compute_product_before_max(lst)
    
    print(f"Number of elements greater than {c}: {count}")
    print(f"Product of elements before max absolute element: {product}")
