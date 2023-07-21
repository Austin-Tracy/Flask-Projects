# ml_app/ml_models/sentiment_analysis.py
import os
import tensorflow as tf
import numpy as np
import pickle
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)


def predict_sentiment(text: str) -> str:
    """
    Predicts the sentiment of a given text using a trained model.

    Args:
        text (str): The text to predict the sentiment of.

    Returns:
        str: The predicted sentiment, either 'Positive' or 'Negative'.
    """
    with open(os.path.join('ml_app', 'trained_models', 'tokenizer.pkl'), 'rb') as handle:
        tokenizer = pickle.load(handle)
    model = tf.keras.models.load_model(os.path.join('ml_app', 'trained_models', 'SentimentAnalysisModel.h5'))
    tokenized_text = tokenizer.texts_to_sequences([text])
    padded_text = tf.keras.preprocessing.sequence.pad_sequences(tokenized_text, maxlen=703)  # assuming a max length of 100
    prediction = model.predict(np.array(padded_text))
    sentiment = 'Positive' if prediction > 0.75 else 'Negative'
    return sentiment

