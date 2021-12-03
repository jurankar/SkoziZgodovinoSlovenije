from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_map', views.test_map, name='test_map'),
    path('question_manager', views.question_manager, name='question_manager'),
    path('add_quiz', views.add_quiz, name='add_quiz')
]