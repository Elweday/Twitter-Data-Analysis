from flask import Flask,Blueprint, render_template, flash, request, redirect, url_for, session
import API
from tweepy import errors
from werkzeug.exceptions import HTTPException
import logging
from pandas import read_csv
logging.basicConfig(filename='record.log', level=logging.DEBUG)

validate = API.__validate__
app = Flask(__name__, static_folder='/static')
app.secret_key = 'super secret key'
@app.route("/", methods = ['POST', 'GET'])
def home():
    user_name = ""
    valid = False
    sent = False
    if request.method == 'POST':
        sent = True
        user_name = request.form["user"]
        valid = validate(user_name)
    if valid:
        return  redirect(url_for('u', user = user_name))
    else:
        if sent :
             flash("Twitter User does not exist", 'danger')

    return render_template("index.html", user_name = user_name, valid = valid )

@app.route("/u/<user>")
def u(user):
    if validate(user):
        return render_template("analytics.html", user_name= user, _analysis = API._analysis(API.get_tweets(user)))
    else:
        valid = False
        flash("Twitter User does not exist", 'info')
        return render_template("index.html", user_name = user, valid = valid )

@app.route("/demo")
def _():
    tweets = read_csv("tweets/elonmusk.csv")
    return render_template("analytics.html", user_name= "Elon Musk", _analysis = API._analysis(tweets))

@app.route("/error")
def error():
    msg = session['msg']
    return render_template("err.html", msg = msg)




@app.errorhandler(errors.TweepyException)
def handle_bad_request1(e):
    session['msg'] = "Unable to access TwitterAPI"
    return  redirect(url_for('error'))

@app.errorhandler(KeyError)
def handle_bad_request2(e):
    session['msg'] = "The account you requested has no tweets"
    return redirect(url_for('error'))
def initiate():
    return app
