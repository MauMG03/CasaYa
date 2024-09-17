from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propiedades')
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50)  # Ejemplo: 'Casa', 'Apartamento'
    price = models.DecimalField(max_digits=15, decimal_places=2)
    location = models.CharField(max_length=255)
    address = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    parking = models.IntegerField()
    area = models.DecimalField(max_digits=15, decimal_places=2)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    type = models.CharField(max_length=50)  # Ejemplo: 'Compra', 'Renta'
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} - {self.property.name}'

class Comment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.DecimalField(max_digits=2, decimal_places=1)  # Ejemplo: '4.5'
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user} en {self.property.name}'