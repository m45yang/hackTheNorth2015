from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import indicoio
import urllib2
import json
import praw
 
app = Flask(__name__)
 
indicoio.config.api_key = 'e77398fb1e34de03ac0b22d09d5fd21a'
COMMENT_SEARCH_LIMIT = 5
SUBMISSION_SEARCH_LIMIT = 10

@app.route("/", methods=['GET'])
def home():
	return render_template('home.html')

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form['searchName']
	r = praw.Reddit(user_agent='sentimenter')
	subReddits = r.search(searchName)
	score = 0
	searchCommentInd = 0
	searchSubmissionInd = 0
	for s in subReddits:
		comments = s.comments
		for c in comments:
			score += indicoio.sentiment(str(c))
			searchCommentInd += 1
			if (searchCommentInd == COMMENT_SEARCH_LIMIT):
				searchCommentInd = 0
				break
			print(str(c))
		searchSubmissionInd += 1
		if (searchSubmissionInd == SUBMISSION_SEARCH_LIMIT):
			break
	score = score / (COMMENT_SEARCH_LIMIT * SUBMISSION_SEARCH_LIMIT)
	return render_template('search.html', searchName = searchName, score = score, s = str(c))


if __name__ == "__main__":
	app.run(debug=True)