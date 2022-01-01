from django import forms

class Quiz(forms.Form):
    ime = forms.CharField(label='ime kviza', max_length=200)
    #avtor = forms.CharField(label='avtor kviza', max_length=200)
    geslo = forms.CharField(widget=forms.HiddenInput(), max_length=200)   # removed widget=forms.PasswordInput()  --> Can we remove this?
    slika = forms.FileField(
        label='izberi naslovno sliko kviza', required=True
    )
    #slikaUrl = forms.CharField(label='url slike', max_length=200)
    form_type = forms.IntegerField(label='form type', initial=0, widget=forms.HiddenInput())

class QuestionType(forms.Form):
    type = forms.ChoiceField(choices=[(1, 'opisno'), (2, 'p/n'), (3, 'izbirno')])  # tip vprašanja (true-false, izberi pravilni odgovor, opisni tip odgovora, izberi vse pravile odgovore,...)
    form_type = forms.IntegerField(label='form type', initial=1, widget=forms.HiddenInput())

class Opisno(forms.Form):
    opis = forms.CharField(max_length=1000)
    slika = forms.FileField(
        label='Izberi datoteko', required=False
    )
    leto = forms.IntegerField(max_value=2021, label='Leto:')
    longitude = forms.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = forms.FloatField()
    vprasanje = forms.CharField(max_length=1000) # seznam vprašanj, odvisno od tipa
    form_type = forms.IntegerField(label='form type', initial=2, widget=forms.HiddenInput())

class PravilnoNepravilno(forms.Form):
    opis = forms.CharField(max_length=1000)
    slika = forms.FileField(
        label='Izberi datoteko', required=False
    )
    leto = forms.IntegerField(max_value=2021, label='Leto:')
    longitude = forms.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = forms.FloatField()
    trditev1 = forms.CharField(max_length=100)
    p1 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    trditev2 = forms.CharField(max_length=100)
    p2 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    trditev3 = forms.CharField(max_length=100)
    p3 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    trditev4 = forms.CharField(max_length=100)
    p4 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    trditev5 = forms.CharField(max_length=100)
    p5 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    form_type = forms.IntegerField(label='form type', initial=3, widget=forms.HiddenInput())

class IzberiOdgovor(forms.Form):
    opis = forms.CharField(max_length=1000)
    slika = forms.FileField(
        label='Izberi datoteko', required=False
    )
    leto = forms.IntegerField(max_value=2021, label='Leto:')
    longitude = forms.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = forms.FloatField()
    vprasanje = forms.CharField(max_length=100)
    odgovor1 = forms.CharField(max_length=100)
    odgovor2 = forms.CharField(max_length=100)
    odgovor3 = forms.CharField(max_length=100)
    odgovor4 = forms.CharField(max_length=100)
    odgovor5 = forms.CharField(max_length=100)
    pravilni_odgovor = forms.IntegerField(max_value=5, min_value=1,initial=1) # številka pravilnega odgovora
    form_type = forms.IntegerField(label='form type', initial=4, widget=forms.HiddenInput())

class OdgovorIzberiOdgovor(forms.Form):
    p = forms.ChoiceField(choices=[(1,''),(2,''),(3,''),(4,''),(5,'')], widget=forms.RadioSelect, label='')

class OdgovorPravilnoNepravilno(forms.Form):
    p1 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    p2 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    p3 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    p4 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)
    p5 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect)

class OdgovorOpisno(forms.Form):
    p = forms.CharField(max_length=1000, label= '')

class UporabniskoIme(forms.Form):
    p = forms.CharField(max_length=30, label='Uporabniško ime')

class Prijava(forms.Form):
    username = forms.CharField(max_length=30, label='Uporabniško ime')
    password = forms.CharField(widget=forms.PasswordInput)

class Registracija(forms.Form):
    uime = forms.CharField(max_length=30, label='Uporabniško ime')
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)