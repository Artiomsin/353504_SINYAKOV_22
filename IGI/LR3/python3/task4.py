
def count_lowercase_letters(sentence: str) -> int:
    """
    Count the number of lowercase letters in a sentence.
    
    Args:
        sentence (str): Input sentence.
    
    Returns:
        int: Number of lowercase letters.
    """
    return sum(1 for char in sentence if char.islower())

def find_last_word_with_i(sentence: str) -> tuple[str, int]:
    """
    Find the last word containing 'i' and its position.
    
    Args:
        sentence (str): Input sentence.
    
    Returns:
        tuple[str, int]: The last word containing 'i' and its position.
    """
    words = sentence.replace(',', ' ').split()
    last_word, last_pos = "", -1
    for idx, word in enumerate(words, 1):
        if 'i' in word:
            last_word, last_pos = word, idx
    return last_word, last_pos

def remove_words_starting_with_i(sentence: str) -> str:
    """
    Remove words that start with 'i' from the sentence.
    
    Args:
        sentence (str): Input sentence.
    
    Returns:
        str: Modified sentence.
    """
    words = sentence.replace(',', ' ').split()
    filtered_words = [word for word in words if not word.lower().startswith('i')]
    return ' '.join(filtered_words)

def task4_main():
    """Main function for Task 4: runs analysis on a predefined text."""
    sample_text = "So she was considering in her own mind, as well as she could, for the " \
    "hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain " \
    "would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit " \
    "with pink eyes ran close by her."
    
    print("4a: Number of lowercase letters:", count_lowercase_letters(sample_text))
    
    word, pos = find_last_word_with_i(sample_text)
    if pos != -1:
        print(f"\n4b: Last word containing 'i': {word}, Position: {pos}")
    else:
        print("\n4b: No word containing 'i' found.")
    
    print("\n4c: Sentence without words starting with 'i':")
    print(remove_words_starting_with_i(sample_text))