from django.test import TestCase
from django.contrib.auth.models import User
from customer.models import Customer

class CustomerModelTest(TestCase):

    def test_customer_creation_on_user_save(self):
        """Testa se um perfil de cliente é criado automaticamente ao salvar um usuário."""
        user = User.objects.create_user(username="testuser", password="12345")
        customer = Customer.objects.get(user=user)
        self.assertEqual(customer.user, user)
        self.assertIsNone(customer.birth_date)

    def test_customer_str_method(self):
        """Testa o método __str__ para o modelo Customer."""
        user = User.objects.create_user(username="testuser", password="12345")
        customer = Customer.objects.get(user=user)
        self.assertEqual(str(customer), "testuser")
