from flask import current_app
from blinker import Namespace
from dbhelper import DBHelper
import datetime

DB = DBHelper

emitting_signal = Namespace()


def summary_signal(user_id):
    DB.click_summary(user_id, date=datetime.datetime.utcnow())


summary = emitting_signal.signal('summary_signal')

summary.connect(summary_signal, current_app)