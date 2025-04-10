
def sum_of_cubes():
    """Sum cubes of numbers entered by the user until 12 is input."""
    total = 0
    while True:
        try:
            num = int(input("Enter an integer (12 to stop): "))
            if num == 12:
                break
            total += num ** 3
        except ValueError:
            print("Invalid input. Please enter an integer.")
    return total

def task2_main():
    """Main function for Task 2: handles input and displays the result."""
    print("Enter integers. 12 to stop.")
    total = sum_of_cubes()
    print(f"Sum of cubes: {total}")

if __name__ == "__main__":
    task2_main()