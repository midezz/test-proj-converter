from django.db import models


class Rate(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=4, unique=True)
    exchange_rate = models.DecimalField(decimal_places=10, max_digits=16)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
