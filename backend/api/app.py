"""This module provides starting Flask app."""

import logging

from flask import Flask
from flask_cors import CORS


logger = logging.getLogger('RUMMAGE')


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app)
    logger.info('Flask APP instantiated.')

    from mongo.worker import MONGER
    if not MONGER:
        logger.error('Mongo DB connection failed.')
    logger.info('Mongo DB connected.')

    from rummager import RUMMAGER
    logger.info('Recommendation engine loaded.')

    from api.views import RUMMAGE
    flask_app.register_blueprint(RUMMAGE, url_prefix='/api/v1/')
    logger.info('Routes configured.')

    return flask_app
