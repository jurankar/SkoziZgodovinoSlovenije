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
    type = forms.ChoiceField(choices=[(1, 'opisno'), (2, 'p/n'), (3, 'izbirno')], label="Tip vprašanja")  # tip vprašanja (true-false, izberi pravilni odgovor, opisni tip odgovora, izberi vse pravile odgovore,...)
    form_type = forms.IntegerField(label='form type', initial=1, widget=forms.HiddenInput())

class Opisno(forms.Form):
    opis = forms.Field(widget=forms.TextInput(attrs={'size': '80'}))
    slika = forms.FileField(
        label='Izberi sliko', required=False
    )
    leto = forms.IntegerField(max_value=2022, label='Leto:')
    longitude = forms.FloatField(widget=forms.HiddenInput()) # koordinate za leaflet (bomo spremenili na koncu)
    latitude = forms.FloatField(widget=forms.HiddenInput())
    vprasanje = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), max_length=1000, label='Vprašanje') # seznam vprašanj, odvisno od tipa
    form_type = forms.IntegerField(label='form type', initial=2, widget=forms.HiddenInput())

class PravilnoNepravilno(forms.Form):
    opis = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    slika = forms.FileField(
        label='Izberi sliko', required=False
    )
    leto = forms.IntegerField(max_value=2022, label='Leto:')
    longitude = forms.FloatField(widget=forms.HiddenInput()) # koordinate za leaflet (bomo spremenili na koncu)
    latitude = forms.FloatField(widget=forms.HiddenInput())
    trditev1 = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), max_length=100)
    p1 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect, label="")
    trditev2 = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), max_length=100)
    p2 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect, label="")
    trditev3 = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), max_length=100)
    p3 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect, label="")
    trditev4 = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), max_length=100)
    p4 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect, label="")
    trditev5 = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), max_length=100)
    p5 = forms.ChoiceField(choices=[("P","P"),("N","N")], widget=forms.RadioSelect, label="")
    form_type = forms.IntegerField(label='form type', initial=3, widget=forms.HiddenInput())

class IzberiOdgovor(forms.Form):
    opis = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    slika = forms.FileField(
        label='Izberi sliko', required=False
    )
    leto = forms.IntegerField(max_value=2022, label='Leto:')
    longitude = forms.FloatField(widget=forms.HiddenInput()) # koordinate za leaflet (bomo spremenili na koncu)
    latitude = forms.FloatField(widget=forms.HiddenInput())
    vprasanje = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), max_length=100, label='Vprašanje')
    odgovor1 = forms.CharField(max_length=100, label='Možnost 1')
    odgovor2 = forms.CharField(max_length=100, label='Možnost 2')
    odgovor3 = forms.CharField(max_length=100, label='Možnost 3')
    odgovor4 = forms.CharField(max_length=100, label='Možnost 4')
    odgovor5 = forms.CharField(max_length=100, label='Možnost 5')
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
    p = forms.CharField(max_length=1000, label= '', widget=forms.TextInput(attrs={'style': 'width:500px'}))

class UporabniskoIme(forms.Form):
    p = forms.CharField(max_length=30, label='Nadimek')

class Prijava(forms.Form):
    username = forms.CharField(max_length=30, label='Uporabniško ime')
    password = forms.CharField(widget=forms.PasswordInput, label='Geslo')

class Registracija(forms.Form):
    uime = forms.CharField(max_length=30, label='Uporabniško ime')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Geslo')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Ponovno vpišite geslo')