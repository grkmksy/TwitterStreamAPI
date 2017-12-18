# Twitter Stream API with Apache Kafka Integration

This python code is streaming Twitter data to your local Apache Kafka topic as json objects, based on your specified stream filters. 

# Requirements
  - [Python3.0](https://www.python.org/) or above must be installed.
  - [tweepy](https://github.com/tweepy/tweepy) python library must be installed.
  - [kafka-python](https://github.com/dpkp/kafka-python) library must be installed
  - Apache Kafka must be installed.
 
### Twitter Stream API Specifications
The Twitter streaming API is used to download twitter messages in real time. It is useful for obtaining a high volume of tweets, or for creating a live feed using a site stream or user stream. See the [Twitter Streaming API Documentation](https://developer.twitter.com/en/docs).

> **Detailed informatin about tweepy library http://docs.tweepy.org/en/v3.4.0/index.html**

Twitter Developer Access Tokens
```sh
CONSUMER_KEY = "Your Consumer Key"
CONSUMER_SECRET = "Your Consumer Secret Key"
ACCESS_TOKEN = "Your Access Token"
ACCESS_TOKEN_SECRET = "Your Token Secret"
```
Create a Twitter Connection and Authorize
```sh
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
```
Class to be passed to Twitter connection. Method names are self explanatory and invoked by Twitter connection
```sh
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
```
Method to be invoked by the main script
```sh
def start_stream():
    # Create listener with properties
    listener = realTimeStreamer(api=tweepy.API(wait_on_rate_limit=False))
    # Pass the authentication and listener to a streamer
    streamer = tweepy.Stream(auth=auth, listener=listener)
    # Start streaming by passing keywords and languages to be tracked
    # Details: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
    streamer.filter(track=word_list, languages=['BCP 47 Language Identifier'], stall_warnings=True)
```
Main method
```sh
if __name__ == "__main__":
    start_stream()
```
### Apache Kafka Installation

Download and Install latest release of Apache Kafka. (Ubuntu 16.04 & CentOS 7)
```sh
$ wget http://ftp.itu.edu.tr/Mirror/Apache/kafka/1.0.0/kafka_2.11-1.0.0.tgz
```
Step 1 : Extract Files
```sh
$ tar -xzf kafka_2.11-1.0.0.tgz
$ cd kafka_2.11-1.0.0
```

Step 2 : Start ZooKeeper & Kafka Servers
```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
$ bin/kafka-server-start.sh config/server.properties
```

Step 3 : Create a Kafka Topic
```sh
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafka-social
```

Step 4: List active Kafka Topics 
```sh
$ bin/kafka-topics.sh --list --zookeeper localhost:2181
```

Step 5 : Test Kafka Producer & Send Some Messages
```sh
$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka-social
```


Step 6 : Test Kafka Consumer & Dump Some Messages
```sh
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kafka-social --from-beginning
```
**After successful completion of these operations, you can start stream api and write tweets to your kafka topic.**
