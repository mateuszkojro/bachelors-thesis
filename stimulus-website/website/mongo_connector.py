from pymongo.mongo_client import MongoClient

class MongoConnection:

    @staticmethod
    def from_uri(uri, db_name, collection_name):
        return MongoConnection(MongoClient(uri), db_name, collection_name)

    def __init__(self, mongo_client, db_name, collection_name) -> None:
        # Create a new client and connect to the server
        self.client = mongo_client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_one(self, content):
        self.collection.insert_one(content)
