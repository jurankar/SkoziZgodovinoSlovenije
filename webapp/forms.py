from django import forms

class Kviz(forms.Form):
    ime = forms.CharField(label='ime kviza', max_length=100)
    avtor = forms.CharField(label='avtor kviza', max_length=100)
    geslo = forms.CharField(widget=forms.PasswordInput(), max_length=100)

