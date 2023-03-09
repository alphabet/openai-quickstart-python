from flask import Flask, redirect, render_template, request, url_for, jsonify
from models import Middleware

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        form_input = request.form["animal"]
        joey3 = Middleware.Joey3()
        joey3.prompt = form_input
        response = joey3.talk()

        #return redirect(url_for("index", result=response.choices[0].text))
        return redirect(url_for("index", result=response))

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/api", methods=(["GET"]))
def api():
    form_input = request.form["animal"]
    joey3 = Middleware.Joey3({'prompt': form_input})
    response = joey3.talk()
    return jsonify({'joey3': response})
  


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
