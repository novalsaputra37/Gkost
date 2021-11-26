from django import template
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
import datetime

#mail
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

    TimeNow = datetime.datetime.now().strftime('%Y')
    context['TimeNow'] = TimeNow

    #Pendapatan Tahun Sekarang
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE YEAR(Tgl_pemasukan)= YEAR(NOW())')
    PendapatanTahunIni = cursor.fetchone()[0]
    if PendapatanTahunIni is None:
        PendapatanTahunIni = 0
    context['PendapatanTahunIni'] = PendapatanTahunIni

    #Pendapatan Chart
    data = []
    count = 0
    while (count < 13):
        cursor = connection.cursor()
        cursor.execute("select SUM(Jmlh_pemasukan) AS Total from dash_admin_pemasukankostmodel where month(Tgl_pemasukan)=%s and year(Tgl_pemasukan) =%s", [count, TimeNow])
        bulan_1 = cursor.fetchone()[0]
        if bulan_1 == None:
            bulan_1 = 0
        float_str = float(bulan_1)
        bulan_1 = int(float_str)
        data.append(bulan_1)
        count = count + 1

    data.pop(0)
    context['data_Main_chart'] = data

    #Pendapatan Tahunan Card 2
    Pendapatan = []
    x = 1
    while (x < 6):
        cursor = connection.cursor()
        cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE YEAR(Tgl_pemasukan)=202%s', [x])
        Pendapatantahuan = cursor.fetchone()[0]
        if Pendapatantahuan == None:
            Pendapatantahuan = 0
        Pendapatantahuan = int(Pendapatantahuan)
        Pendapatan.append(Pendapatantahuan)
        x = x + 1

    context['Pendapatan_pertahun'] = Pendapatan


    #gender Chart
    gender = []

    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(Jenis_kelamin) FROM `dash_tamu_profiltamumodel` WHERE Jenis_kelamin="pria"')
    pria = cursor.fetchone()[0]

    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(Jenis_kelamin) FROM `dash_tamu_profiltamumodel` WHERE Jenis_kelamin="wanita"')
    wanita = cursor.fetchone()[0]

    gender.append(pria)
    gender.append(wanita)
    context['gender'] = gender

    context['segment'] = 'index'
    context['JumalahTamu'] = ProfilTamuModel.objects.all().count()

    #tamu daftar chart
    tamu = []
    count = 0
    while (count < 13):
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM dash_tamu_profiltamumodel where month(published)=%s and year(published) =%s', [count, TimeNow])
        tamu_1 = cursor.fetchone()[0]
        if tamu_1 == None:
            tamu_1 = 0

        tamu.append(tamu_1)
        count = count + 1

    tamu.pop(0)
    context['data_tamu_chart'] = tamu

    #card Jumlah Tamu
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM dash_admin_kamarkostmodel WHERE Waktu_out >= current_date()')
    TamuAktif = cursor.fetchone()[0]
    context['TamuAktif'] = TamuAktif

    #Card Pendapatan Bulan Ini
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel WHERE CONCAT(YEAR(Tgl_pemasukan),'/',MONTH(Tgl_pemasukan))=CONCAT(YEAR(NOW()),'/',MONTH(NOW()))")
    totalBulan = cursor.fetchone()[0]
    if totalBulan is None:
        totalBulan = 0
    context['totalBulan'] = totalBulan

    #Card Log Pembayaran Bulan Ini
    context['LogPembayaran'] = PemasukanKostModel.objects.raw("SELECT dash_admin_pemasukankostmodel.*, dash_tamu_profiltamumodel.Nama_lengkap FROM dash_admin_pemasukankostmodel INNER JOIN dash_tamu_profiltamumodel on dash_tamu_profiltamumodel.Nik = dash_admin_pemasukankostmodel.Nik WHERE CONCAT(YEAR(Tgl_pemasukan),'/',MONTH(Tgl_pemasukan))=CONCAT(YEAR(NOW()),'/',MONTH(NOW()))")
    
    #Card Keuntungan Bersih Tahun Ini
    cursor = connection.cursor()
    cursor.execute('SELECT SUM(jmlh_pengeluaran) AS Total FROM dash_admin_pengeluarankostmodel WHERE YEAR(Tgl_pengeluaran)= YEAR(NOW())')
    PengeluaranTahunIni = cursor.fetchone()[0]
    if PengeluaranTahunIni is None:
        PengeluaranTahunIni = 0
    context['PengeluaranTahunIni'] = PengeluaranTahunIni
    TotalBersih = PendapatanTahunIni - PengeluaranTahunIni
    context['TotalBersih'] = TotalBersih

    html_template = loader.get_template( 'dash_admin/dashboard.html' )
    return HttpResponse(html_template.render(context, request))

class LogPembayaranDashListView(ListView):
    model = PemasukanKostModel
    template_name = "dash_admin/dashboard/logPembayaranDash.html"
    context_object_name = 'obj'

    def get_queryset(self):
        self.queryset = self.model.objects.raw("SELECT dash_admin_pemasukankostmodel.*, dash_tamu_profiltamumodel.Nama_lengkap FROM dash_admin_pemasukankostmodel INNER JOIN dash_tamu_profiltamumodel on dash_tamu_profiltamumodel.Nik=dash_admin_pemasukankostmodel.Nik WHERE YEAR(Tgl_pemasukan)= YEAR(NOW()) ORDER BY `dash_admin_pemasukankostmodel`.`Tgl_pemasukan` DESC")
        return super().get_queryset()

def renderPdfLogPembayaran(request):
    obj = PemasukanKostModel.objects.raw("SELECT dash_admin_pemasukankostmodel.*, dash_tamu_profiltamumodel.Nama_lengkap FROM dash_admin_pemasukankostmodel INNER JOIN dash_tamu_profiltamumodel on dash_tamu_profiltamumodel.Nik=dash_admin_pemasukankostmodel.Nik WHERE YEAR(Tgl_pemasukan)= YEAR(NOW()) ORDER BY `dash_admin_pemasukankostmodel`.`Tgl_pemasukan` DESC")
    template_path = 'dash_admin/dashboard/pdfLogPembayaranDash.html'
    context = {'myvar': 'this is your template context', 'obj' : obj}
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

def PembayaranTamuBaruNew(request):
    template_name = None
    context = None
    
    if request.user.is_authenticated:
        form = PemasukanKostForm()
        profilTamu = ProfilTamuModel.objects.all()

        context = {
            'form' : form,
            'profilTamu' : profilTamu,
            'segment' : 'Pembayaran'
        }

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
            form.save()
            return HttpResponseRedirect('/dashadmin/data/kamar/kamarbaru/')

        template_name = 'dash_admin/konfirmasi/pembayaranTamuBaru.html'
    else:
        template_name = 'auth/login.html'

    return render(request, template_name, context)

#Data Tamu >> Profil
class ProfilTamuListView(ListView):
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/newProfilTamu.html"
    context_object_name = 'ProfilTamu'
    ordering = ['-published']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'ProfilTamu'
        context['jmlh_row'] = self.model.objects.count()
        return context

class ProfilTamuUpdateView(UpdateView):
    form_class = ProfilTamuForm
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuUpdate.html"
    success_url = '/dashadmin/data/profil/1'

class ProfilTamuDetailView(DetailView):
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDetail.html"
    context_object_name = 'ProfilTamu'

class ProfilTamuDeleteView(DeleteView):
    model = ProfilTamuModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = '/dashadmin/data/profil/1'

#Data Tamu >> Kamar
class KamarTamuListView(ListView):
    model = KamarKostModel
    template_name = "dash_admin/dataTamu/kamarTamu/kamarTamu.html"
    context_object_name = 'KamarTamu'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = self.model.objects.raw('SELECT dash_tamu_profiltamumodel.Nama_lengkap, dash_tamu_profiltamumodel.No_tlp, dash_tamu_profiltamumodel.Email, dash_admin_kamarkostmodel.*, current_date() as tgl_sekarang, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik ORDER BY `No_kamar` ASC')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'ProfilTamu'
        context['jmlh_row'] = self.model.objects.count()
        return context

class KomfirmasiTamuBaruView(CreateView):
    form_class = KamarKostForm
    template_name = 'dash_admin/dataTamu/kamarTamu/tamuBaru.html'
    success_url = '/dashadmin/data/kamar/1'

    def get_context_data(self, **kwargs):
        Nokamar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        kamarTerpakai = KamarKostModel.objects.raw('SELECT * FROM dash_admin_kamarkostmodel ORDER BY dash_admin_kamarkostmodel.No_kamar ASC')
        for x in kamarTerpakai:
            Nokamar.remove(x.No_kamar)

        if not Nokamar:
            Nokamar = "Kamar Habis Terisi"
        
        context = super().get_context_data(**kwargs)
        context['nokamar'] = Nokamar
        context['segment'] = ' KomfirmasiTamuBaru'
        context['profilTamu'] = ProfilTamuModel.objects.all()
        return context

class KamarTamuUpdateView(UpdateView):
    form_class = KamarKostForm
    model = KamarKostModel
    template_name = "dash_admin/dataTamu/kamarTamu/kamarTamuUpdate.html"
    success_url = '/dashadmin/data/kamar/1'
    
class KamarTamuDeleteView(DeleteView):
    model = KamarKostModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = '/dashadmin/data/kamar/1'

#Keuangan >> Rincian Keuangan
def PendapatanListView(request):
    context = {}

    PengeluaranKost = PengeluaranKostForm()
    context = {
        'form' : PengeluaranKost,
        'segment' : 'Keuangan'
    }
    form = PengeluaranKostForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        Bulan = request.POST['Bulan']
        Tahun = request.POST['Tahun']
        context['InfoPembayaran'] = PemasukanKostModel.objects.raw('SELECT dash_tamu_profiltamumodel.Nama_lengkap, dash_admin_pemasukankostmodel.* FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_pemasukankostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_pemasukankostmodel.Nik where month(Tgl_pemasukan)=%s and year(Tgl_pemasukan) =%s', [Bulan, Tahun])
        context['InfoPengeluaran'] = PengeluaranKostModel.objects.raw('SELECT * FROM dash_admin_pengeluarankostmodel where month(Tgl_pengeluaran)=%s and year(Tgl_pengeluaran) =%s', [Bulan, Tahun])

        #Table Pemasukan & Pengeluaran
        cursor = connection.cursor()
        cursor.execute('SELECT SUM(Jmlh_pemasukan) AS Total FROM dash_admin_pemasukankostmodel where month(Tgl_pemasukan)=%s and year(Tgl_pemasukan)=%s', [Bulan, Tahun])
        pemasukanTotal = cursor.fetchone()[0]
        context['pemasukanTotal'] = pemasukanTotal

        cursor = connection.cursor()
        cursor.execute('SELECT SUM(jmlh_pengeluaran) AS Total FROM dash_admin_pengeluarankostmodel where month(Tgl_pengeluaran)=%s and year(Tgl_pengeluaran)=%s', [Bulan, Tahun])
        pengeluaranTotal = cursor.fetchone()[0]
        context['pengeluaranTotal'] = pengeluaranTotal

        if pemasukanTotal is None:
            pemasukanTotal = 0
        if pengeluaranTotal is None:
            pengeluaranTotal = 0
        
        profit = pemasukanTotal - pengeluaranTotal
        context['profit'] = profit

    html_template = loader.get_template( 'dash_admin/keuangan/pendapatan.html' )
    return HttpResponse(html_template.render(context, request))

class pengeluaranDeleteView(DeleteView):
    model = PengeluaranKostModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = '/dashadmin/keuangan/pemasukan/'

#Keuangan >> log Pembayaran
def LogPembayaranListView(request):
    template_name = None
    context = None

    if request.user.is_authenticated:
        profilTamu = ProfilTamuModel.objects.all()

        context = {
            'profilTamu' : profilTamu
        }

        context['segment'] = 'Keuangan'

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

class LogPembayaranUpdateView(UpdateView):
    form_class = PemasukanKostForm
    model = PemasukanKostModel
    template_name = 'dash_admin/keuangan/logPembayaranUpdate.html'
    success_url = '/'


class LogPembayaranDeleteView(DeleteView):
    model = PemasukanKostModel
    template_name = "dash_admin/dataTamu/profilTamu/profilTamuDelete.html"
    context_object_name = 'ProfilTamu'
    success_url = '/dashadmin/keuangan/logpembayaran/'

#KritikSaran
class kritikSaranListView(ListView):
    model = KritikSaranModel
    template_name = "dash_admin/kritikSaran/kritikSaranList.html"
    context_object_name = 'kritikSaran'
    paginate_by = 10

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
    success_url = '/dashadmin/kritik/1'

#Email
def send_gmail(request, Email):
    obj = ProfilTamuModel.objects.get(Email=Email)
    invoice = ProfilTamuModel.objects.raw('SELECT dash_tamu_profiltamumodel.*, dash_admin_kamarkostmodel.*, dash_tamu_paketkostmodel.*, CASE WHEN dash_tamu_paketkostmodel.Paket = 3 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 12 MONTH WHEN dash_tamu_paketkostmodel.Paket = 2 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 3 MONTH WHEN dash_tamu_paketkostmodel.Paket = 1 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 1 MONTH END AS Bulan_out, dash_admin_kamarkostmodel.Waktu_in + INTERVAL 1 MONTH AS Bulan_in, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik INNER JOIN dash_tamu_paketkostmodel ON dash_admin_kamarkostmodel.Nik=dash_tamu_paketkostmodel.Nik WHERE dash_tamu_profiltamumodel.Email =%s', [Email])
    subject = 'Invoice Gatotkaca Kost'
    to = obj.Email
    html_content = render_to_string("dash_admin/email/emailTempate.html", {'title': 'Invoice Gatotkaca Kost', 'obj' : obj,'invoice' : invoice })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        'gatotkacakost@gatotkaca-network.com',
        [to],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()

    return render(request, 'dash_admin/email/email.html')

#create PDF
def render_pdf_view(request, Nik):
    obj = ProfilTamuModel.objects.raw("SELECT dash_tamu_profiltamumodel.*, dash_admin_kamarkostmodel.*, dash_tamu_paketkostmodel.*, CASE WHEN dash_tamu_paketkostmodel.Paket = 3 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 12 MONTH WHEN dash_tamu_paketkostmodel.Paket = 2 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 3 MONTH WHEN dash_tamu_paketkostmodel.Paket = 1 THEN dash_admin_kamarkostmodel.Waktu_out + INTERVAL 1 MONTH END AS Bulan_out, dash_admin_kamarkostmodel.Waktu_in + INTERVAL 1 MONTH AS Bulan_in, datediff(Waktu_out, current_date()) as selisih FROM dash_tamu_profiltamumodel INNER JOIN dash_admin_kamarkostmodel ON dash_tamu_profiltamumodel.Nik=dash_admin_kamarkostmodel.Nik INNER JOIN dash_tamu_paketkostmodel ON dash_admin_kamarkostmodel.Nik=dash_tamu_paketkostmodel.Nik WHERE dash_tamu_profiltamumodel.Nik =%s", [Nik])
    template_path = 'dash_admin/konfirmasi/pdf1.html'
    context = {'myvar': 'this is your template context', 'obj' : obj}
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