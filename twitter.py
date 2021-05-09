from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string

from PIL import Image

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import CountVectorizer


def percentage(part, whole):
    return 100 * float(part)/float(whole)

# keyword = input('Please enter keyword or hashtag to search: ')
# noOfTweet = int(input ('Please enter how many tweets to analyze: '))


positive = 0
negative = 0
neutral = 0
polarity = 0

tweet_list = []

neutral_list = []
negative_list = []
positive_list = []


def tweetret(keyword, noOfTweet):
    consumerKey = "7xoPXzuBbqQSdSj5WppOrLM0q"
    consumerSecret = "Dkgn3azOeoFeomriUeWd7hauTxXYczUMwsPFAWjePWOHqovpJH"

    accessToken = "2428603358-iYrImllI5mwabBgrYluH7Vv5S2ukb3ChfvP3c53"
    accessTokenSecret = "e1c3e1Qm8FaZgnBRbnfMIIexq9lccLrzPCjDAfLW8AzPd"

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth)
    tweet_list = []
    tweetcur = tweepy.Cursor(api.search, q=keyword).items(int(noOfTweet))
    for tweet in tweetcur:
        print('\n', tweet.text, '\n')
        tweet_list.append(tweet.text)
    return tweet_list

# Cleaning Text (RT, Punctuation etc)


# Creating new dataframe and new features
def dataframe(tweet_list):
    tw_list = pd.DataFrame(tweet_list)
    tw_list["text"] = tw_list[0]

    # Removing RT, Punctuation etc

    def remove_rt(x): return re.sub('RT @\w+: ', " ", x)

    def rt(x): return re.sub(
        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)

    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] = tw_list.text.str.lower()
    tw_list.head(10)

    tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(
        lambda Text: pd.Series(TextBlob(Text).sentiment))
    positive,negative,neutral = 0,0,0
    for index, row in tw_list['text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        
        if neg > pos:
            tw_list.loc[index, 'sentiment'] = "negative"
            negative+=1
        elif pos > neg:
            tw_list.loc[index, 'sentiment'] = "positive"
            positive+=1
        else:
            tw_list.loc[index, 'sentiment'] = "neutral"
            neutral+=1
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp

    print(tw_list.head(10))
    return tw_list,positive,negative,neutral

def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])

def plotfig(tw_list):
    # create data for Pie Chart
    pichart = count_values_in_column(tw_list, "sentiment")
    names = pichart.index
    size = pichart["Percentage"]

    # Create a circle for the center of the plot
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.pie(size, labels=names, colors=['green', 'blue', 'red'])
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.show()
