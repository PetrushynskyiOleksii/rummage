"""This module provides helper functionality for MongoDB interaction."""

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from .config import MONGO_PORT, MONGO_HOST, MONGO_SERVER_TIMEOUT


__all__ = ['MONGER']


class MongoWorker:
    """Provide functionality for MongoDB interaction."""

    __client = MongoClient(
        host=MONGO_HOST,
        port=MONGO_PORT,
        serverSelectionTimeoutMS=MONGO_SERVER_TIMEOUT
    )
    __instance = None

    def __new__(cls):
        """
        Creates a new instance if not exist, otherwise
        returns reference to already created instance.
        """
        if cls.__instance is None:
            cls.__instance = super(MongoWorker, cls).__new__(cls)

            try:
                cls.__client.admin.command('ismaster')
            except PyMongoError:
                return None

            cls.__database = cls.__client.ifilm_db
            cls.__collections = {
                'films': cls.__database.films,
            }

        return cls.__instance

    def insert_many(self, documents, collection):
        """Insert an iterable of documents to a certain collection."""
        collection = self.__collections.get(collection)

        try:
            documents_ids = collection.insert_many(documents).inserted_ids
        except (PyMongoError, AttributeError):
            # TODO: add logger
            return []

        return [str(document_id) for document_id in documents_ids]

    def filter(self, query_filter, collection, order_by=None, fields=None, limit=0):
        """Retrieve the documents from a certain collection by filter."""
        collection = self.__collections.get(collection)

        try:
            documents = collection.find(
                filter=query_filter,
                sort=order_by,
                projection=fields,
                limit=limit,
            )
        except (PyMongoError, InvalidId, AttributeError, TypeError):
            # TODO: add logger
            return None

        return documents

    def get_by_field(self, field, value, collection):
        """Retrieve a document from a certain collection by specified field."""
        collection = self.__collections.get(collection)

        if field == 'id':
            try:
                query_filter = {'_id': ObjectId(value)}
            except InvalidId:
                return None
        else:
            query_filter = {field: value}

        try:
            document = collection.find_one(query_filter)
        except (PyMongoError, AttributeError):
            # TODO: add logger
            return None

        return document


MONGER = MongoWorker()
