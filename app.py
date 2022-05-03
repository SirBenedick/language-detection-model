import streamlit as st
import tensorflow as tf
import pickle
from keras import layers
import numpy as np

@st.cache
def load_model(path: str):
    saved_model = tf.keras.models.load_model(path)
    return saved_model


def load_vectorizer(path: str):
    loaded_model = tf.keras.models.load_model(path)
    loaded_vectorizer = loaded_model.layers[0]
    return loaded_vectorizer


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def _detect_language(model, vectorizer, text: str):
    '''
    TODO: insert language model magic here
    '''
    max_features = 10000 # top 10K most frequent words
    sequence_length = 50 # We defined it in the previous data exploration section

    vectorized = vectorizer([text])
    print(text, vectorized)

    logits = model.predict(vectorized)
    lang_index = np.argmax(logits, axis=1)[0]
    print(lang_index)
    
    lang = ["de", "en", "es"][lang_index]
    print(lang)
    st.write("Language is %s" % lang)



if __name__ == "__main__":
    language_model = load_model("models/simple_mlp_novectorize.h5")
    vectorizer = load_vectorizer("vectorizer")
    
    with st.sidebar:
        """
        This is a simple streamlit application that guesses the language of the text passed.
        """

    text_input = st.text_area(
        "Please enter sample text to detect language: ",
        value="",
        placeholder=None,
        disabled=False,
    )

    button = st.button(
        "Detect language",
        on_click=_detect_language,
        args=(
            language_model,
            vectorizer,
            text_input,
        ),
    )
