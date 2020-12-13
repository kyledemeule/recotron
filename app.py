from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', active_page="about")

@app.route('/genre')
def genre():
    return render_template(
        'genre.html',
        active_page="genre",
        movie_df=pd.read_csv("static/data/top10_by_genre.csv")
    )

sample_movies = [
    (2918, "Ferris Bueller's Day Off (1986)"),
    (780, 'Independence Day (ID4) (1996)'),
    (1580, 'Men in Black (1997)'),
    (1610, 'Hunt for Red October, The (1990)'),
    (1527, 'Fifth Element, The (1997)'),
    (2699, 'Arachnophobia (1990)'),
    (589, 'Terminator 2: Judgment Day (1991)'),
    (3418, 'Thelma & Louise (1991)'),
    (1, 'Toy Story (1995)'),
    (608, 'Fargo (1996)'),
    (1210, 'Star Wars: Episode VI - Return of the Jedi (1983)'),
    (356, 'Forrest Gump (1994)'),
    (1617, 'L.A. Confidential (1997)'),
    (648, 'Mission: Impossible (1996)'),
    (3114, 'Toy Story 2 (1999)'),
    (1220, 'Blues Brothers, The (1980)'),
    (377, 'Speed (1994)'),
    (1968, 'Breakfast Club, The (1985)'),
    (32, 'Twelve Monkeys (1995)'),
    (2355, "Bug's Life, A (1998)")
]

@app.route('/rating')
def rating():
    return render_template('rating.html',
        active_page="rating",
        sample_movies=sample_movies
    )

@app.route('/rating/recommendation', methods=['POST'])
def rating_recommendation():
    print(request.form)
    movie_df = pd.read_csv(
        "static/data/movies.dat",
        sep="::",
        names=["movie_id", "title", "genres"],
        index_col=0,
        engine="python"
    )
    return render_template('recommendation-result.html',
        reco_movies_df=movie_df.head()
    )

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
