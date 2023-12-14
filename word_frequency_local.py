# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:37:48 2023

@author: vzocc
"""

from collections import Counter
import re

def rank_words_by_frequency(file_path):
    # Read text from the file
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            text = file.read()
    except FileNotFoundError:
        return "File not found. Please provide a valid file path."

    # Clean the text and split it into words
    words = re.findall(r'\b\w+(?:\'\w+)?\b', text.lower())

    # Count the frequency of each word
    word_frequency = Counter(words)

    # Rank words by frequency
    ranked_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

    return ranked_words

def remove_stop_words(ranked_words, stop_words_file):
    try:
        with open(stop_words_file, 'r', encoding='utf-8') as file:
            stop_words = file.read().splitlines()
        filtered_words = [(word, freq) for word, freq in ranked_words if word.lower() not in stop_words]
        return filtered_words
    except FileNotFoundError:
        print("Stop words file not found.")
        return ranked_words

def filter_words_by_frequency(ranked_words, min_frequency=2):
    filtered_words = [(word, freq) for word, freq in ranked_words if freq >= min_frequency]
    return filtered_words

# Replace 'downloaded_text.txt' with the path to your downloaded text file
result = rank_words_by_frequency('G:/Il mio Drive/Resume e Lavoro/Zocca Valentino FINAL.txt')
result = remove_stop_words(result, 'stopwords.txt')
result = filter_words_by_frequency(result, min_frequency=3)

# Display the ranked words and their frequencies
if isinstance(result, str):
    print(result)
else:
    for word, frequency in result:
        print(f"{word}: {frequency}")

