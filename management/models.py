from django.db import models

from core.models import BaseModel
from django.contrib.auth.models import User

# Create your models here.

class Parking(BaseModel):
    
    parking_name = models.CharField(max_length=100, default="Untitled Parking")
    hour_price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None,  related_name="parking_lots")
    headquarters = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='filiais',
        help_text="Indica a sede principal deste estacionamento, se for uma filial."
    )
    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parking Lots"

    def __str__(self):
        if self.headquarters:
            return f"{self.parking_name} (Filial de {self.headquarters.parking_name})"
        return f"{self.parking_name} (Sede)"

class ParkingSpace(BaseModel):
    cod = models.CharField(max_length=10)
    status = models.BooleanField(default=False) 
    pwd = models.BooleanField(default=False) 
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name="spaces", null=True, default=None)

    class Meta:
        verbose_name = "Parking Space"
        verbose_name_plural = "Parking Spaces"
    
    def __str__(self) -> str:
        return f'{self.cod} | {self.parking} | Status: {self.status}'

class Car(BaseModel):
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name="cars")
    color = models.CharField(max_length=100)
    year = models.CharField(max_length=4, null=False, blank=False)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self) -> str:
        return f'{self.id} | {self.model} | {self.license_plate}'


class Ticket(BaseModel):
    checkin = models.TimeField()
    checkout = models.TimeField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, default=None)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, null=True, default=None, related_name="tickets")
    value = models.FloatField()

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self) -> str:
        return f'{self.id} | {self.model} | {self.license_plate} | {self.value}'
    
class Plan(BaseModel):
    nome = models.CharField(max_length=100)
    allowed_parkings = models.ManyToManyField(Parking, blank=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
    
    def __str__(self) -> str:
        return f'{self.name} | {self.allowed_parkings}'