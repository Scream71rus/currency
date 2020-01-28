
import hashlib
import os

from handlers.base_handler import BaseHandler
from models.customer_model import CustomerModel


class Registration(BaseHandler):
    async def post(self):
        password = hashlib.sha256(self.request_data.get('password').encode('utf-8')).hexdigest()

        data = {
            'email': self.request_data.get('email'),
            'password': password,
        }

        data, errors = CustomerModel.create(data)
        if errors is None:
            session_token = os.urandom(24).hex()

            self.set_cache('this_project_customer_%s' % session_token, data.get('id'))
            self.set_cookie('this_project_cookie', session_token)

            self.response({'ok': True})
        else:
            self.response(errors)
