from django.db import models
from django.db.models.deletion import CASCADE
import uuid

# Create your models here.
class dbQuiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, default="Kviz 1")
    author = models.CharField(max_length=200)
    password = models.CharField(max_length=200) # geslo za kviz (da ni vsak kviz dostopen vsakomur)
    pictureUrl = models.CharField(max_length=200)   # url can be local or online
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OpisnoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kviz = models.ForeignKey(dbQuiz, on_delete=CASCADE, null=True)
    opis = models.CharField(max_length=1000)
    longitude = models.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = models.FloatField()
    vprasanje = models.CharField(max_length=1000) # seznam vprašanj, odvisno od tipa
    
class PravilnoNepravilnoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kviz = models.ForeignKey(dbQuiz, on_delete=CASCADE, null=True)   
    opis = models.CharField(max_length=1000)
    longitude = models.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = models.FloatField()
    vprasanje = models.CharField(max_length=1000, default="nan") # seznam vprašanj
    pravilni_odgovor = models.CharField(max_length=1000, default="nan") # seznam pravilnegih odgovorov
    
class IzberiOdgovorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kviz = models.ForeignKey(dbQuiz, on_delete=CASCADE, null=True)
    opis = models.CharField(max_length=1000)
    longitude = models.FloatField() # koordinate za leaflet (bomo spremenili na koncu)
    latitude = models.FloatField()
    vprasanje = models.CharField(max_length=100)
    odgovor1 = models.CharField(max_length=100, default="nan")
    odgovor2 = models.CharField(max_length=100, default="nan")
    odgovor3 = models.CharField(max_length=100, default="nan")
    odgovor4 = models.CharField(max_length=100, default="nan")
    odgovor5 = models.CharField(max_length=100, default="nan")
    pravilni_odgovor = models.IntegerField() # številka pravilnega odgovora

class OdgovorPravilnoNepravilnoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=30)
    vprasanje = models.ForeignKey(PravilnoNepravilnoModel, on_delete=CASCADE)
    odgovori = models.CharField(max_length=1000)

class OdgovorIzberiOdgovorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=30)
    vprasanje = models.ForeignKey(IzberiOdgovorModel, on_delete=CASCADE)
    odgovori = models.CharField(max_length=1000)

class OdgovorOpisnoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=30)
    vprasanje = models.ForeignKey(OpisnoModel, on_delete=CASCADE)
    odgovori = models.CharField(max_length=1000)

class DatotekaOpisnoModel(models.Model):
    datoteka = models.FileField(upload_to='media/')
    vprasanje = models.ForeignKey(OpisnoModel, on_delete=CASCADE)

class DatotekaPravilnoNepravilnoModel(models.Model):
    datoteka = models.FileField(upload_to='media/')
    vprasanje = models.ForeignKey(PravilnoNepravilnoModel, on_delete=CASCADE)

class DatotekaIzberiOdgovorModel(models.Model):
    datoteka = models.FileField(upload_to='media/')
    vprasanje = models.ForeignKey(IzberiOdgovorModel, on_delete=CASCADE)
