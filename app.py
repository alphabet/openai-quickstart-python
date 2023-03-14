from flask import Flask, session, redirect, render_template, request, url_for, jsonify
# from flask_session import Session
from models import Middleware

app = Flask(__name__)
app.secret_key = "any random string"
# Check Configuration section for more details
# Session(app)


@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html", result="")

@app.route("/api", methods=(["GET"]))
def api():
    if not "talks" in session: session["talks"]=0
    question = request.args.get("question")
    joey3 = Middleware.Joey3(prompt = question)
    joey3.talks = session["talks"]
    response = joey3.talk()
    session["talks"] += 1 
    
    return jsonify({'joey3': response, 'talks': joey3.talks})
  


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
