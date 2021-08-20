from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, ListView
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse

#models
from .models import ProfilTamuModel
from dash_admin.models import KamarKostModel, PemasukanKostModel

#form
from .form import ProfilTamuForm,PaketKostForm,KritikSaranForm

#Dashboard View
@login_required(login_url="/")
def dashTamuView(request):
    Akun = request.user
    ProfilTamuModels = ProfilTamuModel.objects.filter(Nik=Akun)
    Statuskos = KamarKostModel.objects.raw('SELECT dash_admin_kamarkostmodel.*, dash_tamu_paketkostmodel.*,datediff(Waktu_out, current_date()) as selisih FROM dash_admin_kamarkostmodel INNER JOIN dash_tamu_paketkostmodel ON dash_admin_kamarkostmodel.Nik=dash_tamu_paketkostmodel.Nik WHERE dash_admin_kamarkostmodel.Nik=%s', [Akun])
    LogPembayaran = PemasukanKostModel.objects.filter(Nik=Akun)

    context = {
        'DataTamu' : ProfilTamuModels,
        'Statuskos' : Statuskos,
        'LogPembayaran' : LogPembayaran
    }
    context['segment'] = 'dashboard'
  
    if ProfilTamuModels.exists() :
        html_template = loader.get_template( 'dash_tamu/dashboard.html' )
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect('/dashtamu/register/peraturan')

#Register Tamu
class PeraturanKostView(TemplateView):
    template_name = 'dash_tamu/registerTamu/peraturan.html'

class RegisterTamuView(CreateView):
    form_class = ProfilTamuForm
    template_name = "dash_tamu/registerTamu/regtamunew.html"
    success_url = '/dashtamu/register/paketkost'

class PaketKostView(FormView):
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
class PeraturanView(TemplateView):
    template_name ='dash_tamu/peraturankost/peraturankost.html'

#harga list
class PaketKostDashView(ListView):
    model = ProfilTamuModel
    template_name ='dash_tamu/Tagihan/tagihan.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        Akun = self.request.user
        print(Akun)
        self.queryset = self.model.objects.raw('SELECT dash_tamu_profiltamumodel.*, dash_admin_kamarkostmodel.*, dash_tamu_paketkostmodel.*, CASE WHEN dash_tamu_paketkostmodel.Paket = 3 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 12 MONTH WHEN dash_tamu_paketkostmodel.Paket = 2 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 3 MONTH WHEN dash_tamu_paketkostmodel.Paket = 1 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 1 MONTH END AS Bulan_out, dash_admin_kamarkostmodel.Waktu_in + INTERVAL 1 MONTH AS Bulan_in, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik INNER JOIN dash_tamu_paketkostmodel ON dash_admin_kamarkostmodel.Nik=dash_tamu_paketkostmodel.Nik WHERE dash_tamu_profiltamumodel.Nik =%s', [Akun])
        return super().get_queryset()
        
#Kritik & Saran
class KritikSaranView(CreateView):
    form_class = KritikSaranForm
    template_name = 'dash_tamu/kritiksaran/kritikSaran.html'
    success_url = '/'