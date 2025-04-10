
def is_binary_number(s: str) -> bool:
    """
    Check if the input string is a binary number (contains only '0' and '1').
    
    Args:
        s (str): Input string.
    
    Returns:
        bool: True if the string is a binary number, False otherwise.
    """
    return all(c in '01' for c in s) and len(s) > 0

def task3_main():
    """Main function for Task 3: handles input and displays results."""
    s = input("Enter a string: ")
    if is_binary_number(s):
        print("The entered string is a binary number.")
    else:
        print("The entered string is NOT a binary number.")

