from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Property, Transaction, Comment
from .serializers import PropertySerializer, TransactionSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions, serializers

# Lista todas las propiedades o crea una nueva
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Solo usuarios autenticados pueden crear

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lectura: permitida a cualquier usuario.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Escritura: permitida solo si es el propietario.
        return obj.user == request.user

# Ver, actualizar o eliminar una propiedad específica
class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Solo usuarios propietarios y autenticados pueden modificar 

# Lista todas las transacciones o crea una nueva
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Solo usuarios autenticados pueden crear

# Ver, actualizar o eliminar una transacción específica
class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Solo usuarios autenticados pueden modificar

# Lista todos los comentarios o crea uno nuevo
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Ver, actualizar o eliminar un comentario específico
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        property = instance.property
        super().perform_destroy(instance)
        # Actualizar el rate de la propiedad después de eliminar un comentario
        comments = property.comentarios.all()
        if comments.exists():
            average_rate = comments.aggregate(avg_rate=serializers.Avg('rate'))['avg_rate']
        else:
            average_rate = None
        property.rate = average_rate
        property.save()
