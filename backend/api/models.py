"""This module provides a model for interactions with films data."""

from mongo.worker import MONGER


class Film:
    """The model to interact with films data."""

    collection = 'films'
    fields = [
        'title',
        'overview',
        'release_date',
        'budget',
        'runtime',
        'cast',
        'crew'
    ]

    @classmethod
    def filter_by_title(cls, title, fields=None):
        """Retrieve a film instances by title."""
        query = {'title': {'$regex': title, '$options': '-i'}}
        films = MONGER.filter(
            collection=cls.collection,
            query_filter=query,
            order_by=[('title', 1)],
            fields=fields,
            limit=10,
        )

        return films

    @classmethod
    def get_by_id(cls, object_id):
        """Retrieve a film instance by id."""
        film = MONGER.get_by_field(
            field='id',
            value=object_id,
            collection=cls.collection
        )

        return film

    @classmethod
    def to_dict(cls, film, fields=None):
        """Convert film instance to dictionary representation."""
        if not fields:
            fields = cls.fields

        film_dict = {field: film.get(field) for field in fields}
        film_dict['id'] = str(film.pop('_id'))

        return film_dict

    @classmethod
    def make_document(cls, film_data):
        """Make document for film instance."""
        document = {
            'title': film_data.get('title', ''),
            'overview': film_data.get('overview'),
            'release_date': film_data.get('release_date'),
            'runtime': film_data.get('runtime'),
            'budget': film_data.get('budget'),
            'cast': film_data.get('cast'),
            'crew': film_data.get('crew'),
        }

        return document
