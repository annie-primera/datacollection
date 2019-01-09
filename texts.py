import datetime
from dbhelper import DBHelper

class Texts(object):
    def __init__(self, user, title, text, date=datetime.datetime.utcnow()):
        self.user = user
        self.date = date
        self.title = title
        self.text = text

    def save_to_db(self):
        DBHelper.insert(collection='texts',
                        data=self.json)