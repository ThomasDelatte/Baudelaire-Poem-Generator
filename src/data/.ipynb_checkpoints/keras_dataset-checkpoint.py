import tensorflow as tf
from tensorflow import keras
import numpy as np

def make_dataset(filepaths, n_steps=100, batch_size=32):
    """Function that preprocesses the data."""

    with open(filepaths) as f:
        text = f.read()

    tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)
    tokenizer.fit_on_texts([text])
    max_id = len(tokenizer.word_index)

    [encoded] = np.array(tokenizer.texts_to_sequences([text])) - 1
    dataset = tf.data.Dataset.from_tensor_slices(encoded)

    window_length = n_steps + 1
    dataset = dataset.window(window_length, shift=1, drop_remainder=True)

    dataset = dataset.flat_map(lambda window: window.batch(window_length))
    dataset = dataset.shuffle(10000).batch(batch_size)
    dataset = dataset.map(lambda windows: (windows[:, :-1], windows[:, 1:]))
    dataset = dataset.map(lambda X_batch, Y_batch: (tf.one_hot(X_batch, depth=max_id), Y_batch))
    dataset = dataset.prefetch(1)

    return dataset