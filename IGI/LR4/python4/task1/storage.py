import csv
import pickle
from student import Student

CSV_FILE = "data/students.csv"
PICKLE_FILE = "data/students.pkl"

def save_to_csv(students):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["surname", "age"])
        writer.writeheader()
        for student in students:
            writer.writerow(student.to_dict())

def load_from_csv():
    students = []
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(Student.from_dict({"surname": row["surname"], "age": int(row["age"])}))
    except FileNotFoundError:
        print("⚠️ CSV-файл не найден.")
    return students

def save_to_pickle(students):
    with open(PICKLE_FILE, "wb") as file:
        data = [s.to_dict() for s in students]
        pickle.dump(data, file)

def load_from_pickle():
    try:
        with open(PICKLE_FILE, "rb") as file:
            data = pickle.load(file)
            return [Student.from_dict(item) for item in data]
    except FileNotFoundError:
        print("⚠️ Pickle-файл не найден.")
        return []
