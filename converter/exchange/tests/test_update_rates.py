from .utils import create_sample_currencys
from django.test import TestCase
from unittest.mock import patch
from django.core.management import call_command
import random
from exchange.models import Rate


class Response:
    """
    This class has used as return value when call requests.get
    in tests
    """
    status_code = 200

    def __init__(self, rate_values):
        self.rate_values = {'rates': rate_values}

    def json(self):
        return self.rate_values


class TestUpdateRatesCommand(TestCase):
    """
    Test update exchange rates command
    """
    def setUp(self):
        self.currencys = create_sample_currencys(3)
        self.new_rates = {curr.code: random.randrange(10, 20)
                          for curr in self.currencys}
        self.response = Response(self.new_rates)

    def test_update_rates(self):
        with patch('requests.get') as get:
            get.return_value = self.response
            call_command('update_rates')
            for rate in self.currencys:
                self.assertTrue(
                    Rate.objects.filter(
                        code=rate.code,
                        exchange_rate=self.new_rates[rate.code]
                    ).exists()
                )
