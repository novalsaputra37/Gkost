from django.contrib.auth.decorators import login_required
from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.views.generic import FormView,TemplateView
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse

#models
from .models import RegisterTamuModel

#form
from .form import RegisterTamuForm,PaketKostForm,KritikSaranForm

#Dashboard View
@login_required(login_url="/")
def dashTamuView(request):
    Akun = request.user
    RegisterTamuModels = RegisterTamuModel.objects.filter(Nik=Akun)
    # Statuskos = StatusKostModel.objects.raw('SELECT dash_admin_statuskostmodel.*, current_date() as tgl_sekarang, datediff(Waktu_out, current_date()) as selisih FROM dash_admin_statuskostmodel WHERE Nik= %s', [Akun])
    # InfoPembayaran = InfoPembayaranModel.objects.filter(Nik=Akun)

    context = {
        'DataTamu' : RegisterTamuModels
    }
    context['segment'] = 'dashboard'
  
    if RegisterTamuModels.exists() :
        html_template = loader.get_template( 'dash_tamu/dashboard.html' )
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect('/dashtamu/register/peraturan')

#Register Tamu
class PeraturanKostView(TemplateView):
    template_name = 'dash_tamu/registerTamu/peraturan.html'

class RegisterTamuView(CreateView):
    form_class = RegisterTamuForm
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