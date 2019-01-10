import datetime
from dbhelper import DBHelper

Database = DBHelper()

class Texts(object):
    def __init__(self, user, title, text, date=datetime.datetime.utcnow()):
        self.user = user
        self.date = date
        self.title = title
        self.text = text

    def save_to_db(self):
        Database.insert(collection='texts',
                        data=self.json())

    def json(self):
        return {
            'user': self.user,
            'text': self.text,
            'title': self.title,
            'created_date': self.date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]