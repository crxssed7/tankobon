from django.contrib import admin
from django.urls import path, include
from .views import get_manga

urlpatterns = [
    path('manga/', get_manga, name='get_manga')
]