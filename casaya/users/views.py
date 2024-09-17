# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder a esta vista

    def get(self, request, user_id, format=None):
        try:
            # Obtener el usuario por ID
            user = User.objects.get(id=user_id)
            # Retornar la información básica del usuario
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'address': user.address,
                'email': user.email,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Si el usuario no existe, devolver un error 404
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
