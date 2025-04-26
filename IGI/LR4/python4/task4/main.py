"""
Main module for testing geometric shape classes.
"""

from shapes import Rectangle, CircleShape, Parallelogram

def get_positive_float(prompt: str) -> float:
    """Get validated positive float input."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive number")

def get_color(prompt: str) -> str:
    """Get color input with basic validation."""
    while True:
        color = input(prompt).strip().lower()
        if len(color) >= 3:
            return color
        print("Color name must be at least 3 characters")

def main_menu():
    """Command-line interface for shape operations."""
    while True:
        print("\nGeometric Shapes Program")
        print("1. Create Rectangle")
        print("2. Create Circle")
        print("3. Create Parallelogram")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '4':
            break
            
        shape = None
        try:
            if choice == '1':
                width = get_positive_float("Enter width: ")
                height = get_positive_float("Enter height: ")
                color = get_color("Enter color: ")
                shape = Rectangle(width, height, color)
                
            elif choice == '2':
                radius = get_positive_float("Enter radius: ")
                color = get_color("Enter color: ")
                shape = CircleShape(radius, color)
            elif choice == '3':
                d1 = get_positive_float("Enter diagonal d1: ")
                d2 = get_positive_float("Enter diagonal d2: ")
                angle = get_positive_float("Enter angle between diagonals (in degrees): ")
                color = get_color("Enter color: ")
                shape = Parallelogram(d1, d2, angle, color)

            else:
                print("Invalid choice")
                continue
            
            # Common operations
            print("\n" + shape.get_info())
            label = input("Enter label text (optional): ")
            filename = input("Enter filename to save (optional): ").strip()
            shape.draw(label=label, filename=filename)
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        if input("\nCreate another shape? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main_menu()