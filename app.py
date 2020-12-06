from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', active_page="about")

@app.route('/genre')
def genre():
    return render_template('genre.html', active_page="genre")

@app.route('/rating')
def rating():
    return render_template('rating.html', active_page="rating")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
