from exchange.models import Rate
import string
import random


def create_sample_currencys(number):
    """
    This function for create random currencys in DB
    """
    currencys_ar = []
    for _ in range(number):
        currencys_ar.append({
            'name': ''.join(random.choices(string.ascii_lowercase, k=8)),
            'code': ''.join(random.choices(string.ascii_uppercase, k=3)),
            'exchange_rate': random.randrange(1000, 10000) / 100
        })
    currencys = [Rate(**r) for r in currencys_ar]
    return Rate.objects.bulk_create(currencys)
