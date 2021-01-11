import os
import json

import pandas as pd

from api.models import Film
from mongo.worker import MONGER


BASE_DIR = os.path.dirname(__file__)
DATASETS_DIR = BASE_DIR + '/datasets/'
TMDB_CREDITS = 'tmdb_5000_credits.csv'
TMDB_MOVIES = 'tmdb_5000_movies.csv'


def load_movies():
    credits_csv = pd.read_csv(DATASETS_DIR + TMDB_CREDITS)
    movies_csv = pd.read_csv(DATASETS_DIR + TMDB_MOVIES)

    credits_csv.columns = ['id', 'tittle', 'cast', 'crew']
    movies = movies_csv.merge(credits_csv, on='id')

    return movies


def populate_db():
    movies = load_movies()

    documents = []
    for movie in movies.itertuples():
        movie_data = {}
        for field in Film.fields:
            value = getattr(movie, field, None)
            if field in ['cast', 'crew']:
                value = json.loads(value)

            movie_data[field] = value

        document = Film.make_document(movie_data)
        documents.append(document)

    MONGER.insert_many(documents, Film.collection)
