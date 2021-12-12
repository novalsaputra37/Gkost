from django.urls import path
from .views import Kamar_API

urlpatterns = [
    path('kamar/', Kamar_API, name='kamar'),
]