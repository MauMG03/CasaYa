"""
URL configuration for casaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import UserDetailView
from properties.views import PropertyListCreateView, PropertyRetrieveUpdateDestroyView, TransactionListCreateView, TransactionRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/auth/', include('djoser.urls')),
    path('users/auth/', include('djoser.urls.jwt')),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
]
