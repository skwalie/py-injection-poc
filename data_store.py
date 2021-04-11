from pymongo import MongoClient


class DataStore(object):
    def insert(self, subject, collection_name):
        pass

    def get_collection(self, collection_name):
        pass


class MongoStore(DataStore):
    def __init__(self, mongo_configuration):
        self._client = MongoClient(mongo_configuration.connection_string, mongo_configuration.port)
        self._db = self._client[mongo_configuration.db_name]

    def insert(self, subject, collection_name):
        self._db[collection_name].insert_one(subject)
        return subject

    def get_collection(self, collection_name):
        return self._db[collection_name].find({})
