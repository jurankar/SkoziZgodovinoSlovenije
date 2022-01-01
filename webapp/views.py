from django.shortcuts import redirect, render
import logging

from webapp.forms import Quiz, QuestionType, Opisno, PravilnoNepravilno, IzberiOdgovor, OdgovorIzberiOdgovor, OdgovorPravilnoNepravilno, OdgovorOpisno, UporabniskoIme, Prijava, Registracija
from webapp.models import dbQuiz, OpisnoModel, PravilnoNepravilnoModel
from webapp.models import IzberiOdgovorModel, OdgovorIzberiOdgovorModel, OdgovorOpisnoModel, OdgovorPravilnoNepravilnoModel, DatotekaIzberiOdgovorModel, DatotekaOpisnoModel, DatotekaPravilnoNepravilnoModel

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html", {})

def test_map(request):
    return render(request, "test_map.html", {})

# Tega mislim da ne rabimo več
@login_required
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

@login_required
def edit_quiz(request, kviz):
    ime_kviza = dbQuiz.objects.filter(id=kviz)
    avtor = ime_kviza[0].author
    if avtor == str(request.user):
        ime_kviza = ime_kviza[0].name
        vprasanja_opisna = OpisnoModel.objects.filter(kviz = dbQuiz.objects.get(id=kviz))
        vprasanja_izbirna = PravilnoNepravilnoModel.objects.filter(kviz = dbQuiz.objects.get(id=kviz))
        vprasanja_pn = IzberiOdgovorModel.objects.filter(kviz = dbQuiz.objects.get(id=kviz))
        return render(request, "edit_quiz.html", {'kviz': kviz, 'vprasanja_opisna': vprasanja_opisna, 'vprasanja_izbirna': vprasanja_izbirna, 'vprasanja_pn': vprasanja_pn, 'naslov': ime_kviza})    
    else:
        return redirect('/')

@login_required
def add_quiz(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = request.POST
        # check whether it's valid:
        #if form.is_valid():
        #    # process the data in form.cleaned_data as required
        #    # ...
        #    # redirect to a new URL:
        kviz = dbQuiz.objects.create(name=form['ime'], author=str(request.user), password=form['geslo'], datoteka=request.FILES['slika'])
        return redirect('/quiz_manager/' + str(kviz.id) + '/')
    # Mislim da tukaj rabimo samo še POST
    else:
        form=Quiz()
        return render(request, "add_quiz.html", {'form': form})

@login_required
def delete_quiz(request, kviz):
    if dbQuiz.objects.filter(id=int(kviz))[0].author == str(request.user):
        dbQuiz.objects.filter(id=int(kviz)).delete()
        return redirect('/')
    else:
        return redirect('/')

# Tega mislim da ne rabimo več
def list_quizes(request):
    kvizi = dbQuiz.objects.all()
    return render(request, "quiz_list.html", {'kvizi': kvizi})

def solve_quiz(request, kviz, vprasanje_index, username):
    kviz = dbQuiz.objects.filter(id=int(kviz))
    # logger.error(kviz[0].id)

    # vprasanja
    vprasanja = []
    vprasanja += OpisnoModel.objects.filter(kviz__id=kviz[0].id)
    vprasanja += PravilnoNepravilnoModel.objects.filter(kviz__id=kviz[0].id)
    vprasanja += IzberiOdgovorModel.objects.filter(kviz__id=kviz[0].id)
    vprasanja = sorted(vprasanja, key=lambda x: x.leto)

    if len(vprasanja) == 0:
        return redirect('/')
    else:
        vprasanje = vprasanja[vprasanje_index]
    
        # pozicije za vprašanja na časovnem traku (enakomerno razporejene po časovnem traku)
        width = 70
        marginLeft = 15
    
        st_vprasanj = len(vprasanja)
        razmak = 100/st_vprasanj
        pozicijeOznak = []
        for i in range(st_vprasanj):
            pozicijeOznak.append(marginLeft*(2/st_vprasanj) + ((i*razmak) * (width/100)))
        return render(request, "solve_quiz.html", {'kviz': kviz[0], 'width': width, 'height': 100, 'marginLeft': marginLeft, 'stVprasanjRange': range(st_vprasanj), 'pozicijeOznak': pozicijeOznak, 'vprasanje': vprasanje, 'vprasanje_index': vprasanje_index, 'username': username})

def solve_question(request, kviz, vprasanje_id, vprasanje_index, username):
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
            OdgovorOpisnoModel.objects.filter(user=username, vprasanje=vprasanje).delete()
            OdgovorOpisnoModel.objects.create(user=username, vprasanje=vprasanje, odgovori = form['p'])

        elif tip == 'pravilno-nepravilno':
            OdgovorPravilnoNepravilnoModel.objects.filter(user=username, vprasanje=vprasanje).delete()
            OdgovorPravilnoNepravilnoModel.objects.create(user=username, vprasanje=vprasanje, 
                                                odgovori = [form['p1'], form['p2'], form['p3'], form['p4'], form['p5']])

        elif tip == 'izbirno':
            OdgovorIzberiOdgovorModel.objects.filter(user=username, vprasanje=vprasanje).delete()
            OdgovorIzberiOdgovorModel.objects.create(user=username, vprasanje=vprasanje, odgovori = form['p'])

        else: 
            raise Exception("Ni vprašanja")

        sez_vprasanj = []
        sez_vprasanj += OpisnoModel.objects.filter(kviz__id = kviz[0].id)
        sez_vprasanj += PravilnoNepravilnoModel.objects.filter(kviz__id = kviz[0].id)
        sez_vprasanj += IzberiOdgovorModel.objects.filter(kviz__id = kviz[0].id)

        if vprasanje_index + 2 <= len(sez_vprasanj):
            return redirect('/solve_quiz/' + str(kviz[0].id) + '/' + str(vprasanje_index + 1) + '/' + username + '/')
        else:
            return redirect('/solve_quiz/' + str(kviz[0].id) + '/' + str(0) + '/' + username + '/')
    
    else:
        kviz = dbQuiz.objects.filter(id=int(kviz))
        # logger.error(kviz[0].id)
        # vprasanja
        formizbirno = OdgovorIzberiOdgovor()
        formopisno = OdgovorOpisno()
        formpn = OdgovorPravilnoNepravilno()
        
        def v_leto(leto):
            if leto < 0:
                return str(- leto) + ' pr. n. št.'
            else:
                return str(leto)

        vprasanja = []
        slike = []
        vprasanja += OpisnoModel.objects.filter(kviz__id=kviz[0].id, id=vprasanje_id)
        slike += DatotekaOpisnoModel.objects.filter(vprasanje=vprasanje_id)
        if len(vprasanja) > 0: 
            tip = 'opisno'
            if len(slike) > 0:
                return render(request, "solve_question.html", {'leto': v_leto(vprasanja[0].leto), 'kviz': int(kviz[0].id), 'vprasanje': vprasanja[0], 'tip': tip, 'formopisno': formopisno, 'formizbirno': formizbirno, 'formpn': formpn, 'vprasanje_index': vprasanje_index, 'seznam_vprasanj': None, 'username': username, 'slika': slike[0].datoteka})
            else:
                return render(request, "solve_question.html", {'leto': v_leto(vprasanja[0].leto), 'kviz': int(kviz[0].id), 'vprasanje': vprasanja[0], 'tip': tip, 'formopisno': formopisno, 'formizbirno': formizbirno, 'formpn': formpn, 'vprasanje_index': vprasanje_index, 'seznam_vprasanj': None, 'username': username, 'slika': None})

        vprasanja = []
        slike = []
        vprasanja += PravilnoNepravilnoModel.objects.filter(kviz__id=kviz[0].id, id=vprasanje_id)
        slike += DatotekaPravilnoNepravilnoModel.objects.filter(vprasanje=vprasanje_id)
        if len(vprasanja) > 0: 
            tip = 'pn'
            import ast
            seznam_vprasanj = ast.literal_eval(vprasanja[0].vprasanje)
            if len(slike) > 0:
                return render(request, "solve_question.html", {'leto': v_leto(vprasanja[0].leto), 'kviz': int(kviz[0].id), 
                    'vprasanje': vprasanja[0], 'tip': tip, 'formopisno': formopisno, 'formizbirno': formizbirno, 
                    'formpn': formpn, 'vprasanje_index': vprasanje_index, 
                    'v1': seznam_vprasanj[0], 'v2': seznam_vprasanj[1], 'v3': seznam_vprasanj[2], 'v4': seznam_vprasanj[3], 'v5': seznam_vprasanj[4], 'username':username, 'slika': slike[0].datoteka})
            else:
                return render(request, "solve_question.html", {'leto': v_leto(vprasanja[0].leto), 'kviz': int(kviz[0].id), 
                    'vprasanje': vprasanja[0], 'tip': tip, 'formopisno': formopisno, 'formizbirno': formizbirno, 
                    'formpn': formpn, 'vprasanje_index': vprasanje_index, 
                    'v1': seznam_vprasanj[0], 'v2': seznam_vprasanj[1], 'v3': seznam_vprasanj[2], 'v4': seznam_vprasanj[3], 'v5': seznam_vprasanj[4], 'username':username, 'slika': None})

        vprasanja = []
        slike = []
        vprasanja += IzberiOdgovorModel.objects.filter(kviz__id=kviz[0].id, id=vprasanje_id)
        slike += DatotekaIzberiOdgovorModel.objects.filter(vprasanje=vprasanje_id)
        if len(vprasanja) > 0:
            tip = 'izbirno'
            if len(slike) > 0:
                return render(request, "solve_question.html", {'leto': v_leto(vprasanja[0].leto), 'kviz': int(kviz[0].id), 'vprasanje': vprasanja[0], 'tip': tip, 'formopisno': formopisno, 'formizbirno': formizbirno, 'formpn': formpn, 'vprasanje_index': vprasanje_index, 'seznam_vprasanj': None, 'username': username, 'slika': slike[0].datoteka})
            else:
                return render(request, "solve_question.html", {'leto': v_leto(vprasanja[0].leto), 'kviz': int(kviz[0].id), 'vprasanje': vprasanja[0], 'tip': tip, 'formopisno': formopisno, 'formizbirno': formizbirno, 'formpn': formpn, 'vprasanje_index': vprasanje_index, 'seznam_vprasanj': None, 'username': username, 'slika': None})

@login_required
def add_question(request, kviz):
    if dbQuiz.objects.get(id=kviz).author != str(request.user):
        return redirect('/')
    else:
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
            opis = form['opis']
    
            longitude = form['longitude']
            latitude = form['latitude']
            leto = form['leto']
            #opisno vprašanje
            if form_type == '2':
            
                tip_vprasanja = 'opisno'
                #forma = Opisno(request.POST, request.FILES)
                vprasanje = form['vprasanje']
                el = OpisnoModel.objects.create(opis=opis, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                           vprasanje=vprasanje, leto=leto)
                el.save()
                try:
                    DatotekaOpisnoModel.objects.create(datoteka=request.FILES['slika'], vprasanje=el)
                except:
                    pass
            #p/n vprašanje
            elif form_type == '3':
            
                #forma = PravilnoNepravilno(request.POST, request.FILES)
                tip_vprasanja = 'pravilno-nepravilno'
                vprasanje = [form['trditev1'], form['trditev2'],
                    form['trditev3'], form['trditev4'], form['trditev5']]
                pravilni_odgovor = [form['p1'], form['p2'],
                    form['p3'], form['p4'], form['p5']]
                el = PravilnoNepravilnoModel.objects.create(opis=opis, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                           vprasanje=vprasanje, pravilni_odgovor = pravilni_odgovor, leto=leto)
                el.save()
                try:
                    DatotekaPravilnoNepravilnoModel.objects.create(datoteka=request.FILES['slika'], vprasanje=el)
                except:
                    pass
                
            #izbirno vprašanje
            elif form_type == '4':
            
                #forma = IzberiOdgovor(request.POST, request.FILES)
                tip_vprasanja = 'izbirno'
                vprasanje = form['vprasanje']
                pravilni_odgovor = form['pravilni_odgovor']
                el = IzberiOdgovorModel.objects.create(opis=opis, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                            pravilni_odgovor=pravilni_odgovor, vprasanje=vprasanje, odgovor1 = form['odgovor1'], 
                                            odgovor2 = form['odgovor2'], odgovor3 = form['odgovor3'], odgovor4 = form['odgovor4'], odgovor5 = form['odgovor5'], leto=leto)
                el.save()
                try:
                    DatotekaIzberiOdgovorModel.objects.create(datoteka=request.FILES['slika'], vprasanje=el)
                except:
                    pass
                
            else:
                pravilni_odgovori = []
                return Exception("Nepravilen tip")
            return redirect('/quiz_manager/' + str(kviz) + '/')
    
        else:
        
            # VPRAŠAMO UPORABNIKA KAKŠEN TIP VPRAŠANJA ŽELI
            form = QuestionType()
            return render(request, "question_type.html", {'form': form, 'title': 'nova vprašanja', 'kviz': kviz})

@login_required
def delete_question(request, kviz, vprasanje_id, vrsta):
    if dbQuiz.objects.filter(id=int(kviz))[0].author == str(request.user):
        if vrsta == 'opisno':
            OpisnoModel.objects.filter(id=str(vprasanje_id)).delete()
        if vrsta == 'pn':
            PravilnoNepravilnoModel.objects.filter(id=str(vprasanje_id)).delete()
        if vrsta == 'izbirno':
            IzberiOdgovorModel.objects.filter(id=str(vprasanje_id)).delete()
        return redirect('/quiz_manager/' + str(kviz) + '/')
    else: raise InterruptedError

def select_username(request, kviz):
    if not request.user.is_anonymous:
        uporabnisko_ime = str(request.user)
        return redirect('/solve_quiz/' + str(kviz) + '/0/' + uporabnisko_ime + '/')
    else:
        if request.method == 'POST':
            form = request.POST
            uporabnisko_ime = form['p']
            return redirect('/solve_quiz/' + str(kviz) + '/0/' + uporabnisko_ime + '/')
        else:
            form = UporabniskoIme()
            return render(request, "select_username.html", {'kviz': kviz, 'form': form})

def rezultati(request, kviz, username):

    vse_tocke = 0
    zasluzene_tocke = 0

    # Pomožne funkcije
    import ast

    def eval_pn(vprasanje, odgovor):
        vprasanje = getattr(vprasanje, 'pravilni_odgovor')
        odgovor = getattr(odgovor, 'odgovori')
        vprasanje = ast.literal_eval(vprasanje)
        odgovor = ast.literal_eval(odgovor)
        t = 0
        for i in range(len(vprasanje)):
            if vprasanje[i] == odgovor[i]:
                t += 1
        return(t)

    def eval_izbirno(vprasanje, odgovor):
        if str(getattr(vprasanje, 'pravilni_odgovor')) == str(getattr(odgovor, 'odgovori')):
            return(3)
        else: return(0)

    vsa_vprasanja = []
    odgovori = []
    tocke = []
    trenutni = []
    vsa_vprasanja += OpisnoModel.objects.filter(kviz__id=kviz)
    odgovori += OdgovorOpisnoModel.objects.filter(user=username, vprasanje__in=vsa_vprasanja)
    trenutni += OdgovorOpisnoModel.objects.filter(user=username, vprasanje__in=vsa_vprasanja)

    for i in odgovori:
        tocke.append('/')

    vsa_vprasanja = []
    trenutni = []
    vsa_vprasanja += PravilnoNepravilnoModel.objects.filter(kviz__id=kviz)
    odgovori += OdgovorPravilnoNepravilnoModel.objects.filter(user=username, vprasanje__in=vsa_vprasanja)
    trenutni += OdgovorPravilnoNepravilnoModel.objects.filter(user=username, vprasanje__in=vsa_vprasanja)

    for i in trenutni:
        tocke.append(str(eval_pn(i.vprasanje, i)) + '/5')
        zasluzene_tocke += eval_pn(i.vprasanje, i)

    for i in vsa_vprasanja:
        vse_tocke += 5

    vsa_vprasanja = []
    trenutni = []
    vsa_vprasanja += IzberiOdgovorModel.objects.filter(kviz__id=kviz)
    odgovori += OdgovorIzberiOdgovorModel.objects.filter(user=username, vprasanje__in=vsa_vprasanja)
    trenutni += OdgovorIzberiOdgovorModel.objects.filter(user=username, vprasanje__in=vsa_vprasanja)

    for i in trenutni:
        tocke.append(str(eval_izbirno(i.vprasanje, i)) + '/3')
        zasluzene_tocke += eval_izbirno(i.vprasanje, i)

    for i in vsa_vprasanja:
        vse_tocke += 3

    #rezul = zip(odgovori, tocke)
    if vse_tocke > 0:
        rez = str(zasluzene_tocke) + '/' + str(vse_tocke) + ' točk, ' + str(round(100 * zasluzene_tocke/vse_tocke, 1)) + ' %'
    else:
        rez = '0/0 točk, 0.0 %'

    vsa_vprasanja = []
    vsa_vprasanja += OpisnoModel.objects.filter(kviz__id=kviz)
    vsa_vprasanja += PravilnoNepravilnoModel.objects.filter(kviz__id=kviz)
    vsa_vprasanja += IzberiOdgovorModel.objects.filter(kviz__id=kviz)
    vsa_vprasanja = sorted(vsa_vprasanja, key=lambda x: x.leto)

    a = []
    b = []
    c = []
    d = []
    e = []

    def v_leto(leto):
        if leto < 0:
            return str(- leto) + ' pr. n. št.'
        else:
            return str(leto)

    for i in vsa_vprasanja:
        x = False
        y = 0
        for j in odgovori:
            if i == j.vprasanje:
                a.append(v_leto(i.leto))
                c.append(i.vprasanje) 
                b.append(j.odgovori) 
                try:
                    d.append(i.pravilni_odgovor)
                except:
                    d.append('')
                e.append(tocke[y]) 
                x = True
            y += 1
        if not x:
            a.append(v_leto(i.leto))
            c.append(i.vprasanje)
            b.append('')
            try:
                d.append(i.pravilni_odgovor)
            except:
                d.append('')
                e.append('0/0')
            try:
                z = i.odgovor1
                e.append('0/3')
            except:
                e.append('0/5')
            
    rezul = zip(a,b,c,d,e)

    return render(request, "rezultati.html", {'rezultat': rez, 'odgovori': rezul, 'username': username})

@login_required
def edit_question(request, kviz, vprasanje_id):
    if str(request.user) != dbQuiz.objects.filter(id=kviz)[0].author:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = request.POST
            form_type = form['form_type']

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
            opis = form['opis']
            longitude = form['longitude']
            latitude = form['latitude']
            leto = form['leto']

            #opisno vprašanje
            if form_type == '2':
                tip_vprasanja = 'opisno'
                #forma = Opisno(request.POST, request.FILES)
                vprasanje = form['vprasanje']
                el = OpisnoModel.objects.create(opis=opis, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                           vprasanje=vprasanje, leto=leto)
                el.save()
                try:
                    if form['slika'] == '':
                        try:
                            dat = DatotekaOpisnoModel.objects.get(vprasanje = OpisnoModel.objects.get(id=vprasanje_id))
                            dat.vprasanje = el
                            dat.save()
                        except:
                            pass
                except:
                    DatotekaOpisnoModel.objects.create(datoteka=request.FILES['slika'], vprasanje=el)
                OpisnoModel.objects.filter(id=str(vprasanje_id)).delete()

            #p/n vprašanje
            elif form_type == '3':
                #forma = PravilnoNepravilno(request.POST, request.FILES)
                tip_vprasanja = 'pravilno-nepravilno'
                vprasanje = [form['trditev1'], form['trditev2'],
                    form['trditev3'], form['trditev4'], form['trditev5']]
                pravilni_odgovor = [form['p1'], form['p2'],
                    form['p3'], form['p4'], form['p5']]
                el = PravilnoNepravilnoModel.objects.create(opis=opis, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                           vprasanje=vprasanje, pravilni_odgovor = pravilni_odgovor, leto=leto)
                el.save()
                try:
                    if form['slika'] == '':
                        try:
                            dat = DatotekaPravilnoNepravilnoModel.objects.get(vprasanje = PravilnoNepravilnoModel.objects.get(id=vprasanje_id))
                            dat.vprasanje = el
                            dat.save()
                        except:
                            pass
                except:
                    DatotekaPravilnoNepravilnoModel.objects.create(datoteka=request.FILES['slika'], vprasanje=el)
                PravilnoNepravilnoModel.objects.filter(id=str(vprasanje_id)).delete()

            #izbirno vprašanje
            elif form_type == '4':
                #forma = IzberiOdgovor(request.POST, request.FILES)
                tip_vprasanja = 'izbirno'
                vprasanje = form['vprasanje']
                pravilni_odgovor = form['pravilni_odgovor']
                el = IzberiOdgovorModel.objects.create(opis=opis, kviz=dbQuiz.objects.get(id=kviz), longitude=longitude, latitude=latitude,
                                            pravilni_odgovor=pravilni_odgovor, vprasanje=vprasanje, odgovor1 = form['odgovor1'], 
                                            odgovor2 = form['odgovor2'], odgovor3 = form['odgovor3'], odgovor4 = form['odgovor4'], odgovor5 = form['odgovor5'], leto=leto)
                el.save()
                try:
                    if form['slika'] == '':
                        try:
                            dat = DatotekaIzberiOdgovorModel.objects.get(vprasanje = IzberiOdgovorModel.objects.get(id=vprasanje_id))
                            dat.vprasanje = el
                            dat.save()
                        except:
                            pass
                except:
                    DatotekaIzberiOdgovorModel.objects.create(datoteka=request.FILES['slika'], vprasanje=el)
                IzberiOdgovorModel.objects.filter(id=str(vprasanje_id)).delete()
            else:
                return Exception("Nepravilen tip")

            return redirect('/quiz_manager/' + str(kviz) + '/')

        else:    
            kviz = dbQuiz.objects.filter(id=kviz)[0]
            vprasanja = []

            vprasanja += OpisnoModel.objects.filter(id = vprasanje_id)
            if len(OpisnoModel.objects.filter(id = vprasanje_id)) > 0:
                tip = 'opisno'
                try:
                    slika = DatotekaOpisnoModel.objects.filter(vprasanje=vprasanje_id)[0]
                except: slika = None

            vprasanja += PravilnoNepravilnoModel.objects.filter(id = vprasanje_id)
            if len(PravilnoNepravilnoModel.objects.filter(id = vprasanje_id)) > 0:
                tip = 'pn'
                try:
                    slika = DatotekaPravilnoNepravilnoModel.objects.filter(vprasanje=vprasanje_id)[0]
                except:
                    slika = None

            vprasanja += IzberiOdgovorModel.objects.filter(id = vprasanje_id)
            if len(IzberiOdgovorModel.objects.filter(id = vprasanje_id)) > 0:
                tip = 'izbirno'
                try:
                    slika = DatotekaIzberiOdgovorModel.objects.filter(vprasanje=vprasanje_id)[0]
                except: 
                    slika = None

            vprasanje = vprasanja[0]

            if tip == 'opisno':
                if slika != None:
                    form = Opisno(initial={'opis': vprasanje.opis,
                        'longitude': vprasanje.longitude, 'latitude': vprasanje.latitude, 'leto': vprasanje.leto,
                        'vprasanje': vprasanje.vprasanje, 'form_type': 2, 'slika': slika.datoteka})
                else:
                    form = Opisno(initial={'opis': vprasanje.opis,
                        'longitude': vprasanje.longitude, 'latitude': vprasanje.latitude, 'leto': vprasanje.leto, 
                        'vprasanje': vprasanje.vprasanje, 'form_type': 2})                

            elif tip == 'pn':
                import ast
                vsa_vprasanja = getattr(vprasanje, 'vprasanje')
                vsi_odgovori = getattr(vprasanje, 'pravilni_odgovor')
                vsa_vprasanja = ast.literal_eval(vsa_vprasanja)
                vsi_odgovori = ast.literal_eval(vsi_odgovori)

                if slika != None:
                    form = PravilnoNepravilno(initial={'opis': vprasanje.opis,
                        'longitude': vprasanje.longitude, 'latitude': vprasanje.latitude, 
                        'trditev1': vsa_vprasanja[0], 
                        'trditev2': vsa_vprasanja[1], 
                        'trditev3': vsa_vprasanja[2], 
                        'trditev4': vsa_vprasanja[3], 
                        'trditev5': vsa_vprasanja[4], 
                        'p1': vsi_odgovori[0], 
                        'p2': vsi_odgovori[1], 
                        'p3': vsi_odgovori[2], 
                        'p4': vsi_odgovori[3], 
                        'p5': vsi_odgovori[4], 'leto': vprasanje.leto,
                        'form_type': 3, 'slika': slika.datoteka})
                else:
                    form = PravilnoNepravilno(initial={'opis': vprasanje.opis,
                        'longitude': vprasanje.longitude, 'latitude': vprasanje.latitude, 
                        'trditev1': vsa_vprasanja[0], 
                        'trditev2': vsa_vprasanja[1], 
                        'trditev3': vsa_vprasanja[2], 
                        'trditev4': vsa_vprasanja[3], 
                        'trditev5': vsa_vprasanja[4], 
                        'p1': vsi_odgovori[0], 
                        'p2': vsi_odgovori[1], 
                        'p3': vsi_odgovori[2], 
                        'p4': vsi_odgovori[3], 
                        'p5': vsi_odgovori[4], 'leto': vprasanje.leto,
                        'form_type': 3})


            elif tip == 'izbirno':
                if slika != None:
                    form = IzberiOdgovor(initial={'opis': vprasanje.opis,
                        'longitude': vprasanje.longitude, 'latitude': vprasanje.latitude, 
                        'vprasanje': vprasanje.vprasanje, 
                        'odgovor1': vprasanje.odgovor1, 
                        'odgovor2': vprasanje.odgovor2, 
                        'odgovor3': vprasanje.odgovor3, 
                        'odgovor4': vprasanje.odgovor4, 
                        'odgovor5': vprasanje.odgovor5, 'leto': vprasanje.leto,
                        'pravilni_odgovor': vprasanje.pravilni_odgovor,
                        'form_type': 4, 'slika': slika.datoteka})
                else:
                        form = IzberiOdgovor(initial={'opis': vprasanje.opis,
                        'longitude': vprasanje.longitude, 'latitude': vprasanje.latitude, 
                        'vprasanje': vprasanje.vprasanje, 
                        'odgovor1': vprasanje.odgovor1, 
                        'odgovor2': vprasanje.odgovor2, 
                        'odgovor3': vprasanje.odgovor3, 
                        'odgovor4': vprasanje.odgovor4, 
                        'odgovor5': vprasanje.odgovor5, 'leto': vprasanje.leto,   
                        'pravilni_odgovor': vprasanje.pravilni_odgovor,
                        'form_type': 4})

            else: raise NotImplementedError

            return render(request, "edit_question.html", {'kviz': kviz, 'form': form, 'vprasanje': vprasanje})

def homePage(request):
    if request.user.is_anonymous:
        # List quizes
        kvizi = dbQuiz.objects.all()

        form=Quiz()
        return render(request, "index2.html", {'kvizi': kvizi, 'form': form, 'kvizi_edit': []})
    else:
        # List quizes
        kvizi = dbQuiz.objects.all()

        # List quizes of user
        kvizi_uporabnika = dbQuiz.objects.filter(author=str(request.user))

        # Add quiz form
        if request.method == 'POST':
            form = Quiz(request.POST)
            if form.is_valid():
                kviz = dbQuiz.objects.create(name=form.cleaned_data['ime'], author=form.cleaned_data['avtor'], password=form.cleaned_data['geslo'], pictureUrl=form.cleaned_data['slikaUrl'])
                return redirect('/quiz_manager/' + str(kviz.id) + '/')
        else:
            form=Quiz()
            return render(request, "index2.html", {'kvizi': kvizi, 'form': form, 'kvizi_edit': kvizi_uporabnika})

def prijava(request, napaka=False):
    if request.method == 'POST':
        form = request.POST
        uime = form['username']
        geslo = form['password']
        user = authenticate(username=uime, password=geslo)
        if user is not None:
            # Uspešna prijava
            login(request, user)
            return redirect('/')
        else:
            # Neuspešna prijava
            napaka = "Napaka: napačno uporabniško ime ali geslo"
            return redirect('/login/' + str(napaka))
    else:
        return render(request, "prijava.html", {'form_prijava': Prijava(), 'form_reg': Registracija(), 'napaka': napaka})

def registracija(request):

    form = request.POST
    if form['password1'] == form['password2']:
        uime = form['uime']
        geslo = form['password1']
    
        if User.objects.filter(username=uime).exists():
            napaka = "Uporabniško ime je že zasedeno"
            return redirect('/login/' + str(napaka))
    
        elif len(uime) < 5 or len(geslo) < 5:
            napaka = "Uporabniško ime in geslo morata biti daljši od 5 znakov"

            return redirect('/login/' + str(napaka))
        else:
            user = User.objects.create_user(uime, '', geslo)
            login(request, user)
            return redirect('/')
            #return redirect('/')
    
    else:
        napaka = "Gesli se ne ujemata"
        return redirect('/login/' + str(napaka))

@login_required
def izpis(request):
    logout(request)
    return redirect('/')

@login_required
def rezultati_kviza(request, kviz):
    kviz = dbQuiz.objects.get(id=kviz)
    if str(request.user) != kviz.author:
        return('/')
    else:
        vsa_vprasanja = []
        t_v = []
        vse_tocke = 0

        vsa_vprasanja += OpisnoModel.objects.filter(kviz=kviz)
        vsa_vprasanja += PravilnoNepravilnoModel.objects.filter(kviz=kviz)
        t_v += PravilnoNepravilnoModel.objects.filter(kviz=kviz)
        for i in t_v:
            vse_tocke += 5
        t_v = []
        vsa_vprasanja += IzberiOdgovorModel.objects.filter(kviz=kviz)
        t_v += IzberiOdgovorModel.objects.filter(kviz=kviz)
        for i in t_v:
            vse_tocke += 3

        vsa_vprasanja = sorted(vsa_vprasanja, key=lambda x: x.leto)

        slovar_tock = {}
        vsi_odgovori = []
        for i in vsa_vprasanja:
            try:
                vsi_odgovori += OdgovorOpisnoModel.objects.filter(vprasanje=i)
            except:
                pass
            try:
                vsi_odgovori += OdgovorIzberiOdgovorModel.objects.filter(vprasanje=i)
            except:
                pass
            try:
                vsi_odgovori += OdgovorPravilnoNepravilnoModel.objects.filter(vprasanje=i)
            except:
                pass

        for i in vsi_odgovori:
            if i.user in slovar_tock:
                slovar_tock[str(i.user)].append(i)
            else:
                slovar_tock[str(i.user)] = [i]

        # Pomožni funkciji za izračun točk
        import ast
        def eval_pn(vprasanje, odgovor):
            vprasanje = getattr(vprasanje, 'pravilni_odgovor')
            odgovor = getattr(odgovor, 'odgovori')
            vprasanje = ast.literal_eval(vprasanje)
            odgovor = ast.literal_eval(odgovor)
            t = 0
            for i in range(len(vprasanje)):
                if vprasanje[i] == odgovor[i]:
                    t += 1
            return(t)

        def eval_izbirno(vprasanje, odgovor):
            if str(getattr(vprasanje, 'pravilni_odgovor')) == str(getattr(odgovor, 'odgovori')):
                return(3)
            else: return(0)
                 
        rezultati = []
        for i in slovar_tock:
            nov_sez = []
            tocke = 0
            for j in slovar_tock[i]: # j...odgovor
                try:
                    a = j.vprasanje.odgovor1 # izberiodgovormodel
                    tocke += eval_izbirno(j.vprasanje, j)
                except:
                    pass
                try:
                    a = j.vprasanje.pravilni_odgovor # pravilnonepravilno
                    tocke += eval_pn(j.vprasanje, j)
                except:
                    # opisno
                    pass
            if vse_tocke > 0:
                procent = str(round(100 * tocke/vse_tocke, 1)) + ' %'
            else:
                procent = '0.0 %'
            nov_sez.append(i)
            nov_sez.append(vse_tocke)
            nov_sez.append(tocke)
            nov_sez.append(procent)
            rezultati.append(nov_sez)

        sort = sorted(rezultati, key=lambda x: -x[2])
      
        return render(request, "rezultati_kviza.html", {'naslov': kviz.name, 'rezultat': sort})
