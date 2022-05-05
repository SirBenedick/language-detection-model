import streamlit as st
from language_detection.lang_detector import LanguageDetector

if __name__ == "__main__":
    detector = LanguageDetector("data/trained_models/simple_mlp_novectorize.h5", "data/trained_models/vectorizer")
    
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

    def get_text_input_value():
        return text_input

    def detect_language():
        user_text = get_text_input_value()
        language = detector.detect_language(text_input)
        st.write("Detected language is %s" % language)


    button = st.button(
        "Detect language",
        on_click=detect_language
    )
