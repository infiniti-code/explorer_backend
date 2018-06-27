from django.conf.urls import url
from app import urls
from blocks import block_api

urlpatterns = [
url(r'^$',block_api.get_block_details,name="get_block_details")
]
