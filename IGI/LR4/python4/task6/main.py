import pandas as pd

# Загружаем данные в DataFrame (например, 'fifa19.csv')
df = pd.read_csv('fifa19.csv')

# 1. Получение информации о DataFrame
print("Информация о DataFrame:")
print(df.info())

# 2. Получение статистической сводки
print("\nСтатистическая сводка:")
print(df.describe())

# Задание 1: Во сколько раз среднее значение силы удара (ShotPower) самых агрессивных игроков (с максимальной агрессией)
# выше среднего значения силы удара игроков с минимальной агрессией.

# Находим самых агрессивных игроков (с максимальной агрессией)
max_aggression = df[df['Aggression'] == df['Aggression'].max()]

# Находим самых неагрессивных игроков (с минимальной агрессией)
min_aggression = df[df['Aggression'] == df['Aggression'].min()]

# Средняя сила удара для самых агрессивных игроков
avg_shotpower_max_aggression = max_aggression['ShotPower'].mean()

# Средняя сила удара для самых неагрессивных игроков
avg_shotpower_min_aggression = min_aggression['ShotPower'].mean()

# Во сколько раз среднее значение силы удара у агрессивных игроков выше у неагрессивных
if avg_shotpower_min_aggression != 0:
    ratio = avg_shotpower_max_aggression / avg_shotpower_min_aggression
    print(f"\nВо сколько раз средняя сила удара агрессивных игроков выше: {round(ratio, 2)}")
else:
    print("\nНе возможно вычислить, так как сила удара у неагрессивных игроков равна 0.")

# Задание 2: Средняя скорость (SprintSpeed) футболистов с зарплатой ниже среднего.

# Средняя зарплата
avg_wage = df['Wage'].mean()

# Футболисты с зарплатой ниже средней
below_avg_wage = df[df['Wage'] < avg_wage]

# Средняя скорость этих футболистов
avg_sprint_speed = below_avg_wage['SprintSpeed'].mean()
print(f"\nСредняя скорость футболистов с зарплатой ниже средней: {round(avg_sprint_speed, 2)}")
