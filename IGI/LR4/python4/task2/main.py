from file_handler import TextFileHandler
from text_analyzer import TextAnalyzer
from data_archiver import DataArchiver

def main():
    input_handler = TextFileHandler('input.txt')
    text = input_handler.read()

    analyzer = TextAnalyzer(text)
    results = analyzer.analyze()

    print("=== Результаты анализа ===")
    print(results)

    output_handler = TextFileHandler('output.txt')
    output_handler.write(results)

    DataArchiver.archive_file('output.txt', 'results.zip')

if __name__ == "__main__":
    main()