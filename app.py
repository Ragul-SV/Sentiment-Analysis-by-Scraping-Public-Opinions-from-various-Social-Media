import reddit as rd
import twitter as tw
import os
from PIL import Image
from flask import Flask, render_template, request, session, redirect, flash, send_file
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
app = Flask(__name__)

folder_path = os.path.abspath(__file__+"/../static/images")
print(folder_path)
filelist = [f for f in os.listdir(folder_path) if (
    f.endswith(".png")) or (f.endswith(".jpg"))]
for f in filelist:
    os.remove(os.path.join(folder_path, f))


@ app.route("/", methods=['GET'])
def home():
    return render_template("home.html")


@ app.route("/reddit", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        details = request.form
        keyword = details['keyword']
        num = details['comments']
        posts = rd.get_keyword(keyword)
        post_id = None
        post_id = rd.postid(posts, num)
        if post_id != None:
            comments = rd.submissionfunc(post_id, num)
            reddit_df = rd.redditdf(comments)
            reddit_df, positive, negative, neutral = rd.findsentiment(
                reddit_df)
            arr = reddit_df.to_numpy()
            arr = arr[:, 1:-1]
            labels = ['Positive ['+str(round(positive*100/(positive+negative+neutral),))+'%] '+str(positive)+' comments', 'Neutral [' +
                      str(round(neutral*100/(positive+negative+neutral),))+'%] '+str(neutral)+' comments', 'Negative ['+str(round(negative*100/(positive+negative+neutral),))+'%] '+str(negative)+' comments']
            sizes = [positive, neutral, negative]
            colors = ['yellowgreen', 'blue', 'red']
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.style.use('default')

            plt.legend(labels)
            plt.title('Sentiment Analysis Result for keyword= '+keyword+' ')
            plt.axis('equal')

            plt.savefig('static/images/new_plot.png')
            plt.close()

            return render_template("result.html", d=details, p=posts, arr=arr)
        else:
            return render_template("nosubreddit.html", k=keyword)
    return render_template("dashboard.html")


@ app.route("/twitter", methods=['GET', 'POST'])
def twitterindex():
    if request.method == 'POST':
        details = request.form
        keyword = details['keyword']
        noOfTweet = details['comments']
        tweet_list = tw.tweetret(keyword, noOfTweet)
        tw_list, positive, negative, neutral = tw.dataframe(tweet_list)
        arr = tw_list.to_numpy()
        arr = arr[:, 1:-1]
        labels = ['Positive ['+str(round(positive*100/(positive+negative+neutral), 2))+'%] '+str(positive)+' tweets', 'Neutral [' +
                  str(round(neutral*100/(positive+negative+neutral), 2))+'%] '+str(neutral)+' tweets', 'Negative ['+str(round(negative*100/(positive+negative+neutral),))+'%] '+str(negative)+' tweets']
        sizes = [positive, neutral, negative]
        colors = ['yellowgreen', 'blue', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.style.use('default')
        plt.legend(labels)
        plt.title('Sentiment Analysis Result for keyword= '+keyword+' ')
        plt.axis('equal')
        # pichart = tw.count_values_in_column(tw_list, "sentiment")
        # print(pichart)
        # names = pichart.index
        # size = pichart["Percentage"]
        # my_circle = plt.Circle((0, 0), 0.7, color='white')
        # plt.pie(size, labels=names, colors=['green', 'blue', 'red'])
        # p = plt.gcf()
        # p.gca().add_artist(my_circle)
        plt.savefig('static/images/tweet_plot.png')
        plt.close()
        return render_template("tresult.html", d=details, arr=arr)
    return render_template("tdashboard.html")


if __name__ == '__main__':
    app.secret_key = 'youcantseeme'
    app.run(debug=True)
