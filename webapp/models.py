from django.db import models

# Create your models here.
class dbKviz(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, default="Kviz 1")
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=50) # geslo za kviz (da ni vsak kviz dostopen vsakomur)

class dbQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    kviz = models.ForeignKey(dbKviz, on_delete=models.CASCADE)
    number = models.IntegerField() # številka vprašanja znotraj kviza
    ime = models.CharField(max_length=100) # ime artefakta
    opis = models.CharField(max_length=1000)
    slika = models.CharField(max_length=200) # ime jpg datoteke zraven vprašanja
    longitude = models.FloatField(max_length=10) # koordinate za leaflet
    latitude = models.FloatField(max_length=10)
    type = models.CharField(max_length=200)  # tip vprašanja (true-false, izberi pravilni odgovor, opisni tip odgovora, izberi vse pravile odgovore,...)
    vprasanja = models.CharField(max_length=1000) # seznam vprašanj, odvisno od tipa
    pravilni_odgovori = models.CharField(max_length=1000) # pravilni odgovori, če obstajajo (true false, izbire,...)

class dbAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    vprasanje = models.ForeignKey(dbQuestion, on_delete=models.CASCADE)
    odgovori = models.CharField(max_length=1000)