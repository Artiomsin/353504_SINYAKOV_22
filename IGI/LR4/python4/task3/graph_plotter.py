import math
import matplotlib.pyplot as plt

import math
import matplotlib.pyplot as plt

class GraphPlotter:
    def plot(self, x: float, series_values: list, eps: float, save_path: str = "arcsin_graph.png"):
        # Если только одна точка — добавляем вторую, чтобы линия была видимой
        if len(series_values) == 1:
            series_values.append(series_values[0])

        # Ось X — номера членов ряда (итерации)
        x_vals = list(range(1, len(series_values) + 1))
        y_vals_series = series_values
        y_vals_function = [math.asin(x)] * len(series_values)

        # Настройка графика
        plt.figure(figsize=(10, 6))

        # Синяя линия — разложение в ряд
        plt.plot(x_vals, y_vals_series, label="Разложение в ряд", color="blue", marker='o', linewidth=2)

        # Красная пунктирная — значение math.asin(x)
        plt.plot(x_vals, y_vals_function, label="Функция math.asin(x)", color="red", linestyle="--", marker='x', linewidth=2)

        # Отображение осей координат
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)

        # Подписи и легенда
        plt.xlabel("Номер члена ряда (n)")
        plt.ylabel("Значение")
        plt.title("Сравнение разложения arcsin(x) и функции math.asin(x)")
        plt.legend()

        # Ограничение по осям, чтобы график был читаем
        plt.xlim(0, 12)
        plt.ylim(-1.2, 1.2)

        # Аннотация
        plt.annotate(f"x = {x}, ε = {eps}",
                     xy=(len(x_vals), y_vals_series[-1]),
                     xytext=(len(x_vals) + 1, y_vals_series[-1] + 0.1),
                     arrowprops=dict(facecolor='black', arrowstyle='->'))

        # Сохраняем в файл
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
