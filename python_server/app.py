from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import indicoio
 
app = Flask(__name__)
 
@app.route("/", methods=['GET'])
def home():
	return render_template('home.html')

@app.route("/search", methods=['POST'])
def search():
	searchName = request.form['searchName']
	return render_template('search.html', searchName = searchName)


if __name__ == "__main__":
	app.run(debug=True)