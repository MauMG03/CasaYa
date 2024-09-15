from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions

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
