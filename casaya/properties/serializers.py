# propiedades/serializers.py
from rest_framework import serializers
from .models import Property, Transaction

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'  # O lista los campos que quieras exponer

class TransactionSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(slug_field='name', queryset=Property.objects.all())
    user = serializers.StringRelatedField()  # Esto mostrará una representación de cadena del usuario

    class Meta:
        model = Transaction
        fields = '__all__'  # O lista explícitamente los campos que quieras exponer