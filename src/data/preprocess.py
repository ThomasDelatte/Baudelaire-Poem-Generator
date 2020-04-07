import numpy as np
import string
from keras.utils import np_utils

def preprocess(filepath):
    """To be completed"""

    # Load the text
    with open(filepath) as f:
        text = f.read()

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation for better performance
    table = str.maketrans("", "", string.punctuation)
    text = [w.translate(table) for w in text]

    # Create mapping of unique chars to integers
    chars = sorted(list(set(text)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    # Summarize the loaded data
    n_chars = len(text)
    n_vocab = len(chars)

    # Prepare the dataset of input to output pairs encoded as integers
    seq_length = 100

    dataX = []
    dataY = []

    for i in range(0, n_chars - seq_length, 1):
        seq_in = text[i:i + seq_length]
        seq_out = text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])

    n_patterns = len(dataX)
    print(f"Total Patterns:{n_patterns}")

    # reshape X to be [samples, time steps, features]
    X = np.reshape(dataX, (n_patterns, seq_length, 1))

    # normalize
    X = X / float(n_vocab)

    # one hot encode the output variable
    y = np_utils.to_categorical(dataY)

    processed_X = np.save(
        "/home/tdelatte/Projects/Deep_Learning/NLP/Baudelaire_Poem_Generator/data/processed/processed_X.npy", X)
    processed_y = np.save(
        "/home/tdelatte/Projects/Deep_Learning/NLP/Baudelaire_Poem_Generator/data/processed/processed_y.npy", y)

    return X, y

X, y = preprocess("/home/tdelatte/Projects/Deep_Learning/NLP/Baudelaire_Poem_Generator/data/raw/baudelaire.txt")