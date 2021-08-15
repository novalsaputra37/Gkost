from django import template
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib import messages

#mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#form
from .forms import KamarKostForm, PemasukanKostForm, PengeluaranKostForm
from dash_tamu.form import ProfilTamuForm

#models
from .models import KamarKostModel,PemasukanKostModel, PengeluaranKostModel
from dash_tamu.models import ProfilTamuModel,PaketKostModel, KritikSaranModel
from django.db import connection

@login_required(login_url="/")
def index(request):
    context = {}
    context['segment'] = 'index'
    context['JumalahTamu'] = ProfilTamuModel.objects.all().count()

    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM dash_admin_kamarkostmodel WHERE Waktu_out >= current_date()')
    TamuAktif = cursor.fetchone()[0]
    context['TamuAktif'] = TamuAktif

    cursor = connection.cursor()
    cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE YEAR(Tgl_pemasukan)= YEAR(NOW())')
    totalTahun = cursor.fetchone()[0]
    context['totalTahun'] = totalTahun

    cursor = connection.cursor()
    cursor.execute("SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE CONCAT(YEAR(Tgl_pemasukan),'/',MONTH(Tgl_pemasukan))=CONCAT(YEAR(NOW()),'/',MONTH(NOW()))")
    totalBulan = cursor.fetchone()[0]
    context['totalBulan'] = totalBulan
    
    html_template = loader.get_template( 'dash_admin/dashboard.html' )
    return HttpResponse(html_template.render(context, request))

#Pembayaran
def KonfimasuTamyViewNew(request):
    template_name = None
    context = None

    if request.user.is_authenticated:
        form = PemasukanKostForm()
        profilTamu = ProfilTamuModel.objects.all()

        context = {
            'form' : form,
            'profilTamu' : profilTamu
        }

        context['segment'] = 'Pembayaran'

        Tagihan = None
        if request.method == 'POST':
            if 'NAMA' in request.POST:
                Tagihan = request.POST['NAMA']
                context['Tagihan'] = Tagihan
                context['invoice'] = ProfilTamuModel.objects.raw('SELECT dash_tamu_profiltamumodel.*, dash_admin_kamarkostmodel.*,dash_admin_kamarkostmodel.Waktu_out + INTERVAL 1 MONTH AS Bulan_out,dash_admin_kamarkostmodel.Waktu_in + INTERVAL 1 MONTH AS Bulan_in , current_date() as tgl_sekarang, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik WHERE dash_tamu_profiltamumodel.Nik =%s', [Tagihan])
                context['PaketKost'] = PaketKostModel.objects.filter(Nik=Tagihan)
            else:
                Tagihan = False

        form = PemasukanKostForm(request.POST)
        if form.is_valid():
            rescuee_instance  = form.save()
            idProfil = ProfilTamuModel.objects.filter(Nik=rescuee_instance.Nik)
            for idProfil in idProfil:
                a = idProfil.id
            return redirect('dashadmin:kamartamu-update', a)
        else:
            form = PemasukanKostForm()
        template_name = 'dash_admin/konfirmasi/perpanjangTamu.html'
    else:
        template_name = 'auth/login.html'
    
    return render(request, template_name, context)

class PemasukanKostView(CreateView):
    form_class = PemasukanKostForm
    template_name = "dash_admin/konfirmasi/perpanjangTamu.html"
    success_url = '/dashadmin/kamar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'PemasukanKost'
        context ['profilTamu'] = ProfilTamuModel.objects.all()
        context ['paketKost'] = PaketKostModel.objects.all()
        return context

#Data Tamu >> Profil
class ProfilTamuListView(ListView):
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamu.html"
    context_object_name = 'ProfilTamu'
    ordering = ['-published']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'ProfilTamu'
        return context

class ProfilTamuUpdateView(UpdateView):
    form_class = ProfilTamuForm
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuUpdate.html"
    success_url = reverse_lazy('dashadmin:profiltamu-view')

class ProfilTamuDetailView(DetailView):
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDetail.html"
    context_object_name = 'ProfilTamu'

class ProfilTamuDeleteView(DeleteView):
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = reverse_lazy('dashadmin:kamartamu-view')

#Data Tamu >> Kamar
class KamarTamuListView(ListView):
    model = KamarKostModel
    template_name = "dash_admin/dataTamu/kamarTamu/kamarTamu.html"
    context_object_name = 'KamarTamu'

    def get_queryset(self):
        self.queryset = self.model.objects.raw('SELECT dash_tamu_profiltamumodel.*, dash_admin_kamarkostmodel.*, current_date() as tgl_sekarang, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik ORDER BY `selisih` DESC')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'ProfilTamu'
        return context

class KomfirmasiTamuBaruView(CreateView):
    form_class = KamarKostForm
    template_name = 'dash_admin/konfirmasi/tamuBaru.html'
    success_url = reverse_lazy('dashadmin:kamartamu-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ' KomfirmasiTamuBaru'
        context['profilTamu'] = ProfilTamuModel.objects.all()
        return context

class KamarTamuUpdateView(UpdateView):
    form_class = KamarKostForm
    model = KamarKostModel
    template_name = "dash_admin/dataTamu/kamarTamu/kamarTamuUpdate.html"
    success_url = reverse_lazy('dashadmin:kamartamu-view')
    
class KamarTamuDeleteView(DeleteView):
    model = KamarKostModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = reverse_lazy('dashadmin:profiltamu-view')

#Keuangan >> Penghasilan
def PendapatanListView(request):
    context = {}
    context['segment'] = 'Keuangan'
    PengeluaranKost = PengeluaranKostForm
    context = {
        'form' : PengeluaranKost
    }
    if request.method == 'POST':
        Bulan = request.POST['Bulan']
        context['InfoPembayaran'] = PemasukanKostModel.objects.raw('SELECT dash_tamu_profiltamumodel.Nama_lengkap, dash_admin_pemasukankostmodel.* FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_pemasukankostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_pemasukankostmodel.Nik where month(tgl_pemasukan)=%s', [Bulan])
        context['InfoPengeluaran'] = PengeluaranKostModel.objects.raw('SELECT * FROM dash_admin_pengeluarankostmodel where month(Tgl_pengeluaran)=%s', [Bulan])

        cursor = connection.cursor()
        cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel where month(Tgl_pemasukan)=%s', [Bulan])
        pemasukanTotal = cursor.fetchone()[0]
        context['pemasukanTotal'] = pemasukanTotal

        cursor = connection.cursor()
        cursor.execute('SELECT SUM(jmlh_pengeluaran) AS Total FROM dash_admin_pengeluarankostmodel where month(Tgl_pengeluaran)=%s', [Bulan])
        pengeluaranTotal = cursor.fetchone()[0]
        context['pengeluaranTotal'] = pengeluaranTotal

        if pemasukanTotal is None:
            pemasukanTotal = 0
        if pengeluaranTotal is None:
            pengeluaranTotal = 0
        
        profit = pemasukanTotal - pengeluaranTotal
        context['profit'] = profit

        form = PengeluaranKostForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    html_template = loader.get_template( 'dash_admin/keuangan/pendapatan.html' )
    return HttpResponse(html_template.render(context, request))

#Keuangan >> log Pembayaran
def LogPembayaranListView(request):
    template_name = None
    context = None

    if request.user.is_authenticated:
        profilTamu = ProfilTamuModel.objects.all()

        context = {
            'profilTamu' : profilTamu
        }

        context['segment'] = 'Pembayaran'

        nama = None
        if request.method == 'POST':
            if 'NAMA' in request.POST:
                nama = request.POST['NAMA']
                context['invoice'] = PemasukanKostModel.objects.raw('SELECT dash_tamu_profiltamumodel.Nama_lengkap, dash_admin_pemasukankostmodel.* FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_pemasukankostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_pemasukankostmodel.Nik WHERE dash_admin_pemasukankostmodel.Nik=%s', [nama])
                cursor = connection.cursor()
                cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE Nik=%s', [nama])
                subtotal = cursor.fetchone()[0]
                context['subtotal'] = subtotal
            else:
                nama = False

        template_name = 'dash_admin/keuangan/logPembayaranView.html'
    else:
        template_name = 'auth/login.html'
    
    return render(request, template_name, context)

class LogPembayaranDeleteView(DeleteView):
    model = PemasukanKostModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = reverse_lazy('dashadmin:profiltamu-view')

#KritikSaran
class kritikSaranListView(ListView):
    model = KritikSaranModel
    template_name = "dash_admin/kritikSaran/kritikSaranList.html"
    context_object_name = 'kritikSaran'

    def get_queryset(self):
        self.queryset = self.model.objects.raw('SELECT dash_tamu_profiltamumodel.Nama_lengkap,dash_tamu_profiltamumodel.Email, dash_tamu_kritiksaranmodel.* FROM dash_tamu_profiltamumodel INNER JOIN dash_tamu_kritiksaranmodel ON dash_tamu_profiltamumodel.Nik=dash_tamu_kritiksaranmodel.Nik')
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = ' KritikSaran'
        return context

class KritikSaranDeleteView(DeleteView):
    model = KritikSaranModel
    template_name = "dash_admin/kritikSaran/kritikSaranDelete.html"
    context_object_name = 'kritikSaran'
    success_url = reverse_lazy('dashadmin:kritikSaran-view')

def send_gmail(request, Email):
    obj = ProfilTamuModel.objects.get(Email=Email)
    print(obj.Email)
    subject = 'cek sound'
    massage = 'Tagihan kost'
    to = obj.Email
    html_content = render_to_string("dash_admin/email/emailTempate.html", {'title': 'test email', 'content' : massage })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        'gatotkacanetwork@gmail.com',
        [to],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()

    return render(request, 'dash_admin/email/email.html')

def render_pdf_view(request):
    template_path = 'dash_admin/konfirmasi/pdf1.html'
    context = {'myvar': 'this is your template context'}
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