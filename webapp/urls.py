from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_map', views.test_map, name='test_map'),
    path('quiz_manager', views.quiz_manager, name='question_manager'),
    path('quiz_manager/<int:kviz>/', views.edit_quiz, name='edit_quiz'),
    path('add_quiz', views.add_quiz, name='add_quiz'),
    path('add_question/<int:kviz>', views.add_question, name='add_questions'),
    path('delete_question/<int:kviz>/<int:vprasanje>/<str:vrsta>', views.delete_question, name='delete_question'),
    path('delete_quiz/<int:kviz>/', views.delete_quiz, name='delete_quiz'),
    path('list_quizes', views.list_quizes, name='list_quizes'),
    path('solve_quiz/<int:kviz>/<int:vprasanje_index>/', views.solve_quiz, name='solve_quiz'),
    path('solve_question/<int:kviz>/<int:vprasanje_id>/<int:vprasanje_index>/', views.solve_question, name='solve_question')
]