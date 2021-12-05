from typing import NoReturn
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.forms import Quiz, BasicQuestion, Opisno, PravilnoNepravilno, IzberiOdgovor
from webapp.models import dbQuiz, dbQuestion, dbAnswer

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
        vprasanja = dbQuestion.objects.all()
    except:
        vprasanja = []
    return render(request, "quiz_manager.html", {'kvizi': kvizi, 'vprasanja': vprasanja})

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

        # Nekako je treba dobiti naslov in tip iz templata
        naslov_vprasanja = 'poskus'
        tip = '3'
        form = request.POST

        #opisno vprašanje
        if tip == '1':
            kviz = '1' # Tukaj je treba popraviti, ko ustvarimo povezavo med kvizom in vprašanjem
            number = 1 # Dodaj številčenje vprašanj v bazi
            ime = naslov_vprasanja
            opis = form['opis']
            slika = form['slika'] # Treba še implementirati
            longitude = form['longitude']
            latitude = form['latitude']
            tip = 'opisno'
            vprasanja = form['vprasanje']
            pravilni_odgovori = ''

            dbQuestion.objects.create(kviz=kviz, number=number, ime=ime,
                opis=opis, slika=slika, longitude=float(longitude), latitude=float(latitude),
                type=tip, vprasanja=vprasanja,pravilni_odgovori=pravilni_odgovori)
            return HttpResponseRedirect('/')
        
        #p/n vprašanje
        elif tip == '2':
            kviz = 1 # Tukaj je treba popraviti, ko ustvarimo povezavo med kvizom in vprašanjem
            number = 1 # Dodaj številčenje vprašanj v bazi
            ime = naslov_vprasanja
            opis = form['opis']
            slika = form['slika'] # Treba še implementirati
            longitude = form['longitude']
            latitude = form['latitude']
            tip = 'pravilno-nepravilno'
            vprasanja = [form['trditev1'], form['trditev2'],
                form['trditev3'], form['trditev4'], form['trditev5']]
            pravilni_odgovori = [form['p1'], form['p2'],
                form['p3'], form['p4'], form['p5']]

            dbQuestion.objects.create(kviz=kviz, number=number, ime=ime,
                opis=opis, slika=slika, longitude=float(longitude), latitude=float(latitude),
                type=tip, vprasanja=vprasanja,pravilni_odgovori=pravilni_odgovori)
            return HttpResponseRedirect('/')

        #izbirno vprašanje
        elif tip == '3':
            kviz = 1 # Tukaj je treba popraviti, ko ustvarimo povezavo med kvizom in vprašanjem
            number = 1 # Dodaj številčenje vprašanj v bazi
            ime = naslov_vprasanja
            opis = form['opis']
            slika = form['slika'] # Treba še implementirati
            longitude = form['longitude']
            latitude = form['latitude']
            tip = 'izbirno'
            vprasanja = [form['vprasanje'], form['odgovor1'], 
                form['odgovor2'], form['odgovor3'], 
                form['odgovor4'], form['odgovor5']]
            pravilni_odgovor = form['pravilni_odgovor']
            dbQuestion.objects.create(kviz=kviz, number=number, ime=ime,
                opis=opis, slika=slika, longitude=float(longitude), latitude=float(latitude),
                type=tip, vprasanja=vprasanja,pravilni_odgovori=int(pravilni_odgovor))
            return HttpResponseRedirect('/')
        else: return Exception("Nepravilen tip")
    else:
        form=BasicQuestion()
        return render(request, "question_basic.html", {'form': form, 'title': 'nova vprašanja'})

def add_question_type(request):
    form = request.GET
    naslov_vprasanja = form['ime']
    # opisno vprašanje
    if form['type'][0]=='1':
        return render(request, "question_opisno.html", {'form': Opisno(), 'type': 1, 'naslov_vprasanja': naslov_vprasanja})

    # pravilno/nepravilno
    elif form['type'][0]=='2':
        return render(request, "question_pn.html", {'form': PravilnoNepravilno(), 'type': 2, 'naslov_vprasanja': naslov_vprasanja})
    
    # izbirno 
    elif form['type'][0]=='3':
        return render(request, "question_izbirno.html", {'form': IzberiOdgovor(), 'type': 3, 'naslov_vprasanja': naslov_vprasanja})
    else:
        return Exception("Napačen tip")


