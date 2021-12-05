from typing import NoReturn
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import logging

from webapp.forms import Quiz, QuestionType, Opisno, PravilnoNepravilno, IzberiOdgovor
from webapp.models import dbQuiz, dbQuestion, OpisnoModel, dbAnswer, PravilnoNepravilnoModel, IzberiOdgovorModel

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html", {})

def test_map(request):
    return render(request, "test_map.html", {})

def quiz_manager(request):
    try:
        kvizi = dbQuiz.objects.all()
    except:
        kvizi = []
    try:
        vprasanja_old = dbQuestion.objects.all()
    except:
        vprasanja_old = []

    vprasanja = []
    vprasanja += OpisnoModel.objects.all()
    vprasanja += PravilnoNepravilnoModel.objects.all()
    vprasanja += IzberiOdgovorModel.objects.all()
    return render(request, "quiz_manager.html", {'kvizi': kvizi, 'vprasanja_old': vprasanja_old, 'vprasanja': vprasanja})

def add_quiz(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Quiz(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            dbQuiz.objects.create(name=form.cleaned_data['ime'], author=form.cleaned_data['avtor'], password=form.cleaned_data['geslo'])
            return HttpResponseRedirect('/')
    else:
        form=Quiz()
        return render(request, "add_quiz.html", {'form': form})

def add_question(request):
    if request.method == 'POST':
        form = request.POST
        form_type = form['form_type']
        logger.error(form_type)


        # GENERIRAMO VPRAŠALNIK GLEDE NA TIP VPRAŠANJA
        if form_type == '1':
            tip_vprasanja = form['type']
            if tip_vprasanja == '1':
                form = Opisno()
            elif tip_vprasanja == '2':
                form = PravilnoNepravilno()
            elif tip_vprasanja == '3':
                form = IzberiOdgovor()
            else:
                form = "error"

            return render(request, "question.html", {'form': form, 'title': 'nova vprašanja'})



        # PROCESIRAMO ODGOVORJEN VPRAŠALNIK
        kviz = 1  # Tukaj je treba popraviti, ko ustvarimo povezavo med kvizom in vprašanjem
        number = 1  # Dodaj številčenje vprašanj v bazi
        opis = form['opis']
        slika = form['slika']  # Treba še implementirati
        longitude = form['longitude']
        latitude = form['latitude']

        #opisno vprašanje
        if form_type == '2':
            tip_vprasanja = 'opisno'
            vprasanje = form['vprasanje']
            pravilni_odgovori = ''
            OpisnoModel.objects.create(opis=opis, slika=slika, longitude=longitude, latitude=latitude,
                                       vprasanje=vprasanje)

        #p/n vprašanje
        elif form_type == '3':
            tip_vprasanja = 'pravilno-nepravilno'
            vprasanje = [form['trditev1'], form['trditev2'],
                form['trditev3'], form['trditev4'], form['trditev5']]
            pravilni_odgovori = [form['p1'], form['p2'],
                form['p3'], form['p4'], form['p5']]
            IzberiOdgovorModel.objects.create(opis=opis, slika=slika, longitude=longitude, latitude=latitude,
                                       vprasanje=vprasanje, pravilni_odgovori = 5)

        #izbirno vprašanje
        elif form_type == '4':
            tip_vprasanja = 'izbirno'
            vprasanje = [form['vprasanje'], form['odgovor1'],
                form['odgovor2'], form['odgovor3'], 
                form['odgovor4'], form['odgovor5']]
            pravilni_odgovori = form['pravilni_odgovor']
            PravilnoNepravilnoModel.objects.create(opis=opis, slika=slika, longitude=longitude, latitude=latitude,
                                       )

        else:
            pravilni_odgovori = []
            return Exception("Nepravilen tip")

        return HttpResponseRedirect('/')



    else:
        # VPRAŠAMO UPORABNIKA KAKŠEN TIP VPRAŠANJA ŽELI
        form = QuestionType()
        return render(request, "question_type.html", {'form': form, 'title': 'nova vprašanja'})


