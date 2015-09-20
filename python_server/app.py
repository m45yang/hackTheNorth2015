from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
	 render_template, flash
# from flask.ext.uwsgi_websocket import GeventWebSocket
from twilio import twiml
import pymongo
from pymongo import MongoClient
import indicoio
import urllib2
import json
import praw
import statistics
 
app = Flask(__name__)
# websocket = GeventWebSocket(app)

#intialize mongoDB client
mongo = MongoClient('mongodb://localhost:27017/')
db = mongo['test']
messages = db['messages']
 
indicoio.config.api_key = 'e77398fb1e34de03ac0b22d09d5fd21a'
SUBMISSION_SEARCH_LIMIT = 5
RECENT_MESSAGE = 0
UPDATE = 0

@app.route("/", methods=['GET'])
def home():
	score = []
	for message in messages.find():
		score.append(float(message["value"]))
	score = statistics.mean(score)
	return render_template('index.html', score = score)

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form['searchName']
	score = reddit_search(searchName)
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

# @websocket.route('/echo')
# def echo(ws):
#     while True:
#         msg = ws.receive()
#         if msg == "fuck!":
#             ws.send("fuck you too!")

# @websocket.route('/message')
# def message(ws):
# 	while True:
# 		if UPDATE:
# 			UPDATE = 0
# 			new_message = messages.find_one({"_id" : RECENT_MESSAGE})
# 			m = new_message.text + " " + new_message.value
# 			ws.send(m)

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

if __name__ == "__main__":
	app.run(debug=True)