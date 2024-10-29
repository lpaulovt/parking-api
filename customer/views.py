from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from customer.serializers import CustomerRegisterSerializer

class CustomerRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerRegisterSerializer
