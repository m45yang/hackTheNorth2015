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

#choose masterword
print("type in the masterword")
masterWord = input("")
#string sentance segment
totalString = "I love Facebook when it works. I also think the messenger app is really good. Facebook is good "
#totalString = """I thoroughly enjoyed the movie, only a few annoyances with it. I wish they had gone into the fact that the guy (who's name escapes me right now) who said all the oxygen bottles were empty near the top actually had a broken tester, and that those bottles were full.
#I'm glad they didn't make anyone out as a villain, and that it truly was man versus nature."""
#spilt totalString by each sentance
sentenceArray = totalString.split(". ")
newSentenceArray = []
sentimentArray = []
wordArray = []
newWordArray = []
tempSentiArray = []
avgSenti = []
avgSentiArray = []

for i in range(0, len(sentenceArray)) :
    #keep all comments with masterword
    if (masterWord in sentenceArray[i]) :
        #add to new array
        newSentenceArray.append(sentenceArray[i])
 
#turns the sentence array into a large string, then seperates and removes doops
space = " "
jointString = space.join(newSentenceArray)
wordArray = jointString.split()
newWordArray = list(set(wordArray))

#get sediment value for each sentance, then store in array
for i in range(0, len(newSentenceArray)) :
    sentimentArray.append(indicoio.sentiment(newSentenceArray[i]))

#calculate sediment average for ea word based on sentance group
for i in range(0, len(newWordArray)) :
    for j in range(0, len(newSentenceArray)) :
        if (newWordArray[i] in newSentenceArray[j]) :
            tempSentiArray.append(sentimentArray[j])
            avgSenti = sum(tempSentiArray)/len(tempSentiArray)
            avgSentiArray.append(avgSenti)

#find avg of all these values, then output.
if (len(avgSentiArray) > 0) :
    totAvgSenti = sum(avgSentiArray)/len(avgSentiArray)
    print(totAvgSenti)
else :
    print("No master word mentioned in data set")

if __name__ == "__main__":
	app.run(debug=True)