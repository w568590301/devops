#coding=utf-8
from django.conf.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^dbconfig/(?P<pk>\d+)?/?$', DBview.as_view(), name='dbconfig'),
    re_path(r'^inception_check/',InceptionCheckView.as_view(),name='inception_check'),
    re_path(r'^autoselect/', APISelectView.as_view(), name='autoselect'),

]

