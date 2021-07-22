from django.urls import path, re_path
from dash_admin import views
from .views import KomfirmasiTamuBaruView,PemasukanKostView
urlpatterns = [

    # The home page
    path('', views.index, name='dashadmin-home'),
    path('kamar/', KomfirmasiTamuBaruView.as_view(), name='tambah-kamar'),
    path('pembayaran/', PemasukanKostView.as_view(), name='tambah-pembayaran'),
]