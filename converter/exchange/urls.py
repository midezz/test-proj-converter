from django.urls import path
from exchange.views import ConvertView


app_name = 'exchange'

urlpatterns = [
    path(
        'convert/<str:from>/<str:to>/<str:value>/',
        ConvertView.as_view(),
        name='convert'
    )
]
