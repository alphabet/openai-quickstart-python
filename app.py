from flask import Flask, app, session, redirect, render_template, request, url_for, jsonify
from flask_session import Session
from models import Middleware
from datetime import timedelta

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "beelzebub coughed"


sess = Session()
#Session(app)

@app.before_first_request
def anonymous_function():
  session.permanent = True
  app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)


@app.route("/", methods=("GET", "POST"))
def index():
  return render_template("index.html")

@app.route("/api", methods=(["GET"]))
def api():
  if not "talks" in session: session["talks"]=0
  question = request.args.get('question')
  print("the question is >>>>>>>>>>>", question)
  if question: question.replace("?", "") # and str(question).endswith("?")

  joey3 = Middleware.Joey3(question = question)
  joey3.talks = session["talks"]
  response = joey3.talk()
  session["talks"] += 1 
  response['talks'] = session["talks"]
  response['question'] = question
  
  return jsonify(response)