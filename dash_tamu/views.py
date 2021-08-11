from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import FormView,TemplateView
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
class PaketKostDashView(TemplateView):
    template_name ='dash_tamu/paketKost.html'

#Kritik & Saran
class KritikSaranView(CreateView):
    form_class = KritikSaranForm
    template_name = 'dash_tamu/kritiksaran/kritikSaran.html'
    success_url = '/'