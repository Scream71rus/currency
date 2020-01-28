
import json
import pickle

import tornado.web

from utils.json_encoder import ObjectEncoder
from models.customer_model import CustomerModel

class BaseHandler(tornado.web.RequestHandler):

    @property
    def customer(self):
        return self._customer

    @property
    def db(self):
        return self.application.db

    @property
    def cache(self):
        return self.application.cache

    @property
    def httpclient(self):
        return self.application.httpclient

    @property
    def request_data(self):
        if not hasattr(self, "_request_data"):
            self._request_data = json.loads(self.request.body.decode()) \
                if self.request.body else {}

            self._request_data = dict(filter(lambda i: i[1] != '', self._request_data.items()))

        return self._request_data

    def response(self, data):
        self.set_header('Content-Type', 'application/json')
        data = json.dumps(data, cls=ObjectEncoder)
        self.finish(data)

    def get_cache(self, key):
        value = self.cache.get(key)
        try:
            return pickle.loads(value) if value else None

        except:
            return None

    def set_cache(self, key, value, ex=None):
        value = pickle.dumps(value)
        self.cache.set(key, value, ex=ex)

    async def prepare(self):
        session_key = self.get_cookie("session-key")
        customer_id = self.get_cache("rtb_ui:session_pool:{}".format(session_key))
        self._customer = await CustomerModel.get(customer_id)

        if self.customer is None:
            self.send_error(401)