import numpy as np
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def tokenize(sentence):
    """Split sentence into words/tokens"""
    return word_tokenize(sentence)

def stem(word):
    """Reduce word to its stem"""
    return stemmer.stem(word.lower())

def lemmatize(word):
    """Reduce word to its base form"""
    return lemmatizer.lemmatize(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """Create bag of words array"""
    # Stem all words
    sentence_words = [stem(word) for word in tokenized_sentence]
    # Initialize bag with 0s
    bag = np.zeros(len(all_words), dtype=np.float32)
    # Create word-to-index mapping
    word_idx = {word: idx for idx, word in enumerate(all_words)}
    # Set 1 for each known word
    for word in sentence_words:
        if word in word_idx:
            bag[word_idx[word]] = 1
    return bag