import os
from pathlib import Path
import nltk
from flask import Flask, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.data.path.insert(0, str(Path(__file__).parent / "sentiment"))
sia = SentimentIntensityAnalyzer(lexicon_file="vader_lexicon.zip/vader_lexicon/vader_lexicon.txt")
app = Flask(__name__)
@app.get("/")
def home(): return jsonify(service="Sentiment Analyzer", status="ok")
@app.get("/analyze/<path:input_txt>")
def analyze_sentiment(input_txt):
    compound = sia.polarity_scores(input_txt)["compound"]
    sentiment = "positive" if compound >= .05 else "negative" if compound <= -.05 else "neutral"
    return jsonify(sentiment=sentiment)
if __name__ == "__main__": app.run(host="0.0.0.0", port=int(os.getenv("PORT",5050)))
