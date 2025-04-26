from school_class import SchoolClass
from student import Student
from utils import get_valid_input
import storage

# Определяем возрастные группы
AGE_GROUPS = {
    '10-12': (10, 12),
    '13-15': (13, 15),
    '16-18': (16, 18)
}

def main():
    school_class = SchoolClass()

    # 1. Задание исходных данных (словарь)
    initial_data = {
        "Иванов": 14,
        "Петров": 12,
        "Сидоров": 16
    }

    print("📌 Исходные данные из словаря:")
    for surname, age in initial_data.items():
        student = Student(surname, age)
        school_class.add_student(student)
        print(f"✅ Добавлен ученик: {student}")

    # 2. Дополнительный ручной ввод учеников
    print("\n📝 Введите дополнительных учеников (или 'stop'):")
    while True:
        surname = input("Введите фамилию (или 'stop'): ").strip()
        if surname.lower() == 'stop':
            break
        if not surname:
            print("❌ Фамилия не может быть пустой!\n")
            continue

        age = get_valid_input(
            "Введите возраст: ",
            int,
            lambda x: any(min_age <= x <= max_age for min_age, max_age in AGE_GROUPS.values()),
            "❌ Возраст вне допустимых границ!"
        )

        student = Student(surname, age)
        school_class.add_student(student)
        print(f"✅ Добавлен ученик: {student}")

    # 3. Группировка по возрасту
    print("\n📊 Возрастные группы:")
    age_groups = school_class.categorize_age_groups()
    for group, students in age_groups.items():
        names = ', '.join([s.surname for s in students]) if students else "— Нет учеников"
        print(f"{group}: {names}")

    # 4. Сортировка
    school_class.sort_students_by_age()
    print("\n📋 Ученики после сортировки по возрасту:")
    school_class.display_students()

    # 5. Поиск ученика
    surname_search = input("\n🔍 Введите фамилию ученика для поиска: ").strip()
    if not surname_search:
        print("⚠️ Фамилия не может быть пустой.")
    else:
        found = school_class.find_student(surname_search)
        if found:
            print(f"✅ Найден ученик: {found}")
        else:
            print("❌ Ученик не найден.")

    # 6. Сохранение в файлы
    storage.save_to_csv(school_class.students)
    print("\n💾 Сохранено в CSV (students.csv)")

    storage.save_to_pickle(school_class.students)
    print("💾 Сохранено в Pickle (students.pkl)")

    # 7. Загрузка из файлов
    print("\n📂 Данные из CSV:")
    csv_students = storage.load_from_csv()
    if csv_students:
        for s in csv_students:
            print(s)
    else:
        print("⚠️ CSV-файл пуст или не найден.")

    print("\n📂 Данные из Pickle:")
    pickle_students = storage.load_from_pickle()
    if pickle_students:
        for s in pickle_students:
            print(s)
    else:
        print("⚠️ Pickle-файл пуст или не найден.")

    # 8. Повтор программы
    while True:
        again = input("\n🔄 Повторить программу? (yes/no): ").lower()
        if again == "yes":
            print("\n🔁 Перезапуск...\n")
            main()
            break
        elif again == "no":
            print("👋 Завершение.")
            break
        else:
            print("❌ Введите 'yes' или 'no'.")

if __name__ == "__main__":
    main()
