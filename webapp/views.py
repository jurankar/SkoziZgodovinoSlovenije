from typing import NoReturn
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import logging
import json

from webapp.forms import Quiz, QuestionType, Opisno, PravilnoNepravilno, IzberiOdgovor, OdgovorIzberiOdgovor, OdgovorPravilnoNepravilno, OdgovorOpisno
from webapp.models import dbQuiz, OpisnoModel, PravilnoNepravilnoModel, IzberiOdgovorModel, OdgovorIzberiOdgovorModel, OdgovorOpisnoModel, OdgovorPravilnoNepravilnoModel

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html", {})

def test_map(request):
    return render(request, "test_map.html", {})

def quiz_manager(request,kviz=None):
    try:
        kvizi = dbQuiz.objects.all()
    except:
        kvizi = []
    vprasanja = []
    vprasanja += OpisnoModel.objects.all()
    vprasanja += PravilnoNepravilnoModel.objects.all()
    vprasanja += IzberiOdgovorModel.objects.all()

    odgovori = []
    odgovori += OdgovorOpisnoModel.objects.all()
    odgovori += OdgovorPravilnoNepravilnoModel.objects.all()
    odgovori += OdgovorIzberiOdgovorModel.objects.all()

    return render(request, "quiz_manager.html", {'kvizi': kvizi, 'vprasanja': vprasanja, 'odgovori': odgovori})

def edit_quiz(request, kviz):
    ime_kviza = dbQuiz.objects.filter(id=kviz)
    ime_kviza = ime_kviza[0].name
    vprasanja_opisna = OpisnoModel.objects.filter(kviz = dbQuiz.objects.get(id=kviz))
    vprasanja_izbirna = PravilnoNepravilnoModel.objects.filter(kviz = dbQuiz.objects.get(id=kviz))
    vprasanja_pn = IzberiOdgovorModel.objects.filter(kviz = dbQuiz.objects.get(id=kviz))
    return render(request, "edit_quiz.html", {'kviz': kviz, 'vprasanja_opisna': vprasanja_opisna, 'vprasanja_izbirna': vprasanja_izbirna, 'vprasanja_pn': vprasanja_pn, 'naslov': ime_kviza})    

def add_quiz(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Quiz(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            kviz = dbQuiz.objects.create(name=form.cleaned_data['ime'], author=form.cleaned_data['avtor'], password=form.cleaned_data['geslo'])
            return redirect('/quiz_manager/' + str(kviz.id) + '/')
    else:
        form=Quiz()
        return render(request, "add_quiz.html", {'form': form})

def delete_quiz(request, kviz):
    dbQuiz.objects.filter(id=int(kviz)).delete()
    return redirect('/quiz_manager')

def list_quizes(request):
    kvizi = dbQuiz.objects.all()
    return render(request, "quiz_list.html", {'kvizi': kvizi})

def solve_quiz(request, kviz, vprasanje_index):
    kviz = dbQuiz.objects.filter(id=int(kviz))
    # logger.error(kviz[0].id)

    # vprasanja
    vprasanja = []
    vprasanja += OpisnoModel.objects.filter(kviz__id=kviz[0].id)
    vprasanja += PravilnoNepravilnoModel.objects.filter(kviz__id=kviz[0].id)
    vprasanja += IzberiOdgovorModel.objects.filter(kviz__id=kviz[0].id)
    vprasanje = vprasanja[vprasanje_index]

    # pozicije za vprašanja na časovnem traku (enakomerno razporejene po časovnem traku)
    st_vprasanj = len(vprasanja)
    razmak = 100/st_vprasanj
    pozicijeOznak = []
    for i in range(st_vprasanj):
        pozicijeOznak.append(i*razmak)

    return render(request, "solve_quiz.html", {'kviz': kviz[0], 'width':70, 'height':100, 'marginLeft':15, 'st_vprasanj':range(st_vprasanj), 'pozicijeOznak':pozicijeOznak, 'vprasanje': vprasanje, 'vprasanje_index': vprasanje_index})

def solve_question(request, kviz, vprasanje_id, vprasanje_index):
    if request.method == 'POST':
        form = request.POST
        kviz = dbQuiz.objects.filter(id=int(kviz))

        vprasanja = []
        tipi = []

        vprasanja += OpisnoModel.objects.filter(id = vprasanje_id)
        if len(vprasanja) > 0:
            tipi.append('opisno')
        vprasanja += PravilnoNepravilnoModel.objects.filter(id = vprasanje_id)
        if len(vprasanja) > 0:
            tipi.append('pravilno-nepravilno')
        vprasanja += IzberiOdgovorModel.objects.filter(id = vprasanje_id)
        if len(vprasanja) > 0:
            tipi.append('izbirno')
        vprasanje = vprasanja[0]
        tip = tipi[0]
        if tip == 'opisno':
            OdgovorOpisnoModel.objects.create(user="Implementiraj", vprasanje=vprasanje, odgovori = form['p'])

        elif tip == 'pravilno-nepravilno':
            OdgovorPravilnoNepravilnoModel.objects.create(user="Implementiraj", vprasanje=vprasanje, 
                                                odgovori = [form['p1'], form['p2'], form['p3'], form['p4'], form['p5']])

        elif tip == 'izbirno':
            OdgovorIzberiOdgovorModel.objects.create(user="Implementiraj", vprasanje=vprasanje, odgovori = form['p'])

        else: 
            raise Exception("Ni vprašanja")

        return redirect('/solve_quiz/' + str(kviz[0].id) + '/' + str(vprasanje_index) + '/')
    else:
        kviz = dbQuiz.objects.filter(id=int(kviz))
        # logger.error(kviz[0].id)
        # vprasanja
        tip = []
        vprasanja = []
        vprasanja += OpisnoModel.objects.filter(kviz__id=kviz[0].id, id=vprasanje_id)
        if len(vprasanja) > 0: 
            tip.append('opisno')
        formopisno = OdgovorOpisno()

        vprasanja += PravilnoNepravilnoModel.objects.filter(kviz__id=kviz[0].id, id=vprasanje_id)
        if len(vprasanja) > 0: tip.append('pn')
        formpn = OdgovorPravilnoNepravilno()

        vprasanja += IzberiOdgovorModel.objects.filter(kviz__id=kviz[0].id, id=vprasanje_id)
        if len(vprasanja) > 0: tip.append('izbirno')
        formizbirno = OdgovorIzberiOdgovor()

        return render(request, "solve_question.html", {'kviz': int(kviz[0].id), 'vprasanje': vprasanja[0], 'tip': tip[0], 'formopisno': formopisno, 'formizbirno': formizbirno, 'formpn': formpn, 'vprasanje_index': vprasanje_index})


def add_question(request, kviz):
    if request.method == 'POST':
        form = request.POST
        form_type = form['form_type']
        # logger.error(form_type)

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

            return render(request, "question.html", {'form': form, 'title': 'nova vprašanja', 'kviz': kviz})

        # PROCESIRAMO ODGOVORJEN VPRAŠALNIK
        number = 1  # Dodaj številčenje vprašanj v bazi
        opis = form['opis']
        slika = form['slika']  # Treba še implementirati
        longitude = form['longitude']
        latitude = form['latitude']

        #opisno vprašanje
        if form_type == '2':
            tip_vprasanja = 'opisno'
            vprasanje = form['vprasanje']
            OpisnoModel.objects.create(opis=opis, slika=slika, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                       vprasanje=vprasanje)

        #p/n vprašanje
        elif form_type == '3':
            tip_vprasanja = 'pravilno-nepravilno'
            vprasanje = [form['trditev1'], form['trditev2'],
                form['trditev3'], form['trditev4'], form['trditev5']]
            pravilni_odgovor = [form['p1'], form['p2'],
                form['p3'], form['p4'], form['p5']]
            PravilnoNepravilnoModel.objects.create(opis=opis, slika=slika, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                       vprasanje=vprasanje, pravilni_odgovor = pravilni_odgovor)

        #izbirno vprašanje
        elif form_type == '4':
            tip_vprasanja = 'izbirno'
            vprasanje = [form['vprasanje'], form['odgovor1'],
                form['odgovor2'], form['odgovor3'], 
                form['odgovor4'], form['odgovor5']]
            pravilni_odgovor = form['pravilni_odgovor']
            IzberiOdgovorModel.objects.create(opis=opis, slika=slika, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                        pravilni_odgovor=pravilni_odgovor)

        else:
            pravilni_odgovori = []
            return Exception("Nepravilen tip")

        return redirect('/quiz_manager/' + str(kviz) + '/')

    else:
        # VPRAŠAMO UPORABNIKA KAKŠEN TIP VPRAŠANJA ŽELI
        form = QuestionType()
        return render(request, "question_type.html", {'form': form, 'title': 'nova vprašanja', 'kviz': kviz})

def delete_question(request, kviz, vprasanje, vrsta):
    if vrsta == 'opisno':
        OpisnoModel.objects.filter(id=str(vprasanje)).delete()
    elif vrsta == 'pn':
        PravilnoNepravilnoModel.objects.filter(id=vprasanje).delete()
    elif vrsta == 'izbirno':
        IzberiOdgovorModel.objects.filter(id=vprasanje).delete()
    return redirect('/quiz_manager/' + str(kviz) + '/')