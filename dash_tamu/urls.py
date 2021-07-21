from django.urls import path, re_path

from dash_tamu import views
from .views import RegisterTamuView,PeraturanKostView,PaketKostView,KritikSaranView,PeraturanView,PaketKostDashView

app_name = "dash_tamu"
urlpatterns = [
    path('', views.dashTamuView, name='dashtamu-home'),

    #RegisterTamu
    path('register/profil', RegisterTamuView.as_view(), name='register-profil'),
    path('register/peraturan', PeraturanKostView.as_view(), name='register-peraturan'),
    path('register/paketkost', PaketKostView.as_view(), name='register-paketkost'),

    #daftarpaketkost
    path('paket/', PaketKostDashView.as_view(), name='paket'),
    #peraturanKost
    path('peraturan/', PeraturanView.as_view(), name='peraturan'),
    #Kritik
    path('kritik/', KritikSaranView.as_view(), name='kritik-saran'),
]
