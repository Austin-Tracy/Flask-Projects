from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(review: str) -> str:
    """
    Analyzes the sentiment of a review using the SentimentIntensityAnalyzer from the nltk.sentiment module.

    Args:
        review (str): The text of the review to analyze.

    Returns:
        str: The sentiment of the review, which can be 'Positive', 'Negative', or 'Neutral'.
    """
    sentiment_scores = sia.polarity_scores(review)

    # Classify the sentiment based on the compound score
    if sentiment_scores['compound'] >= 0.1:
        return 'Positive'
    elif sentiment_scores['compound'] <= -0.1:
        return 'Negative'
    else:
        return 'Neutral'