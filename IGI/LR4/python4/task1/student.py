class Student:
    """
    Класс, представляющий ученика.
    """

    def __init__(self, surname: str, age: int):
        self.surname = surname
        self.age = age

    def __repr__(self):
        return f"Student(surname={self.surname}, age={self.age})"

    def __lt__(self, other):
        return self.age < other.age

    def to_dict(self):
        """Преобразование в словарь (для сериализации)."""
        return {"surname": self.surname, "age": self.age}

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря."""
        return cls(data["surname"], data["age"])
