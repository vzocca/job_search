# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:40:24 2023

@author: vzocc
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def open_file(file_path):
    # Read text from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        return "File not found. Please provide a valid file path."

def get_text_from_link(url):
    try:
        # Fetch content from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from HTML
            text = soup.get_text()
            return text
        else:
            return "Failed to fetch content. Please check the URL."
    except requests.RequestException as e:
        return f"Request Exception: {e}"
    
def save_text_to_file(text, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text saved to {file_path}")
    except Exception as e:
        print(f"Error occurred while saving the text: {e}")

def rank_words_by_frequency(text):
    # Use regex to split the text into words while preserving alphanumeric characters and apostrophes
    words = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())

    # Count the frequency of each word
    word_frequency = Counter(words)

    # Rank words by frequency
    ranked_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

    return ranked_words

def filter_words_by_frequency(ranked_words, min_frequency=2):
    filtered_words = [(word, freq) for word, freq in ranked_words if freq >= min_frequency]
    return filtered_words

def remove_stop_words(ranked_words, stop_words_file):
    try:
        with open(stop_words_file, 'r', encoding='utf-8') as file:
            stop_words = file.read().splitlines()
        filtered_words = [(word, freq) for word, freq in ranked_words if word.lower() not in stop_words]
        return filtered_words
    except FileNotFoundError:
        print("Stop words file not found.")
        return ranked_words

# Replace 'your_web_link_here' with the actual URL
web_link = 'your_web_link_here'
web_link = 'https://www.upstart.com/our-story'
web_text = get_text_from_link(web_link)

if not web_text.startswith("Failed"):
    save_text_to_file(web_text, 'downloaded_text.txt')
    ranked_words = rank_words_by_frequency(web_text)
    # Filter out stop words
    ranked_words_without_stop_words = remove_stop_words(ranked_words, 'stopwords.txt')

    filtered_words = filter_words_by_frequency(ranked_words_without_stop_words, min_frequency=3)
    for word, frequency in filtered_words:
        print(f"{word}: {frequency}")
else:
    print(web_text)
