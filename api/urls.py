from django.urls import path
from .views import my_view

urlpatterns = [
    path('test/', my_view, name='test'),
]