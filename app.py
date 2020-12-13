from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

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

def center_vector(v):
    v_copy = v.copy()
    v_mean = v.sum() / (v != 0).sum()
    for v_i, val in enumerate(v):
        if val != 0:
            v_copy[v_i] = val - v_mean
    return(v_copy)

def centered_cosine_similarity(v1, v2):
    if np.linalg.norm(v2) == 0:
        return 0
    return np.matmul(v1.T, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@app.route('/rating/recommendation', methods=['POST'])
def rating_recommendation():
    movie_ids = request.form.getlist("movie_ids[]")
    movie_ratings = request.form.getlist("movie_ratings[]")
    # read in the movie list
    movie_df = pd.read_csv(
        "static/data/movies.dat",
        sep="::",
        names=["movie_id", "title", "genres"],
        index_col=0,
        engine="python"
    )
    # generate movie lookup
    movie_lookup = {}
    movie_rev_lookup = {}
    i = 0
    for index, row in movie_df.iterrows():
        movie_lookup[index] = i
        movie_rev_lookup[i] = index
        i += 1
    n_movies = len(movie_lookup)
    # generate new user vector
    new_user_rating = np.zeros(n_movies)
    for movie_id, movie_rating in zip(movie_ids, movie_ratings):
        new_user_rating[movie_lookup[int(movie_id)]] = float(movie_rating)
    new_user_rating_centered = center_vector(new_user_rating)
    # calculate new user weights
    movie_rating_matrix_centered = np.load('static/data/movie_rating_matrix_centered.npy')
    new_user_weights = np.array([
        centered_cosine_similarity(new_user_rating_centered, user_vector)
        for user_vector
        in movie_rating_matrix_centered
    ])
    movie_rating_matrix_centered = None # allow GC if memory is short
    # calculate rankings
    movie_estimate_matrix_centered = np.load('static/data/movie_estimate_matrix_centered.npy')
    n_est = (movie_estimate_matrix_centered.T * new_user_weights).T
    n_est = n_est.sum(axis=0)
    sorted_movies = list(np.argsort(n_est))
    # argsort sorts in ascending order
    sorted_movies.reverse()
    movie_recs = [movie_rev_lookup[m_id] for m_id in sorted_movies]
    return render_template('recommendation-result.html',
        reco_movies_df=movie_df.loc[movie_recs[:10]]
    )

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
