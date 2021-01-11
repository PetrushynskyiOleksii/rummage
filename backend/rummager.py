import pandas as pd
import numpy as np

from ast import literal_eval

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from utils import load_movies

__all__ = ['RUMMAGER']


def _get_director(crew):
    for item in crew:
        if item['job'] == 'Director':
            return item['name']

    return np.nan


def _get_list(data):
    if isinstance(data, list):
        names = [i['name'] for i in data]

        if len(names) > 3:
            names = names[:3]
        return names

    return []


def _clean_data(data):
    if isinstance(data, list):
        return [str.lower(i.replace(" ", "")) for i in data]
    else:
        if isinstance(data, str):
            return str.lower(data.replace(" ", ""))
        else:
            return ''


def _create_soup(data):
    soup = ' '.join(data['keywords'])
    soup += ' ' + ' '.join(data['cast'])
    soup += ' ' + data['director']
    soup += ' ' + ' '.join(data['genres'])

    return soup


class Rummager:
    __instance = None
    movies_df = None

    def __new__(cls):
        if cls.__instance is not None:
            return cls.__instance

        cls.__instance = super(Rummager, cls).__new__(cls)
        cls.movies_df = load_movies()
        cls._prepare_df()

        vectorizer_matrix = cls._get_vectorizer_matrix()
        cls.cosine_matrix = cosine_similarity(vectorizer_matrix, vectorizer_matrix)

        cls.movies_df = cls.movies_df.reset_index()
        cls.indices = pd.Series(cls.movies_df.index, index=cls.movies_df['title'])

        return cls.__instance

    @classmethod
    def _prepare_df(cls):
        cls.movies_df['overview'] = cls.movies_df['overview'].fillna('')

        features = ['cast', 'crew', 'keywords', 'genres']
        for feature in features:
            cls.movies_df[feature] = cls.movies_df[feature].apply(literal_eval)

        cls.movies_df['director'] = cls.movies_df['crew'].apply(_get_director)

        features = ['cast', 'keywords', 'genres']
        for feature in features:
            cls.movies_df[feature] = cls.movies_df[feature].apply(_get_list)

        features = ['cast', 'keywords', 'director', 'genres']
        for feature in features:
            cls.movies_df[feature] = cls.movies_df[feature].apply(_clean_data)

        cls.movies_df['soup'] = cls.movies_df.apply(_create_soup, axis=1)

    @classmethod
    def _get_vectorizer_matrix(cls):
        vectorizer = CountVectorizer(stop_words='english')
        vectorizer_matrix = vectorizer.fit_transform(cls.movies_df['soup'])

        return vectorizer_matrix

    def get_similar(self, title):
        try:
            idx = self.indices[title]
        except KeyError:
            return None

        sim_scores = list(enumerate(self.cosine_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]
        similar = self.movies_df.iloc[movie_indices]

        return similar['title']


RUMMAGER = Rummager()
