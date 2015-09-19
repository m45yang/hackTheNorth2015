from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
 
app = Flask(__name__)
 
@app.route("/", methods=['GET'])
def home():
	return render_template('home.html')

 


if __name__ == "__main__":
	app.run(debug=True)