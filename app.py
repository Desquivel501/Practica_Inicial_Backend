from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return ("<h1>Bienvenidos</h1>")

if __name__ == "__main__":
    app.run(threaded=True, port=3000, debug=True)