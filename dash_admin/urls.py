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
                    PembayaranTamuBaruNew,
                    LogPembayaranUpdateView,
                    renderPdfLogPembayaran,
                    pengeluaranDeleteView,
                    UpdatePaketView)

app_name = 'dashadmin'
urlpatterns = [

    # The home page
    path('', views.index, name='dashadmin-home'),
    path('logpembayaran/', LogPembayaranDashListView.as_view(), name='log-dash'),
    path('logpembayaran/pdf/', renderPdfLogPembayaran, name='log-pdf'),

    # pembayaran
    path('pembayaran/tamubaru', PembayaranTamuBaruNew, name='tambah-tamu-baru'),
    path('pembayaran/', KonfimasuTamyViewNew, name='tambah-pembayaran'),

    #Data>>Profil Tamu
    path('data/profil/', ProfilTamuListView.as_view(), name='profiltamu-view'),
    path('data/profil/update/<int:pk>', ProfilTamuUpdateView.as_view(), name='profiltamu-update'),
    path('data/profil/detail/<int:pk>', ProfilTamuDetailView.as_view(), name='profiltamu-detail'),
    path('data/profil/delete/<int:pk>', ProfilTamuDeleteView.as_view(), name='profiltamu-delete'),

    #Data>>Kamar Tamu
    path('data/kamar/', KamarTamuListView.as_view(), name='kamartamu-view'),
    path('data/kamar/kamarbaru/', KomfirmasiTamuBaruView.as_view(), name='kamartamu-create'),
    path('data/kamar/update/<int:pk>', KamarTamuUpdateView.as_view(), name='kamartamu-update'),
    path('data/kamar/paket/update/<int:pk>', UpdatePaketView.as_view(), name='kamartamu-update-paket'),
    path('data/kamar/delete/<int:pk>', KamarTamuDeleteView.as_view(), name='kamartamu-delete'),

    #Keuangan >> Pemasukan
    path('keuangan/pemasukan/', PendapatanListView, name='pemasukan-view'),
    path('keuangan/pemasukan/delete/<int:pk>', pengeluaranDeleteView.as_view(), name='pengeluaran-delete'),

    #Keuangan >> Log Pembayaran
    path('keuangan/logpembayaran/', LogPembayaranListView, name='LogPembayaran-view'),
    path('keuangan/logpembayaran/update/<int:pk>', LogPembayaranUpdateView.as_view(), name='LogPembayaran-update'),
    path('keuangan/logpembayaran/delete/<int:pk>', LogPembayaranDeleteView.as_view(), name='LogPembayaran-delete'),

    #KritikSaran
    path('kritik/', kritikSaranListView.as_view(), name='kritikSaran-view'),
    path('kritik/delete/<int:pk>', KritikSaranDeleteView.as_view(), name='kritikSaran-delete'),

    #Tagihan
    path('email/<str:Email>', send_gmail, name='send_mail'),
    path('pdf/<str:Nik>', render_pdf_view, name='pdf-tagihan')
]