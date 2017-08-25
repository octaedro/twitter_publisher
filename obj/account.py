# -*- coding: utf-8 -*-
import tweepy

class Account:
    def __init__(self,data):
        self.consumerkey = data["consumerkey"]
        self.consumersecret = data["consumersecret"]
        self.accesstoken = data["accesstoken"]
        self.accesstokensecret = data["accesstokensecret"]
        self.account = data["account"]
        self.key_word = data["key_word"]
        self.table = data["table"]
        self.publish_min = data["publish_min"]
        self.api = self.getAPI()

    def getNewTweet(self,connection):
        self.tweet = connection.getNewTweet(self.table)
        if self.tweet:
            return self.tweet
        tweets_list = self.getTweetsFromTwitter()
        if len(tweets_list) > 0:
            connection.saveTweetsList(self.table, tweets_list)
            return connection.getNewTweet(self.table)
        return False

    def publish(self):
        # send message to twitter'
        return self.api.update_status(self.tweet['content'])

    def getTweetsFromTwitter(self):
        list_tweets = []
        search_number = 100
        search_result = self.api.search(self.key_word, lang="es", rpp=search_number)
        for i in search_result:
            try:
                if i.retweeted_status is None:
                    print "Is retweet"
            except:
                if not i.text == "":
                    list_tweets.append(i.text)
        return list_tweets

    def getAPI(self):
        auth = tweepy.OAuthHandler(self.consumerkey, self.consumersecret)
        auth.set_access_token(self.accesstoken, self.accesstokensecret)
        return tweepy.API(auth)