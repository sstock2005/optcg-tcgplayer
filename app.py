from flask import Flask, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from tcgplayer_api import analyze, as_currency

app = Flask(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])

limiter.init_app(app) 

@app.route("/", methods=["GET"])
def index():
    return render_template("optcg.html", deck_text="")

@app.route("/calculate", methods=["POST"])
@limiter.limit("25 per minute")
def calculate():
    deck_text = request.form.get("deck", "")
    deck_lines = deck_text.splitlines()
    total, errors = analyze(deck_lines)
    result = as_currency(total)
    return jsonify(result=result, errors=errors, deck_text=deck_text)

if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)
