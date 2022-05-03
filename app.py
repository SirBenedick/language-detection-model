import streamlit as st
import tensorflow as tf
from keras import layers


@st.cache
def load_model(path: str):
    saved_model = tf.keras.models.load_model(path)
    return saved_model


# Pickle the config and weights
pickle.dump({'config': vectorizer.get_config(),
             'weights': vectorizer.get_weights()}
            , open("tv_layer.pkl", "wb"))

@st.cache
def load_vectorizer(path: str):
    from_disk = pickle.load(open(path, "rb"))
    new_v = TextVectorization.from_config(from_disk['config'])
    # You have to call `adapt` with some dummy data (BUG in Keras)
    new_v.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
    new_v.set_weights(from_disk['weights'])
    return new_v


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def _detect_language(model, vectorizer, text: str):
    '''
    TODO: insert language model magic here
    '''
    max_features = 10000 # top 10K most frequent words
    sequence_length = 50 # We defined it in the previous data exploration section

    vectorized = vectorizer(text)

    logits = model.predict(vectorized)
    probits = softmax(logits)
    idx_predictions = np.argmax(probits, axis=1)
    
    lang = le.inverse_transform(idx_predictions)[0]


if __name__ == "__main__":
    language_model = load_model("models/simple_mlp_novectorize.h5")
    
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
            text_input,
        ),
    )
