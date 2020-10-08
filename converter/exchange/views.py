from rest_framework.generics import RetrieveAPIView
from exchange.models import Rate
from exchange.serializers import ConvertSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from rest_framework.exceptions import ValidationError


class ConvertView(RetrieveAPIView):
    serializer_class = ConvertSerializer
    queryset = Rate.objects.all()

    def get_object(self):
        convert = get_object_or_404(
            self.queryset,
            code=self.kwargs.get('from')
        )
        second = get_object_or_404(self.queryset, code=self.kwargs.get('to'))
        convert.to_name = second.name
        convert.to_code = second.code
        convert.rate_second = second.exchange_rate
        try:
            convert.value = Decimal(self.kwargs.get('value'))
        except InvalidOperation:
            raise ValidationError('Uncorrect value')
        return convert
