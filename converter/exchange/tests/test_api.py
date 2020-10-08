from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .utils import create_sample_currencys


class TestConverterAPI(TestCase):
    """
    The test converter API endpoint
    """
    def setUp(self):
        self.client = APIClient()
        self.currencys = create_sample_currencys(5)

    def test_success_convert(self):
        """
        Test success convert
        """
        cur_from = self.currencys[1]
        cur_to = self.currencys[3]
        value = 108.2
        params = {
            'from': cur_from.code,
            'to': cur_to.code,
            'value': value
        }
        url = reverse('exchange:convert', kwargs=params)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = resp.data.get('result')
        culc_res = value / cur_from.exchange_rate * cur_to.exchange_rate
        self.assertEqual(round(culc_res, 1), round(float(result), 1))
        self.assertEqual(resp.data.get('name'), cur_from.name)
        self.assertEqual(resp.data.get('code'), cur_from.code)
        self.assertEqual(resp.data.get('to_name'), cur_to.name)
        self.assertEqual(resp.data.get('to_code'), cur_to.code)
        self.assertEqual(float(resp.data.get('value')), value)

    def test_fail_from_convert(self):
        """
        Test unsuccess convert with invalid from currency code
        """
        params = {
            'from': 'usc',
            'to': self.currencys[0].code,
            'value': 10
        }
        url = reverse('exchange:convert', kwargs=params)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_to_convert(self):
        """
        Test unsuccess convert with invalid to currency code
        """
        params = {
            'from': self.currencys[0].code,
            'to': 'cpp',
            'value': 10
        }
        url = reverse('exchange:convert', kwargs=params)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_value_convert(self):
        """
        Test unsuccess convert with invalid value currency
        """
        params = {
            'from': self.currencys[0].code,
            'to': self.currencys[1].code,
            'value': '10a'
        }
        url = reverse('exchange:convert', kwargs=params)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
