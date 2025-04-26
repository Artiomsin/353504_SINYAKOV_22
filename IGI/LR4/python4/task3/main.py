from function_calculator import ArcsinCalculator
from graph_plotter import GraphPlotter
from utils import UserInput

def task3_main():
    x = UserInput.get_valid_input("Enter x (|x| <1): ", float, lambda x: -1 < x < 1, "x must be in range (-1, 1).")
    eps = UserInput.get_valid_input("Enter epsilon (precision): ", float, lambda x: x > 0, "Epsilon must be positive.")

    # Работа с вычислениями
    calculator = ArcsinCalculator(x, eps)
    sum_series, n, series_values = calculator.calculate_series()
    math_fx = calculator.calculate_function()

    # Анализ статистики
    mean = calculator.mean()
    median = calculator.median()
    mode = calculator.mode()
    variance = calculator.variance()
    std_dev = calculator.standard_deviation()

    # Выводим результаты
    print(f"{'x':<10} {'n':<10} {'F(x)':<15} {'MathF(x)':<15} {'eps':<10}")
    print(f"{x:<10.4f} {n:<10} {sum_series:<15.6f} {math_fx:<15.6f} {eps:<10.6f}")
    
    print("\n=== Статистический анализ серии ===")
    print(f"Среднее значение: {mean}")
    print(f"Медиана: {median}")
    print(f"Мода: {mode}")
    print(f"Дисперсия: {variance}")
    print(f"Стандартное отклонение: {std_dev}")

    # Строим графики
    graph_plotter = GraphPlotter()
    graph_plotter.plot(x, series_values, eps)

if __name__ == "__main__":
    task3_main()
