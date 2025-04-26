from abc import ABC, abstractmethod

class FileHandler(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

class TextFileHandler(FileHandler):
    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def write(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)
