"""
Author: Sinyakov Artiom Alexandrovich
Group: 353504
Lab Work: Lab 3
Topic: Standard Data Types, Collections, Functions, Modules
Purpose: To master the basic syntax of Python, gain skills in working with standard data types, collections, functions, and modules, and consolidate these skills through the development of interactive applications.
Date: 04.04.2025
"""


from task1 import task1_main
from utils import get_valid_input
from task2 import task2_main
from task3 import task3_main
from task4 import task4_main
from task5 import task5_main

def main_menu():
    """Display the main menu and handle user input to run tasks."""
    while True:
        print("\nMain Menu")
        print("1. Task 1: arcsin series")
        print("2. Task 2: sum_of_cubes")
        print("3. Task 3: is_binary_number")
        print("4. Task 4: Analyze text")
        print("5. Task 5: Process list")
        print("6. Exit")
        choice = get_valid_input("Select task (1-6): ", int, lambda x: 1 <= x <= 6)
        if choice == 1:
            task1_main()
        elif choice == 2:
            task2_main()
        elif choice == 3:
            task3_main()
        elif choice == 4:
            task4_main()
        elif choice == 5:
            task5_main()
        elif choice == 6:
            break
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()