from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)  # Obligatorio
    last_name = models.CharField(max_length=30, blank=False, null=False)  # Obligatorio
    email = models.EmailField(unique=True, blank=False, null=False)  # Obligatorio y único
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Usaremos el email como campo principal para iniciar sesión
    REQUIRED_FIELDS = ['first_name', 'last_name','address','phone','username']  # Campos requeridos adicionales

    def __str__(self):
        return self.email