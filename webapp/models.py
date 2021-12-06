from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class dbQuiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, default="Kviz 1")
    author = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=50) # geslo za kviz (da ni vsak kviz dostopen vsakomur)

class OpisnoModel(models.Model):
    kviz = models.ForeignKey(dbQuiz, on_delete=CASCADE, null=True)
    opis = models.CharField(max_length=1000)
    slika = models.CharField(max_length=200) # upload jpg-ja
    longitude = models.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = models.FloatField()
    vprasanje = models.CharField(max_length=1000) # seznam vprašanj, odvisno od tipa
    
class PravilnoNepravilnoModel(models.Model):
    kviz = models.ForeignKey(dbQuiz, on_delete=CASCADE, null=True)   
    opis = models.CharField(max_length=1000)
    slika = models.CharField(max_length=200) # upload jpg-ja
    longitude = models.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = models.FloatField()
    vprasanje = models.CharField(max_length=1000, default="nan") # seznam vprašanj
    pravilni_odgovor = models.CharField(max_length=1000, default="nan") # seznam pravilnegih odgovorov
    
class IzberiOdgovorModel(models.Model):
    kviz = models.ForeignKey(dbQuiz, on_delete=CASCADE, null=True)
    opis = models.CharField(max_length=1000)
    slika = models.CharField(max_length=200) # upload jpg-ja
    longitude = models.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = models.FloatField()
    vprasanje = models.CharField(max_length=100)
    odgovor1 = models.CharField(max_length=100, default="nan")
    odgovor2 = models.CharField(max_length=100, default="nan")
    odgovor3 = models.CharField(max_length=100, default="nan")
    odgovor4 = models.CharField(max_length=100, default="nan")
    odgovor5 = models.CharField(max_length=100, default="nan")
    pravilni_odgovor = models.IntegerField() # številka pravilnega odgovora

class dbAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    #vprasanje = models.ForeignKey(dbQuestion, to_field='id', on_delete=models.CASCADE) # kako foreign key na več kot eno tabelo
    vprasanje = models.CharField(max_length=100)
    odgovori = models.CharField(max_length=1000)