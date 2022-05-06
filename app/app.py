import streamlit as st
from language_detection.lang_detector import LanguageDetector
import requests
API = "https://language-detection-api-v2.herokuapp.com"

if __name__ == "__main__":
    detector = LanguageDetector(
        "data/trained_models/simple_mlp_novectorize.h5", "data/trained_models/vectorizer")

    title = st.title('Language detection model v2')

    # Input section
    input_section_text = st.text_area(
        "Please enter sample text to detect language: ",
        value="",
        placeholder="SE4AI is my favorite course",
        disabled=False,
    )

    detect_button = st.button("Detect language")
    if detect_button:
        user_input = str(input_section_text)
        language = detector.detect_language(user_input)
        detection_result_input = st.markdown(f'Input text: **{user_input}**')
        detection_result_language = st.markdown(
            f'The detected language is: **{language}**')

    # Results section
    detection_result_input = st.empty()
    detection_result_language = st.empty()

    # Feedback section
    feedback_headline = st.markdown('## Please provide feedback')
    feedback_language = st.radio(
        f'What language was "{str(input_section_text)}"?', ('English', 'German', 'Spanish'))

    feedback_button = st.button("Send Feedback")

    if feedback_button:
        text = str(input_section_text)
        label = str(feedback_language)
        if bool(text) and bool(label):
            if label == "English":
                label = "en"
            elif label == "German":
                label = "de"
            elif label == "Spanish":
                label = "es"

            r = requests.get(f"{API}/add?text={text}&label={label}")
            if r.status_code == 200:
                st.write("Successfully entered fedback. Thank you!")
            else:
                st.write("Something failed")
        else:
            st.write("Please enter a text first and detect the language!")
