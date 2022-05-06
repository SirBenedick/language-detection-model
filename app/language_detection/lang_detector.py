import tensorflow as tf
import pickle
from keras import layers
import numpy as np
import enum


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

class Language(enum.Enum):
    SPANISH = "es"
    ENGLISH = "en"
    GERMAN = "de"

    def __str__(self):
        return self.value

class LanguageDetector:

    LABELS = [Language.GERMAN, Language.ENGLISH, Language.SPANISH]
    
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = self._load_model(model_path)
        self.vectorizer = self._load_vectorizer(vectorizer_path)

    def _load_model(self, path: str):
        saved_model = tf.keras.models.load_model(path)
        return saved_model

    def _load_vectorizer(self, path: str):
        loaded_model = tf.keras.models.load_model(path)
        loaded_vectorizer = loaded_model.layers[0]
        return loaded_vectorizer

    def detect_language(self, text: str) -> Language:
        vectorized = self.vectorizer([text])
        print(text, vectorized)
        logits = self.model.predict(vectorized)
        lang_index = np.argmax(logits, axis=1)[0]
        lang = self.LABELS[lang_index]
        print(lang)
        return lang
