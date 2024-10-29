from django.urls import path
from customer.views import CustomerRegisterView

urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
]
