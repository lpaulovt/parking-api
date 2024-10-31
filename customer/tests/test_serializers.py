from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import serializers
from customer.models import Customer
from customer.serializers import CustomerRegisterSerializer

class CustomerRegisterSerializerTest(APITestCase):

    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'birth_date': '2000-01-01'
        }

    def test_valid_data_creates_user_and_customer(self):
        """Testa se os dados válidos criam um usuário e um perfil de cliente."""
        serializer = CustomerRegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        # Verifica se o usuário e o perfil do cliente foram criados corretamente
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.customer.birth_date.strftime('%Y-%m-%d'), self.valid_data['birth_date'])

    def test_password_mismatch(self):
        """Testa se a validação falha quando as senhas não correspondem."""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        serializer = CustomerRegisterSerializer(data=invalid_data)
        
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn("password", cm.exception.detail)

    def test_existing_username_raises_error(self):
        """Testa se ocorre erro ao tentar criar um usuário com nome de usuário existente."""
        User.objects.create_user(username="testuser", password="12345")
        serializer = CustomerRegisterSerializer(data=self.valid_data)
        
        with self.assertRaises(serializers.ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
            self.assertEqual(str(cm.exception.detail[0]), "Usuário já existe com esse nome de usuário.")

