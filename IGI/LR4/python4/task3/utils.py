import time

class UserInput:
    @staticmethod
    def get_valid_input(prompt: str, type_cast, validation=lambda x: True, error_msg="Invalid input.") -> float:
        while True:
            try:
                value = type_cast(input(prompt))
                if validation(value):
                    return value
                print(error_msg)
            except ValueError:
                print(error_msg)

def timer_decorator(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken by {func.__name__}: {end_time - start_time:.6f} seconds")
        return result
    return wrapper
