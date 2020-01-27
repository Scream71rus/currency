
import datetime
import json


class ObjectEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, (datetime.date, datetime.datetime)):
            return datetime.datetime.strftime(value, "%Y-%m-%d %H:%M")

        return json.JSONEncoder.default(self, value)
