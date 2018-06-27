from django.conf.urls import url
from app import urls
from transactions import transaction_api

urlpatterns = [
url(r'^get_transaction_details/$', transaction_api.get_transaction_details, name="get_transaction_details"),
]
