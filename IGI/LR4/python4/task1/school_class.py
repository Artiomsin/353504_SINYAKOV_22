from student import Student

class SchoolClass:
    """
    Класс для управления списком учеников.
    """

    def __init__(self):
        self.students = []

    def add_student(self, student: Student):
        self.students.append(student)

    def categorize_age_groups(self):
        age_groups = {
            '10-12': [],
            '13-15': [],
            '16-18': []
        }
        for student in self.students:
            if 10 <= student.age <= 12:
                age_groups['10-12'].append(student)
            elif 13 <= student.age <= 15:
                age_groups['13-15'].append(student)
            elif 16 <= student.age <= 18:
                age_groups['16-18'].append(student)
        return age_groups

    def display_students(self):
        for student in self.students:
            print(student)

    def sort_students_by_age(self):
        self.students.sort()

    def find_student(self, surname: str):
        for student in self.students:
            if student.surname.lower() == surname.lower():
                return student
        return None
