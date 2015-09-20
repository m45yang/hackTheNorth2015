from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from twilio import twiml
import pymongo
from pymongo import MongoClient
import indicoio
import urllib2
import json
import praw
import statistics
import twitter
 
app = Flask(__name__)

#intialize mongoDB client
mongo = MongoClient('mongodb://localhost:27017/')
db = mongo['test']
messages = db['messages']
 
indicoio.config.api_key = 'e77398fb1e34de03ac0b22d09d5fd21a'
SUBMISSION_SEARCH_LIMIT = 5
NUMBER_TWEETS = 50
RECENT_MESSAGE = 0
UPDATE = 0

consumer_key='2X3zyVXZEyES5Ks4gdgIH7rJb'
consumer_secret='2PpVLZNyzFE8AT9TDPAt9cdr1C7fC4zDIQ91PBG3oXdT5K8yY0'
access_token_key='2827298030-oerojVBfa4eviORV0MrNKvj8EkA15u4vATvuO62'
access_token_secret='jx1u9fwOYdhZUzFyXmqZJtN3VLD3c5Hbqb6XhOkF7VhEt'

api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

@app.route("/", methods=['GET'])
def home():
	score = []
	for message in messages.find():
		score.append(float(message["value"]))
	score = statistics.mean(score)
	return render_template('index.html', score = score)

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form["searchName"]
	score = (reddit_search(searchName) + tweety_search(searchName)) / 2 * 100
	score = "{0:.2f}".format(score)
	return jsonify(searchName = searchName, score = score)

@app.route('/sms', methods=['GET'])
def show():
	messageArray = []
	valueArray = []
	for message in messages.find():
		messageArray.append(message["text"])
		valueArray.append(message["value"])
	return render_template('show.html', messageArray = messageArray, valueArray = valueArray)

@app.route('/sms', methods=['POST'])
def sms():
	response = twiml.Response()
	body = request.form['Body']
	print(body)
	value = indicoio.sentiment_hq(body)
	print(value)
	response.message("You sent: {0}\nSentiment analysis: {1}".format(body, value))
	data = {
		"text": body,
		"value": value
	}
	messages.insert_one(data)
	print('here1')
	UPDATE = 1
	print('here2')
	return str(response)

@app.route("/test_check", methods=['GET','POST'])
def test_check():
	if request.method == 'POST':
		print request.form.getlist('reddit')
	return render_template('test_check.html')

@app.route('/test_ws', methods=['GET'])
def test_ws():
	return render_template('test.html')

def reddit_search(searchName):
	searchName = request.form['searchName']
	r = praw.Reddit(user_agent='sentimenter')
	submissions = r.search(searchName)
	score = []
	commentList = []
	for searchSubmissionInd, submission in enumerate(submissions):
		submission.replace_more_comments(limit=1, threshold=1)
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:
			commentList.append(comment.body)
		print("Grabbing comments from reddit thread: " + submission.short_link)
		if (searchSubmissionInd +1 == SUBMISSION_SEARCH_LIMIT):
			break
	score = statistics.mean(indicoio.sentiment_hq(commentList))
	return score

def tweety_search(searchName):
	tweet_list = []
	search = api.GetSearch(term=searchName, lang='en', result_type='recent', count=NUMBER_TWEETS, max_id='')
	for t in search:
		tweet_list.append(t.text.encode('utf-8'))
	score = statistics.mean(indicoio.sentiment_hq(tweet_list))
	return score

if __name__ == "__main__":
	app.run(debug=True)