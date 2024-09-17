# propiedades/serializers.py
from rest_framework import serializers
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
    property = serializers.SlugRelatedField(slug_field='name', queryset=Property.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self, validated_data):
        # Llamamos al método create normal
        comment = super().create(validated_data)
        # Actualizamos el rate promedio de la propiedad asociada
        self.update_property_rate(comment.property)
        return comment

    def update(self, instance, validated_data):
        # Llamamos al método update normal
        comment = super().update(instance, validated_data)
        # Actualizamos el rate promedio de la propiedad asociada
        self.update_property_rate(comment.property)
        return comment

    def update_property_rate(self, property):
        comments = property.comentarios.all()
        if comments.exists():
            average_rate = comments.aggregate(avg_rate=serializers.Avg('rate'))['avg_rate']
            property.rate = average_rate
            property.save()