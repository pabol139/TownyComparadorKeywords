import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

from keys import consumer_key, consumer_secret

print(consumer_key)
print(consumer_secret)

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def get_tweets(keyword: str) -> List[str]:

    all_tweets = []

    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='extended', lang='es').items(100):
        all_tweets.append(tweet.full_text)    

   # for tweet in all_tweets:
    #    print(tweet)



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

if __name__ == "__main__":

    print("Primera Keyword:")
    first_thing = input()
    print("Segunda Keyword:")
    second_thing = input()
    print("\n")

    first_score = generate_average_sentiment_score(first_thing)
    second_score = generate_average_sentiment_score(second_thing)

    print(f"Puntuacion Primera Keyword: {first_score}")
    print(f"Puntuacion Segunda Keyword: {second_score}")
