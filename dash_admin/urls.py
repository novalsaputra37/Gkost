from django.urls import path, re_path
from dash_admin import views

urlpatterns = [

    # The home page
    path('', views.index, name='dashadmin-home'),
]