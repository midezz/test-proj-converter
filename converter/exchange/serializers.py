from rest_framework import serializers
from exchange.models import Rate


class ConvertSerializer(serializers.ModelSerializer):
    to_name = serializers.CharField()
    to_code = serializers.CharField()
    value = serializers.DecimalField(
        decimal_places=10,
        max_digits=16,
        coerce_to_string=False
    )
    result = serializers.SerializerMethodField()
    exchange_rate = serializers.HiddenField(default=1)
    rate_second = serializers.HiddenField(default=1)

    class Meta:
        model = Rate
        fields = ('name', 'code', 'value', 'exchange_rate', 'to_name',
                  'to_code', 'result', 'rate_second')

    def get_result(self, instance):
        base_value = instance.value / instance.exchange_rate
        result = instance.rate_second * base_value
        return result
