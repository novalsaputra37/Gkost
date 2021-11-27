from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, ListView
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#models
from .models import ProfilTamuModel, PaketKostModel
from dash_admin.models import KamarKostModel, PemasukanKostModel

#pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#form
from .form import ProfilTamuForm,PaketKostForm,KritikSaranForm

#Dashboard View
@login_required(login_url="/")
def dashTamuView(request):
    Akun = request.user
    ProfilTamuModels = ProfilTamuModel.objects.filter(Nik=Akun)
    Statuskos = KamarKostModel.objects.raw('SELECT dash_admin_kamarkostmodel.*, dash_tamu_paketkostmodel.*,datediff(Waktu_out, current_date()) as selisih FROM dash_admin_kamarkostmodel INNER JOIN dash_tamu_paketkostmodel ON dash_admin_kamarkostmodel.Nik=dash_tamu_paketkostmodel.Nik WHERE dash_admin_kamarkostmodel.Nik=%s', [Akun])
    LogPembayaran = PemasukanKostModel.objects.filter(Nik=Akun)
    PaketKost = PaketKostModel.objects.filter(Nik=Akun)
    
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE Nik=%s', [Akun])
    subtotal = cursor.fetchone()[0]
    if subtotal is None:
        subtotal = 0

    context = {
        'subtotal' : subtotal,
        'DataTamu' : ProfilTamuModels,
        'Statuskos' : Statuskos,
        'LogPembayaran' : LogPembayaran,
        'PaketKost' : PaketKost
    }
    context['segment'] = 'dashboard'
  
    if ProfilTamuModels.exists() :
        html_template = loader.get_template( 'dash_tamu/dashboard.html' )
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect('/dashtamu/register/peraturan')

class LogPembayaranTamuListView(LoginRequiredMixin, ListView):
    model = PemasukanKostModel
    template_name = "dash_tamu/dashboard/logPembayaranTamu.html"
    context_object_name = 'obj'

    def get_queryset(self):
        Akun = self.request.user
        self.queryset = self.model.objects.raw('SELECT dash_admin_pemasukankostmodel.*, dash_tamu_profiltamumodel.Nama_lengkap  FROM dash_admin_pemasukankostmodel INNER JOIN dash_tamu_profiltamumodel ON dash_admin_pemasukankostmodel.Nik=dash_tamu_profiltamumodel.Nik WHERE dash_admin_pemasukankostmodel.Nik=%s', [Akun])
        return super().get_queryset()

def render_pdf_LogPembayaran_view(request):
    Akun = request.user
    obj = PemasukanKostModel.objects.raw('SELECT dash_admin_pemasukankostmodel.*, dash_tamu_profiltamumodel.Nama_lengkap  FROM dash_admin_pemasukankostmodel INNER JOIN dash_tamu_profiltamumodel ON dash_admin_pemasukankostmodel.Nik=dash_tamu_profiltamumodel.Nik WHERE dash_admin_pemasukankostmodel.Nik=%s', [Akun])
    template_path = 'dash_tamu/dashboard/printLogPembayaran.html'
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class ProfilListView(LoginRequiredMixin, ListView):
    model = ProfilTamuModel
    template_name = "dash_tamu/profil/profil.html"
    context_object_name = 'DataTamu'

    def get_queryset(self):
        Akun = self.request.user
        self.queryset = self.model.objects.filter(Nik=Akun)
        return super().get_queryset()

#Register Tamu
class PeraturanKostView(LoginRequiredMixin, TemplateView):
    template_name = 'dash_tamu/registerTamu/peraturan.html'

class RegisterTamuView(LoginRequiredMixin, CreateView):
    form_class = ProfilTamuForm
    template_name = "dash_tamu/registerTamu/regtamunew.html"
    success_url = '/dashtamu/register/paketkost'

class PaketKostView(LoginRequiredMixin, FormView):
    form_class = PaketKostForm
    template_name = 'dash_tamu/registerTamu/pilihanPaket.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form })

#Peraturan Kost
class PeraturanView(LoginRequiredMixin, TemplateView):
    template_name ='dash_tamu/peraturankost/peraturankost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'PemasukanKost'
        return context

#harga list
class PaketKostDashView(LoginRequiredMixin, ListView):
    model = ProfilTamuModel
    template_name ='dash_tamu/Tagihan/tagihan.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        Akun = self.request.user
        self.queryset = self.model.objects.raw('SELECT dash_tamu_profiltamumodel.*, dash_admin_kamarkostmodel.*, dash_tamu_paketkostmodel.*, CASE WHEN dash_tamu_paketkostmodel.Paket = 3 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 12 MONTH WHEN dash_tamu_paketkostmodel.Paket = 2 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 3 MONTH WHEN dash_tamu_paketkostmodel.Paket = 1 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 1 MONTH END AS Bulan_out, dash_admin_kamarkostmodel.Waktu_in + INTERVAL 1 MONTH AS Bulan_in, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik INNER JOIN dash_tamu_paketkostmodel ON dash_admin_kamarkostmodel.Nik=dash_tamu_paketkostmodel.Nik WHERE dash_tamu_profiltamumodel.Nik =%s', [Akun])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Akun = self.request.user
        cursor = connection.cursor()
        cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE Nik=%s', [Akun])
        subtotal = cursor.fetchone()[0]
        if subtotal is None:
            subtotal = 0
        print(subtotal)
        context['segment'] = 'Tagihan'
        context['subtotal'] = subtotal
        return context

#Kritik & Saran
class KritikSaranView(LoginRequiredMixin, CreateView):
    form_class = KritikSaranForm
    template_name = 'dash_tamu/kritiksaran/kritikSaran.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'KritikSaran'
        return context