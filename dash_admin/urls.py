from django.urls import path
from dash_admin import views
from .views import (KomfirmasiTamuBaruView,
                    PemasukanKostView,
                    ProfilTamuListView,
                    ProfilTamuUpdateView,
                    ProfilTamuDetailView,
                    ProfilTamuDeleteView,
                    KamarTamuListView,
                    KamarTamuUpdateView,
                    KamarTamuDeleteView,
                    KonfimasuTamyViewNew,
                    kritikSaranListView,
                    KritikSaranDeleteView,
                    LogPembayaranListView,
                    PendapatanListView,
                    LogPembayaranDeleteView,)

app_name = 'dashadmin'
urlpatterns = [

    # The home page
    path('', views.index, name='dashadmin-home'),
    # path('pembayaran/', PemasukanKostView.as_view(), name='tambah-pembayaran'),
    path('pembayaran/', KonfimasuTamyViewNew, name='tambah-pembayaran'),

    #Data>>Profil Tamu
    path('data/profil/', ProfilTamuListView.as_view(), name='profiltamu-view'),
    path('data/profil/kamarbaru/', KomfirmasiTamuBaruView.as_view(), name='tambah-kamar'),
    path('data/profil/update/<int:pk>', ProfilTamuUpdateView.as_view(), name='profiltamu-update'),
    path('data/profil/detail/<int:pk>', ProfilTamuDetailView.as_view(), name='profiltamu-detail'),
    path('data/profil/delete/<int:pk>', ProfilTamuDeleteView.as_view(), name='profiltamu-delete'),

    #Data>>Kamar Tamu
    path('data/kamar/', KamarTamuListView.as_view(), name='kamartamu-view'),
    path('data/kamar/update/<int:pk>', KamarTamuUpdateView.as_view(), name='kamartamu-update'),
    path('data/kamar/delete/<int:pk>', KamarTamuDeleteView.as_view(), name='kamartamu-delete'),

    #Keuangan >> Pemasukan
    path('keuangan/pemasukan/', PendapatanListView, name='pemasukan-view'),

    #Keuangan >> Log Pembayaran
    path('keuangan/logpembayaran/', LogPembayaranListView, name='LogPembayaran-view'),
    path('keuangan/logpembayaran/delete/<int:pk>', LogPembayaranDeleteView.as_view(), name='LogPembayaran-delete'),

    #KritikSaran
     path('kritik/', kritikSaranListView.as_view(), name='kritikSaran-view'),
     path('kritik/delete/<int:pk>', KritikSaranDeleteView.as_view(), name='kritikSaran-delete'),
]