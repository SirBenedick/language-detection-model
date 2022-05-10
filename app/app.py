import streamlit as st
from language_detection.lang_detector import LanguageDetector, Language
import requests
API = "https://language-detection-api-v2.herokuapp.com"
# wake up the API deployment
requests.get(API)

if __name__ == "__main__":
    detector = LanguageDetector(
        "data/trained_models/simple_mlp_novectorize.h5", "data/trained_models/vectorizer")

    # Add "user_input" and "detected_language" to the session state, this stop steramlit from overwriting them
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ''
    if 'detected_language' not in st.session_state:
        st.session_state['detected_language'] = ''

    title = st.title('Language detection model v2')

    ## Input section
    input_section_text = st.text_area(
        "Please enter sample text to detect language: ",
        value="",
        placeholder="SE4AI is my favorite course",
        disabled=False,
    )

    detect_button = st.button("Detect language")

    if detect_button:
        st.session_state.user_input = str(input_section_text)
        st.session_state.detected_language = detector.detect_language(
            st.session_state.user_input)
    
    ## Results section
    user_input = str(input_section_text)
    detection_result_input = st.markdown(
        f'Input text: **{st.session_state.user_input if st.session_state.user_input else "-"}**')
    detection_result_language = st.markdown(
        f'The detected language is: **{st.session_state.detected_language if st.session_state.detected_language else "-"}**')

    ## Feedback section
    def getIndexForLanguage():
        if(st.session_state.detected_language == Language.ENGLISH):
            return 0
        elif(st.session_state.detected_language == Language.GERMAN):
            return 1
        elif(st.session_state.detected_language == Language.SPANISH):
            return 2
        else:
            return 0

    feedback_headline = st.markdown('## Please provide feedback')
    feedback_language = st.radio(
        f'What language was "{st.session_state.user_input if st.session_state.user_input else "-"}"?', ('English', 'German', 'Spanish'), index=getIndexForLanguage())

    feedback_button = st.button("Send Feedback")

    if feedback_button:
        text = st.session_state.user_input
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
                st.write("Successfully sent feedback. Thank you!")
            else:
                st.write("Something failed")
        else:
            st.write("Please enter a text first and detect the language!")
