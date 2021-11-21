from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_map', views.test_map, name='test_map'),
]