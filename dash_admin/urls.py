from django.urls import path
from dash_admin import views
from .views import (KomfirmasiTamuBaruView,
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
                    LogPembayaranDeleteView,
                    LogPembayaranDashListView,
                    send_gmail,
                    render_pdf_view,
                    PembayaranTamuBaru,
                    PembayaranTamuBaruNew,
                    iotListrikKost,
                    renderPdfLogPembayaran)

app_name = 'dashadmin'
urlpatterns = [

    # The home page
    path('', views.index, name='dashadmin-home'),
    path('logpembayaran/', LogPembayaranDashListView.as_view(), name='log-dash'),
    path('logpembayaran/pdf/', renderPdfLogPembayaran, name='log-pdf'),

    # path('pembayaran/tamubaru', PembayaranTamuBaru.as_view(), name='tambah-tamu-baru'),
    path('pembayaran/tamubaru', PembayaranTamuBaruNew, name='tambah-tamu-baru'),
    path('pembayaran/', KonfimasuTamyViewNew, name='tambah-pembayaran'),

    #Data>>Profil Tamu
    path('data/profil/<page>', ProfilTamuListView.as_view(), name='profiltamu-view'),
    path('data/profil/update/<int:pk>', ProfilTamuUpdateView.as_view(), name='profiltamu-update'),
    path('data/profil/detail/<int:pk>', ProfilTamuDetailView.as_view(), name='profiltamu-detail'),
    path('data/profil/delete/<int:pk>', ProfilTamuDeleteView.as_view(), name='profiltamu-delete'),

    #Data>>Kamar Tamu
    path('data/kamar/<page>', KamarTamuListView.as_view(), name='kamartamu-view'),
    path('data/kamar/kamarbaru/', KomfirmasiTamuBaruView.as_view(), name='kamartamu-create'),
    path('data/kamar/update/<int:pk>', KamarTamuUpdateView.as_view(), name='kamartamu-update'),
    path('data/kamar/delete/<int:pk>', KamarTamuDeleteView.as_view(), name='kamartamu-delete'),

    #Keuangan >> Pemasukan
    path('keuangan/pemasukan/', PendapatanListView, name='pemasukan-view'),

    #Keuangan >> Log Pembayaran
    path('keuangan/logpembayaran/', LogPembayaranListView, name='LogPembayaran-view'),
    path('keuangan/logpembayaran/delete/<int:pk>', LogPembayaranDeleteView.as_view(), name='LogPembayaran-delete'),

    #KritikSaran
    path('kritik/<page>', kritikSaranListView.as_view(), name='kritikSaran-view'),
    path('kritik/delete/<int:pk>', KritikSaranDeleteView.as_view(), name='kritikSaran-delete'),

    #Tagihan
    path('email/<str:Email>', send_gmail, name='send_mail'),
    path('pdf/<str:Nik>', render_pdf_view, name='pdf-tagihan'),

    #Iot
    path('iotkost/', iotListrikKost, name='iotkost'),
]