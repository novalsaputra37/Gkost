from django.urls import path, re_path

from dash_tamu import views

app_name = "dash_tamu"
urlpatterns = [
    path('', views.dashTamuView, name='dashtamu-home'),

    #RegisterTamu
    path('register/profil', views.RegisterTamuView.as_view(), name='register-profil'),
    path('register/peraturan', views.PeraturanKostView.as_view(), name='register-peraturan'),
    path('register/paketkost', views.PaketKostView.as_view(), name='register-paketkost'),

    #daftarpaketkost
    path('paket/', views.PaketKostDashView.as_view(), name='paket'),
    #peraturanKost
    path('peraturan/', views.PeraturanView.as_view(), name='peraturan'),
    #Kritik
    path('kritik/', views.KritikSaranView.as_view(), name='kritik-saran'),
]
