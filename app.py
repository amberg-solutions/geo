from flask import Flask, render_template, jsonify
from classes import Map

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/get_map")
def get_map():
    
    html_map = Map.build_html_map()
    return jsonify({"map" : html_map})



if __name__ == '__main__':
    app.run(debug=True, port=8000)