from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

from keys import consumer_key, consumer_secret

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

app = Flask(__name__)
CORS(app)
apiSv = Api(app)

precision = 10

def get_tweets(keyword: str) -> List[str]:

    all_tweets = []

    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='extended', lang='es').items(precision):
        all_tweets.append(tweet.full_text)    

    return all_tweets

def clean_tweets(all_tweets: List[str]) -> List[str]:

    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    return tweets_clean

def get_sentiment(all_tweets: List[str]) -> List[float]:

    sentiment_scores = []

    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores

def generate_average_sentiment_score(keyword: str) -> int:

    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)

    average_score = statistics.mean(sentiment_scores)

    return average_score

class Puntuacion(Resource):
    def get(self):
    	kw1 = request.args.get("keyword1")
    	kw2 = request.args.get("keyword2")
    	global precision
    	precision = int(request.args.get("precision"))

    	first_score = generate_average_sentiment_score(kw1)
    	second_score = generate_average_sentiment_score(kw2)

    	finaaaa = (f"Puntuacion Primera Keyword: {first_score}! Puntuacion Segunda Keyword: {second_score}!")

    	return finaaaa

apiSv.add_resource(Puntuacion, '/puntuacion')  # Route_1

if __name__ == '__main__':
     app.run(port='5000')
