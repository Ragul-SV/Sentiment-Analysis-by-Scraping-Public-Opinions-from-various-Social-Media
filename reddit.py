#!/usr/bin/env python
# coding: utf-8

from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
import langdetect
import string
import re
import pycountry
import praw
import textblob

from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk


def hello():
    return "Hello! Inside the function"


reddit = praw.Reddit(client_id='Dhznns6gONFzwA',
                     client_secret='4M0JphpGxNhEzhrInPZvGsyYKu9O0Q', user_agent='sjghs8gy4oitwkgl')

keyword = None

posts = []


def get_keyword(keyword):
    redditpage = reddit.subreddit(keyword).hot(limit=10)
    posts = []
    try:
        for post in redditpage:
            posts.append([post.title, post.id, post.subreddit,
                          post.url, post.num_comments, post.created])
    except:
        return posts
    return posts


post_id = None


def postid(posts, num):
    post_id = None
    for row in posts:
        if row[4] >= 5:
            post_id = row[1]
            break

    if post_id == None:
        print("No Comments!!!")
    else:
        print(post_id)
    return post_id


comments = []


def submissionfunc(post_id, count):
    comments = []
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    c = int(count)
    for top_level_comment in submission.comments:
        if not c:
            break
        comments.append(top_level_comment.body)
        c -= 1
    return comments


# Cleaning Text (RT, Punctuation etc)

# Creating new dataframe and new features
reddit_df = None


def redditdf(comments):
    reddit_df = pd.DataFrame(comments)
    reddit_df["text"] = reddit_df[0]

    # Removing RT, Punctuation etc
    def remove_rt(x): return re.sub('RT @\w+: ', " ", x)
    def rt(x): return re.sub(
        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)
    reddit_df["text"] = reddit_df.text.map(remove_rt).map(rt)
    reddit_df["text"] = reddit_df.text.str.lower()
    reddit_df[['polarity', 'subjectivity']] = reddit_df['text'].apply(
        lambda Text: pd.Series(TextBlob(Text).sentiment))
    return reddit_df


def percentage(part, whole):
    return 100 * float(part)/float(whole)


positive, neutral, negative = 0, 0, 0


def findsentiment(reddit_df):
    positive = 0
    negative = 0
    neutral = 0
    for index, row in reddit_df['text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        if neg > pos:
            reddit_df.loc[index, 'sentiment'] = "negative"
            negative += 1
        elif pos > neg:
            reddit_df.loc[index, 'sentiment'] = "positive"
            positive += 1
        else:
            reddit_df.loc[index, 'sentiment'] = "neutral"
            neutral += 1

        reddit_df.loc[index, 'neg'] = neg
        reddit_df.loc[index, 'neu'] = neu
        reddit_df.loc[index, 'pos'] = pos
        reddit_df.loc[index, 'compound'] = comp
    return reddit_df, positive, neutral, negative


def resultarray():
    positive_list = []
    negative_list = []
    neutral_list = []
    for index, row in reddit_df.iterrows():
        if row['sentiment'] == 'positive':
            positive_list.append(row["text"])
        if row['sentiment'] == 'negative':
            negative_list.append(row["text"])
        if row['sentiment'] == 'neutral':
            neutral_list.append(row["text"])

    print("------------------------------------Positive-------------------------------------------------")

    for index, i in enumerate(list(positive_list)):
        print(index+1, ')', i)
    print("------------------------------------Negative-------------------------------------------------")
    for index, i in enumerate(list(negative_list)):
        print(index+1, ')', i)
    print("------------------------------------Neutral-------------------------------------------------")
    for index, i in enumerate(list(neutral_list)):
        print(index+1, ')', i)


# Creating new data frames for all sentiments (positive, negative and neutral)
def newdf():
    reddit_df_negative = reddit_df[reddit_df["sentiment"] == "negative"]
    reddit_df_positive = reddit_df[reddit_df["sentiment"] == "positive"]
    reddit_df_neutral = reddit_df[reddit_df["sentiment"] == "neutral"]

# Function for count_values_in single columns


def count_values_in_column():
    data = reddit_df
    feature = "sentiment"
    total = data.loc[:, feature].value_counts(dropna=False)
    percentage = round(data.loc[:, feature].value_counts(
        dropna=False, normalize=True)*100, 2)
    return pd.concat([total, percentage], axis=1, keys=['Total', 'Percentage'])


def plot():
    labels = ['Positive ['+str(positive)+'%]', 'Neutral [' +
              str(neutral)+'%]', 'Negative ['+str(negative)+'%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.style.use('default')
    plt.legend(labels)
    plt.title('Sentiment Analysis Result for keyword= '+keyword+' ')
    plt.axis('equal')
    plt.show()
