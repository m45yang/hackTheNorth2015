from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import indicoio
import urllib2
import json
import praw
 
app = Flask(__name__)
 
indicoio.config.api_key = 'e77398fb1e34de03ac0b22d09d5fd21a'
SEARCH_LIMIT = 100

@app.route("/", methods=['GET'])
def home():
	# print(indicoio.sentiment('indico is so easy to use!'))
	return render_template('home.html')

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form['searchName']
	r = praw.Reddit(user_agent='sentimenter')
	submissions = r.get_subreddit(searchName).get_comments(limit=SEARCH_LIMIT)
	print(indicoio.sentiment([str(x) for x in submissions]))
	return render_template('search.html', searchName = searchName)


if __name__ == "__main__":
	app.run(debug=True)