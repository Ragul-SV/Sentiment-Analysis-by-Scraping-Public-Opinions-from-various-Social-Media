# Sentiment-Analysis-of-Twitter-and-Reddit

https://group29sentimentanalyser.herokuapp.com

## Problem Definition:
To create a Web Application that which will do a comparative sentiment analysis by scraping public opinions from various Social Media.

Sentiment Analysis is the understanding the emotion behind the text. This project emphasizes on classifying the natural language text based on how much of the text positive,
negative and neutral. The availability of a lot of public content in social media, blogs, product reviews and e-commerce sites have encouraged a lot of people to express
and publish their opinion online. Social media is the biggest source of them all with massive amount of text content that can be scraped and used for Sentiment Analysis.
The Data used in this project were scraped from Social Media such as Reddit and Twitter by using their respective APIs.

## Software / Tools Used:
Softwares: Jupyter Notebook, Visual Studio Code  
Natural Language Toolkit, Pandas, Numpy, Matplotlib. Tweepy (Twitter Application Programming Interface (API)), TextBlob, PRAW (Reddit API).  
Web development Tools: Flask, Hyper Text Markup Language (HTML), Bootstrap, Cascading Style Sheets (CSS), Heroku.  

## System Requirement Analysis
• To access the tweets the requirement is to use tweepy twitter API, by creating a twitter developer account to get access to this API. Similarly in Reddit, the
requirement is to use PRAW reddit API.  
• To do sentiment analysis, the requirements are  
&nbsp; &nbsp; 1. NLTK toolkit package (nltk.sentiment.vader)  
&nbsp; &nbsp; 2. The function used to find polarity score is SentimentIntensityAnalyzer()  
&nbsp; &nbsp; 3. TextBlob (perform Natural Language Processing (NLP) tasks)  
• matplotlib.pyplot (For Plotting)  
• To create a Webapp the requirements are  
&nbsp; &nbsp; 1. Python (version >3.0)  
&nbsp; &nbsp; 2. Flask 1.1.2 (Back End)  
&nbsp; &nbsp; 3. HTML and CSS (Front End)  
&nbsp; &nbsp; 4. Github and Heroku (For deployment)    
    
## Module Details of the System
1. Social Media Sentiment Analysis  
2. Visualize the Results  
3. Comparative Study of Analysis  
4. Creating a Web Application  

**1) Social Media Sentiment Analysis:** Extract a given number of tweets related to a keywords from Twitter using Twitter’s API, Content from Reddit using Reddit’s API and also Wikipedia article and perform Sentiment Analysis on it.  
For retrieving user comments from reddit we have used PRAW API. By specifying the keyword and number of comments to extract, the API can retrieve top comments from a reddit post related to that keyword. Similarly, for retrieving tweets from twitter, we have used tweepy API. This retrieved data is cleaned (removing punctuation and special symbols). We have used Snowball Stemmer to trim a word to its root(stem) form.  
Then we apply the sentiment intensity analyzer function from the NLTK toolkit to the data and find out the polarity and subjectivity scores. Polarity Scores range from -1 to 1. If it is near to +1, then the sentence is positive. If it is near to -1, then the sentence is negative. If it is not near to either of them, then is it is classified as a neutral sentence.  
This sentiment analyzer function decides the polarity scores by averaging the intensity
of each word. This intensity can be found in the textblob word corpus. Finally, this
result is stored in a Dataframe.  
**2) Visualize the Results:** Visualize the results of the Analysis using pie-chart.  
**3) Comparative Study of Analysis:** Compare the analysis results extracted from both the platforms and present the results.
**4) Creating a Web Application:** Wrap the whole project with a Web Application. In the Home Page of the Web Application, two options are given (Reddit or Twitter), out of which one can be chosen which redirects to the dashboard. In the dashboard, two details are asked (the keyword and the number of comments to be extracted). When these details are entered the backend will run the python code and the sentiment analysis is done. This final dataframe is then displayed as a table in the result page along with a pie chart for visualization.  
