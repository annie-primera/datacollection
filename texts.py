import datetime
import uuid
from dbhelper import DBHelper

Database = DBHelper()

class Texts(object):
    def __init__(self, user, title, text, _id=None, date=datetime.datetime.utcnow()):
        self.user = user
        self.date = date
        self.title = title
        self.text = text
        self._id = uuid.uuid4().hex if _id is None else _id

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
    def from_mongo(cls, _id):
        post_data = Database.find_one(collection='texts', query={'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog(_id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]