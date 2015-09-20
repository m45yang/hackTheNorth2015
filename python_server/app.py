from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from flask.ext.uwsgi_websocket import GeventWebSocket
from twilio import twiml
import pymongo
from pymongo import MongoClient
import indicoio
import urllib2
import json
import praw
import statistics
 
app = Flask(__name__)
websocket = GeventWebSocket(app)

#intialize mongoDB client
mongo = MongoClient('mongodb://localhost:27017/')
db = mongo['test']
messages = db['messages']
 
indicoio.config.api_key = 'e77398fb1e34de03ac0b22d09d5fd21a'
SUBMISSION_SEARCH_LIMIT = 5

@app.route("/", methods=['GET'])
def home():
	object = {"hello": "world"}
	return render_template('index.html')

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form['searchName']
	reddit = request.form.get('reddit', default=False, type=bool)
	twitter = request.form.get('twitter', default=False, type=bool)
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

	return str(response)

@app.route("/test_check", methods=['GET','POST'])
def test_check():
	if request.method == 'POST':
		print request.form.getlist('reddit')
	return render_template('test_check.html')

@app.route('/test_ws', methods=['GET'])
def test_ws():
	return render_template('test.html')

@websocket.route('/echo')
def echo(ws):
    while True:
        msg = ws.receive()
        if msg == "fuck!":
            ws.send("fuck you too!")



# TOP THREE BOTTOM THREE
# def three()
# 	temp = list(commentList)
# 	temp.sort()
# 	length = len(temp)

# 	index=0
# 	for i in score:
# 		if (temp[0] == i):
# 			bottom = index
# 		elif (temp[1] == i):
# 			secondBot = index
# 		elif (temp[2] == i):
# 			thirdBot = index
# 		elif (temp[length-3] == i):
# 			thirdTop = index
# 		elif(temp[length-2] == i):
# 			secondTop = index
# 		elif(temp[length-1] == i):
# 			Top = index
# 		index = index + 1


if __name__ == "__main__":
	app.run(debug=True)