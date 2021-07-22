from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.views.generic import CreateView
from .forms import KamarKostForm,PemasukanKostForm

@login_required(login_url="/")
def index(request):
    
    context = {}
    context['segment'] = 'index'
    
    html_template = loader.get_template( 'dash_admin/dashboard.html' )
    return HttpResponse(html_template.render(context, request))

class KomfirmasiTamuBaruView(CreateView):
    form_class = KamarKostForm
    template_name = 'dash_admin/konfirmasi/tamuBaru.html'
    success_url = '/'

class PemasukanKostView(CreateView):
    form_class = PemasukanKostForm
    template_name = "dash_admin/konfirmasi/perpanjangTamu.html"
    success_url = '/dashadmin/kamar'
