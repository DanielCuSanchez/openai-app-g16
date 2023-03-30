import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/images", methods=("GET", "POST"))
def images():
    if request.method == "POST":
        prompt_form = request.form["prompt"]
        quantity_form = request.form["quantity"]
        response = openai.Image.create(
            prompt=prompt_form,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        return redirect(url_for("images", result=image_url))

    result = request.args.get("result")
    return render_template("images.html", image_url=result)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", names=result)


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


