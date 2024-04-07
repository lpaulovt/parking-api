from django.db import models

# Create your models here.

class Parking(models.Model):
    hour_price = models.FloatField()

class ParkingSpace(models.Model):
    cod = models.CharField(max_length=10)
    status = models.BooleanField(default=False) 
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name="spaces", default=None)

class Ticket(models.Model):
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=100)
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    vaga = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, default=None)
    valor = models.FloatField()

