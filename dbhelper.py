import pymongo
from bson.objectid import ObjectId

DATABASE = "datacollection"

uri = 'mongodb://ahibert:stNW65oh@ds259912.mlab.com:59912/datacollection'


class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient(uri)
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

    # CRUD for texts
    def add_text(self, _id, number, user):
        self.db.append({"_id": number, "number": number, "user": user})
        return number

    def get_texts(self, user_id):
        texts = list(self.db.texts.find({"user": user_id}))
        return texts

    def get_text(self, text_id):
        text = self.db.texts.find_one({"_id": text_id})
        return text

    def update_text(self, _id, text):
        self.db.texts.update({"_id": _id}, {'$set': {"text": text}})

    def delete_text(self, text_id):
        self.db.texts.remove({"_id": text_id})

    # Summary database
    def click_summary(self, user_id, date):
        self.db.summary.insert({"user_id": user_id, "date": date})

    # Login database
    def click_login(self, user_id, date):
        self.db.login.insert({"user_id": user_id, "date": date})

    # Save database
    def click_save(self, user_id, date):
        self.db.save.insert({"user_id": user_id, "date": date})

    # Copy of the text
    def text_version(self, user_id, text, date, status):
        self.db.backups.insert({"user_id": user_id, "date": date, "text": text, "status": status})

    #Are they part of a control group
    def is_control(self, email):
        control = self.db.users.find_one({"email": email})
        return control
