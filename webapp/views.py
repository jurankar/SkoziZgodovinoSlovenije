from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html", {})

def test_map(request):
    return render(request, "test_map.html", {})

def question_manager(request):
    return render(request, "question_manager.html", {})

def add_quiz(request):
    return render(request, "add_quiz.html", {})
