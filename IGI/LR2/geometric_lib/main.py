import circle
import square

def main():
    print("Circle Calculations:")
    r = 5  # Радиус круга
    print(f"Area: {circle.area(r)}")
    print(f"Perimeter: {circle.perimeter(r)}")

    print("\nSquare Calculations:")
    a = 4  # Сторона квадрата
    print(f"Area: {square.area(a)}")
    print(f"Perimeter: {square.perimeter(a)}")

if __name__ == "__main__":
    main()
