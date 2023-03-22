from flask import Flask, render_template, request
import pandas as pd
import snscrape.modules.twitter as snscrape
import jinja2 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tweets', methods=['POST'])
def tweets():
    # Get search parameters from form
    username = request.form['username']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Define Twitter search query
    query = f'(Data OR Science)(#Data) min_faves:5 until:{end_date} since:{start_date} from:{username} -filter:replies'

    # Scrape Twitter data and store in DataFrame
    tweets = []
    for tweet in snscrape.TwitterSearchScraper(query).get_items():
        if len(tweets) >= 10:
            break
        tweets.append({
            'id': tweet.id,
            'date': tweet.date,
            'source': tweet.source,
            'username': tweet.user.username,
            'content': tweet.content,
            'hashtags': tweet.hashtags,
            'likes': tweet.likeCount
        })
    data = pd.DataFrame(tweets)

    # Pass list of tweet content to template
    return render_template('tweets.html', tweets=data['content'].tolist())

if __name__ == '__main__':
    app.run(debug=True)
