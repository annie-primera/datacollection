from pymongo import MongoClient

DATABASE = "datacollection"

uri = 'mongodb://ahibert:stNW65oh@ds259912.mlab.com:59912/datacollection'


class DBHelper:

    def __init__(self):
        client = MongoClient(uri)
        self.db = client[DATABASE]

    def get_user(self, email):
        return self.db.users.find_one({"email": email})

    def add_user(self, email, salt, hashed):
        self.db.users.insert({"email": email, "salt": salt, "hashed": hashed})

    def insert(self, collection, data):
        return self.db[collection].insert(data)

    # This is supposed to be a staticmethod for some reason but YOLO
    def find_one(self, collection, query):
        return self.db[collection].find_one(query)