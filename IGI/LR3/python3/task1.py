import math
from utils import timer_decorator

@timer_decorator
def compute_arcsin_series(x: float, eps: float) -> tuple[float, int]:
    """
    Compute the sum of the arcsin series up to the specified precision.
    
    Args:
        x (float): The input value (|x|<1).
        eps (float): The precision (epsilon) for the series convergence.
    
    Returns:
        tuple[float, int]: The sum of the series and the number of terms added.
    """
    if abs(x) > 1:
        raise ValueError("Input x must be in the range (-1, 1).")
    
    sum_total = x  # First term (n=0)
    terms_added = 1
    max_terms = 500
    
    for n in range(1, max_terms):
        term = (math.factorial(2 * n) / ((4 ** n) * (math.factorial(n) ** 2) * (2 * n + 1))) * (x ** (2 * n + 1))
        if abs(term) < eps:
            break
        sum_total += term
        terms_added += 1
    
    return sum_total, terms_added

def task1_main():
    """Main function for Task 1: handles user input and displays results."""
    from utils import get_valid_input
    
    x = get_valid_input("Enter x (|x| <1): ", float, lambda x: -1 < x < 1, "x must be in range (-1, 1).")
    eps = get_valid_input("Enter epsilon (precision): ", float, lambda x: x > 0, "Epsilon must be positive.")
    
    sum_series, n = compute_arcsin_series(x, eps)
    math_fx = math.asin(x)
    
    print(f"{'x':<10} {'n':<10} {'F(x)':<15} {'MathF(x)':<15} {'eps':<10}")
    print(f"{x:<10.4f} {n:<10} {sum_series:<15.6f} {math_fx:<15.6f} {eps:<10.6f}")
