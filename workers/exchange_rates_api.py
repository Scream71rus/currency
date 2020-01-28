
import json
from urllib.parse import urlencode

from tornado.options import options
from tornado import httpclient
from tornado.gen import sleep

from models.currency_type_model import CurrencyTypeModel


class ExchangeRatesAPI:
    @property
    def application(self):
        return self._application

    def __init__(self, application=None):
        self._application = application

    async def update_rate(self):
        while True:
            url_params = urlencode({
                'base': options.base_currency,
            })

            request = httpclient.HTTPRequest(options.exchange_rates_url + url_params, method='GET')

            try:
                response = await self.application.httpclient.fetch(request)
            except Exception as ex:
                await sleep(60 * 30)
                continue

            response = json.loads(response.body)
            response_rate = response.get('rates')

            currency_types = await CurrencyTypeModel.get_list()

            for currency_type in currency_types:
                await CurrencyTypeModel.update_rate({
                    'id': currency_type.get('id'),
                    'rate_in_rub': response_rate.get(currency_type.get('name')),
                })

            await sleep(60 * 3)
