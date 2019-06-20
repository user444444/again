import pymongo

class Database(object):

    #URI = "mongodb://db:27017"
    URI = "mongodb://127.0.0.1:27017"
    Database = None

    @staticmethod
    def initiaize():
        client = pymongo.MongoClient(Database.URI)
        Database.Database = client["fullstack4"]

    @staticmethod
    def insert(collection,data):
        Database.Database[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.Database[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.Database[collection].find_one(query)


    @staticmethod
    def update(collection,query,update):
        Database.Database[collection].find_one_and_update(query,update)

    @staticmethod
    def remove(collection, query):
        Database.Database[collection].remove(query)




