import json

from flask import Blueprint, Response

from rummager import RUMMAGER
from .models import Film


RUMMAGE = Blueprint('rummage', __name__)


def custom_response(status_code, response=None):
    """Return custom response in JSON format."""
    response = Response(
        mimetype='application/json',
        response=json.dumps(response, ensure_ascii=False),
        status=status_code
    )

    return response


@RUMMAGE.route('/search', methods=['GET'])
@RUMMAGE.route('/search/<string:title>', methods=['GET'])
def search(title=''):
    films = Film.filter_by_title(title, fields=['title'])
    if not films:
        return custom_response(400)

    films = [Film.to_dict(film, ['title']) for film in films]
    return custom_response(200, films)


@RUMMAGE.route('/films/<string:film_id>')
def get_films(film_id):
    film = Film.get_by_id(film_id)
    if not film:
        response = 'Not found a film with such id'
        return custom_response(400, response)

    film = Film.to_dict(film)
    return custom_response(200, film)


@RUMMAGE.route('/similar/<string:title>')
def get_similar(title):
    similar = RUMMAGER.get_similar(title)
    if similar is None:
        response = 'Not found a film with such title'
        return custom_response(400, response)

    titles = '|'.join(similar)
    query_filter = f'({titles})'

    films = Film.filter_by_title(query_filter, fields=['title'])
    films = [Film.to_dict(film, ['title']) for film in films]

    return custom_response(200, films)
