from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.forms import Kviz
from webapp.models import dbKviz

def index(request):
    return render(request, "index.html", {})

def test_map(request):
    return render(request, "test_map.html", {})

def question_manager(request):

    kvizi = dbKviz.objects.all()

    return render(request, "question_manager.html", {'kvizi': kvizi})

def add_quiz(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Kviz(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            dbKviz.objects.create(name=form.cleaned_data['ime'], author=form.cleaned_data['avtor'], password=form.cleaned_data['geslo'])
            return HttpResponseRedirect('/')
    else:
        form=Kviz()

    return render(request, "add_quiz.html", {'form': form})

def add_questions(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Kviz(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            return HttpResponseRedirect('/')
    else:
        form=Kviz()

    return render(request, "add_quiz.html", {'form': form})

