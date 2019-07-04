from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url
from .views import *

urlpatterns = [
    re_path(r'^idcs/(?P<pk>\d+)?/?$',IdcView.as_view()),
    re_path(r'^api_idcs/(?P<pk>\d+)?/?$',APIIDCView.as_view()),
    re_path(r'^racks/(?P<pk>\d+)?/?$',RackView.as_view()),
    re_path(r'^api_racks/(?P<pk>\d+)?/?$',APIRackView.as_view()),
    re_path(r'^servers/(?P<pk>\d+)?/?$',ServerView.as_view()),
    re_path(r'^api_servers/(?P<pk>\d+)?/?$',APIServerView.as_view()),
    url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
    url(r'^api_dashboard/$', APIDashBoardView.as_view(), name='apidashboard'),

]