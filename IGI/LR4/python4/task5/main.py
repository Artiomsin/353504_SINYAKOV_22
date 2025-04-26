import numpy as np

# -------------------------
# а) Библиотека NumPy
# -------------------------

print("=== а) Библиотека NumPy ===\n")

# 1. Создание массива. Функции array() и arange()
print("1. Функция array():")
manual_array = np.array([[1, 2, 3], [4, 5, 6]])
print(manual_array)

print("\nФункция arange():")
values_array = np.arange(1, 10)
print(values_array)

# 2. Функции создания массива заданного вида
print("\n2. Массивы специального вида:")
zeros_array = np.zeros((2, 3))
ones_array = np.ones((3, 2))
identity_matrix = np.eye(3)

print("Массив из нулей:\n", zeros_array)
print("Массив из единиц:\n", ones_array)
print("Единичная матрица:\n", identity_matrix)

# 3. Индексирование и срезы
print("\n3. Индексирование и срезы:")
n, m = 4, 5
A = np.random.randint(0, 100, size=(n, m))
print("Матрица A:\n", A)

first_row = A[0]
last_col = A[:, -1]
sub_matrix = A[1:3, 1:4]

print("Первая строка:", first_row)
print("Последний столбец:", last_col)
print("Подматрица [1:3, 1:4]:\n", sub_matrix)

# 4. Поэлементные операции
print("\n4. Универсальные (поэлементные) функции:")
A_squared = A ** 2
A_plus_10 = A + 10
print("A в квадрате:\n", A_squared)
print("A + 10:\n", A_plus_10)

# -------------------------
# б) Математические и статистические операции
# -------------------------

print("\n=== б) Математические и статистические операции ===\n")

# 1. mean()
mean_val = np.mean(A)
print("1. Среднее значение (mean):", mean_val)

# 2. median()
median_val = np.median(A)
print("2. Медиана (median):", median_val)

# 3. corrcoef()
corr_matrix = np.corrcoef(A)
print("3. Матрица корреляций (corrcoef):\n", corr_matrix)

# 4. var()
variance = np.var(A)
print("4. Дисперсия (var):", variance)

# 5. std()
std_dev = np.std(A)
print("5. Стандартное отклонение (std):", std_dev)

# 6. Элементы выше среднего
above_mean = A[A > mean_val]
print("\nЭлементы выше среднего значения:", above_mean)

# 7. Побочная диагональ
print("\n7. Работа с побочной диагональю:")

# Побочная диагональ — от верхнего правого к нижнему левому
min_dim = min(n, m)
secondary_diag = np.array([A[i, m - 1 - i] for i in range(min_dim)])
print("Элементы побочной диагонали:", secondary_diag)

# Наименьший элемент
min_secondary = np.min(secondary_diag)
print("Наименьший элемент побочной диагонали:", min_secondary)

# Дисперсия — метод 1
var1 = round(np.var(secondary_diag), 2)

# Дисперсия — метод 2 (ручной)
mean_sd = np.mean(secondary_diag)
squared_diffs = (secondary_diag - mean_sd) ** 2
var2 = round(np.mean(squared_diffs), 2)

print("Дисперсия побочной диагонали (метод 1):", var1)
print("Дисперсия побочной диагонали (метод 2):", var2)
