import re
from collections import Counter
from abc import ABC, abstractmethod

class Analyzer(ABC):
    def __init__(self, text):
        self.text = text

    @abstractmethod
    def analyze(self):
        pass

class TextAnalyzer(Analyzer):
    def analyze(self):
        results = []

        # Email и имена
        email_name_pairs = re.findall(r'([A-Za-z]+)\s*<([\w.-]+@[\w.-]+)>', self.text)
        results.append(f"Email-адреса и соответствующие имена: {dict(email_name_pairs)}\n")

        # Замена $v_(i)$ на v[i]
        replaced_text = re.sub(r'\$v_\(([a-zA-Z0-9])\)\$', r'v[\1]', self.text)
        results.append(f"Текст после замены $v_(i)$ на v[i]:\n{replaced_text}\n")

        # Слова, начинающиеся или заканчивающиеся на гласную
        words = re.findall(r'\b\w+\b', self.text)
        vowels = 'aeiouаеёиоуыэюяAEIOUАЕЁИОУЫЭЮЯ'
        vowel_words = [word for word in words if word[0] in vowels or word[-1] in vowels]
        results.append(f"Количество слов, начинающихся или заканчивающихся на гласную: {len(vowel_words)}\n")

        # Частота символов
        char_count = Counter(self.text)
        results.append(f"Частота встречаемости символов:\n{char_count}\n")

        # Слова после первой запятой, в алфавитном порядке
        after_comma = re.split(r',', self.text, maxsplit=1)
        words_after_comma = sorted(re.findall(r'\b\w+\b', after_comma[1])) if len(after_comma) > 1 else []
        results.append(f"Слова после первой запятой (в алфавитном порядке):\n{words_after_comma}\n")

        # Типы предложений
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        total_sentences = len(sentences)
        declarative = len(re.findall(r'(?<!\?)\.(\s|$)', self.text))
        interrogative = len(re.findall(r'\?(\s|$)', self.text))
        imperative = 0  # Пока не реализовано определение побудительных
        results.append(f"Общее количество предложений: {total_sentences}")
        results.append(f"Повествовательные предложения: {declarative}")
        results.append(f"Вопросительные предложения: {interrogative}")
        results.append(f"Побудительные предложения: {imperative}\n")

        # Средняя длина предложений и слов
        avg_sent_len = sum(len(s.split()) for s in sentences) / total_sentences if total_sentences else 0
        avg_word_len = sum(len(word) for word in words) / len(words) if words else 0
        results.append(f"Средняя длина предложения (в словах): {avg_sent_len:.2f}")
        results.append(f"Средняя длина слова (в символах): {avg_word_len:.2f}\n")

        # Количество смайликов
        smiley_pattern = r'[:;]-*([\(\)\[\]])\1+'
        smileys = re.findall(smiley_pattern, self.text)
        results.append(f"Количество смайликов в тексте: {len(smileys)}\n")

        return "\n".join(results)
