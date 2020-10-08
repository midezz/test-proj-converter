import requests
from exchange.models import Rate
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.exchange import get_codes


class Command(BaseCommand):
    """
    This command for updating exchange rates in DB
    """
    def handle(self, *args, **options):
        self.stdout.write('Start update exchange rates')
        payload = {
            'app_id': settings.APP_ID,
            'symbols': get_codes(),
            'base': settings.BASE_CURR
        }
        url = 'https://openexchangerates.org/api/latest.json'
        resp = requests.get(url, params=payload)
        if resp.status_code == 200:
            rates = resp.json().get('rates')
            if rates is None:
                self.stdout.write('Error of update exhange rates')
            else:
                for currency in rates:
                    Rate.objects.filter(
                        code=currency).update(
                            exchange_rate=rates.get(currency))
                self.stdout.write('Exhange rates have updated successfully')
        else:
            self.stdout.write('Error of update exhange rates request')
