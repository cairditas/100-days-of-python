#TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

import pandas as pd

df = pd.read_csv("nato_phonetic_alphabet.csv")

nato_dict = {row.letter: row.code for (index, row) in df.iterrows()}

input = input("Enter a word: ")
nato_words = [nato_dict[letter.upper()] for letter in input]

[print(format(f"{word}")) for word in nato_words]