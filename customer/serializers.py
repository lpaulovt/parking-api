
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class CustomerRegisterSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(write_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name', 
            'last_name', 'birth_date'
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        return attrs

    def create(self, validated_data):
        birth_date = validated_data['birth_date']
        user = None

        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError("Usuário já existe com esse nome de usuário.")

        try:
            user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
            )

            user.set_password(validated_data['password'])
            user.save()

            user.customer.birth_date = birth_date
            user.customer.save()

        except Exception as e:
            raise serializers.ValidationError(f"Erro ao criar cliente: {str(e)}")

        return user

