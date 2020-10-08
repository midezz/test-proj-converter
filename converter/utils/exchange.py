from exchange.models import Rate


def get_codes():
    rates = Rate.objects.all()
    rate_codes = [r.code for r in rates]
    return ','.join(rate_codes)
