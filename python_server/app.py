from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from twilio import twiml
import pymongo
from pymongo import MongoClient
import indicoio
import urllib2
import json
import praw
import statistics
 
app = Flask(__name__)

#intialize mongoDB client
mongo = MongoClient('localhost', 27017)
db = mongo.test_database
messages = db.messages

 
indicoio.config.api_key = 'e77398fb1e34de03ac0b22d09d5fd21a'
SUBMISSION_SEARCH_LIMIT = 5

@app.route("/", methods=['GET'])
def home():
	return render_template('home.html')

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form['searchName']
	r = praw.Reddit(user_agent='sentimenter')
	submissions = r.search(searchName)
	score = []
	searchSubmissionInd = 0
	commentList = []
	for submission in submissions:
		submission.replace_more_comments(limit=1, threshold=1)
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:
			commentList.append(comment.body)
		print(commentList)
		searchSubmissionInd += 1
		if (searchSubmissionInd == SUBMISSION_SEARCH_LIMIT):
			break
	score = statistics.mean(indicoio.sentiment_hq(commentList))
	return render_template('search.html', searchName = searchName, score = score)

@app.route('/sms', methods=['GET'])
def show():
	return render_template('show.html')


@app.route('/sms', methods=['POST'])
def sms():
	response = twiml.Response()
	body = request.form['Body']
	print(body)
	value = indicoio.sentiment_hq(body)
	print(value)
	object = {
		"text": body,
		"value": value
	}
	object_id = messages.insert_one(object)

	response.message("You sent: {0}\nSentiment analysis: {1}".format(body, value))

	return str(response)

if __name__ == "__main__":
	app.run(debug=True)