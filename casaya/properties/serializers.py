# propiedades/serializers.py
from rest_framework import serializers
from django.db.models import Avg
from .models import Property, Transaction, Comment

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

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        # Obtenemos el usuario autenticado
        request = self.context.get('request')
        validated_data['user'] = request.user

        # Creamos el comentario
        comment = super().create(validated_data)

        # Llamamos a la función que actualizará el rate promedio de la propiedad
        self.update_property_rate(comment.property)

        return comment

    def update_property_rate(self, property):
        # Calculamos el promedio de las calificaciones de los comentarios asociados a la propiedad
        avg_rate = property.comentarios.aggregate(Avg('rate'))['rate__avg']

        # Asignamos el valor promedio al campo 'rate' de la propiedad
        property.rate = avg_rate if avg_rate is not None else 0  # Si no hay comentarios, rate será 0
        property.save()  # Guardamos el cambio en la base de datos