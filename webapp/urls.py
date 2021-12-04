from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_map', views.test_map, name='test_map'),
    path('quiz_manager', views.quiz_manager, name='question_manager'),
    path('add_quiz', views.add_quiz, name='add_quiz'),
    path('add_question', views.add_question, name='add_questions'),
    path('add_question_type', views.add_question_type, name='add_questions_type')
]