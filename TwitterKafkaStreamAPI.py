"""Twitter Stream API with Apache Kafka Producer Integration"""
__author__ = "Görkem Aksoy"

from __future__ import print_function
import tweepy
import sys
import json
from kafka import KafkaProducer

# Keywords to be tracked
word_list = ["Keyword List to be Tracked"]

# Twitter Authentication Keys
# Details : https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens
CONSUMER_KEY = "Your Consumer Key"
CONSUMER_SECRET = "Your Consumer Secret Key"
ACCESS_TOKEN = "Your Access Token"
ACCESS_TOKEN_SECRET = "Your Token Secret"

# Create a Twitter Connection and Authorize
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create a Apache Kafka Producer object to be able to send data to desired topics
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))


# Class to be passed to Twitter connection. Method names are self explanatory and invoked by Twitter connection
class realTimeStreamer(tweepy.StreamListener):
    def on_connect(self):
        print("Connected")

    def on_error(self, status_code):
        print('Error:' + repr(status_code))
        return False

    def on_data(self, data):
        try:
            # Whole Tweet object.
            # Details https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
            datajson = json.loads(data)
            # Display twitter stream
            print(datajson)
            # Send each tweet object to Kafka Topic named kafka-social
            producer.send("kafka-social", datajson)
        except Exception as e:
            # Error is occurred while processing a tweet.
            print("In exception")
            print(e)
            print(sys.exc_info()[0])


# Method to be invoked by the main script
def start_stream():
    # Create listener with properties
    listener = realTimeStreamer(api=tweepy.API(wait_on_rate_limit=False))
    # Pass the authentication and listener to a streamer
    streamer = tweepy.Stream(auth=auth, listener=listener)
    # Start streaming by passing keywords and languages to be tracked
    # Details: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
    streamer.filter(track=word_list, languages=['BCP 47 Language Identifier'], stall_warnings=True)


# Main method
if __name__ == "__main__":
    start_stream()
