from django.conf.urls import url
from app import urls
from addresses import address_api

urlpatterns = [

url(r'^get_address_details/$', address_api.get_address_details, name="get_address_details"),
url(r'^get_full_address_details/$', address_api.get_full_address_details, name="get_full_address_details"),

url(r'^test/$',address_api.test),

]
