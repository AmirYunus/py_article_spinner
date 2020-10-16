import nltk
import random
import numpy as np

from bs4 import BeautifulSoup

positive_reviews = BeautifulSoup(open('electronics/positive.review').read(), "html.parser")
positive_reviews = positive_reviews.findAll('review_text')
trigrams = {}

for each_review in positive_reviews:
    string = each_review.text.lower()
    tokens = nltk.tokenize.word_tokenize(string)

    for each_index in range(len(tokens) - 2):
        k = (tokens[each_index], tokens[each_index + 2])

        if k not in trigrams:
            trigrams[k] = []

        trigrams[k].append(tokens[each_index + 1])

trigram_probabilities = {}

for k, words in trigrams.items():
    if len(set(words)) > 1:
        dictionary = {}
        n = 0

        for each_word in words:
            if each_word not in dictionary:
                dictionary[each_word] = 0
            
            dictionary[each_word] += 1
            n += 1

        for each_word, each_character in dictionary.items():
            dictionary[each_word] = float(each_character) / n

        trigram_probabilities[k] = dictionary

def random_sample(dictionary):
    cumulative = 0

    for each_word, p in dictionary.items():
        cumulative += p
        
        if random.random() < cumulative:
            return each_word

def test_spinner():
    review = random.choice(positive_reviews)
    string = review.text.lower()
    print(f"Original: {string}")
    tokens = nltk.tokenize.word_tokenize(string)

    for each_index in range(len(tokens) -2):
        if random.random() < 0.2:
            k = (tokens[each_index], tokens[each_index +2])

            if k in trigram_probabilities:
                each_word = random_sample(trigram_probabilities[k])
                tokens[each_index + 1] = each_word

    print(f"Generated: \n{' '.join(tokens).replace(' .', '.').replace(' ,', ',').replace('$ ', '$').replace(' !', '!')}")

if __name__ == "__main__":
    test_spinner()