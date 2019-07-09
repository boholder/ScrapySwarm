from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('refreshdata', getData),
    path('startsipder', start_spider),
    path('test',test)
]
