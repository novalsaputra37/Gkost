from django.db import models

# Create your models here.
class ProfilTamuModel(models.Model):
    Nik             = models.CharField(max_length=50)
    Nama_lengkap    = models.CharField(max_length=50)
    No_tlp          = models.BigIntegerField()
    Email           = models.CharField(max_length=255)
    Tempat_lahir    = models.CharField(max_length=50)
    Tanggal_lahir   = models.DateField()
    Agama           = models.CharField(max_length=50)
    Pekerjaan       = models.CharField(max_length=50)
    Jenis_kelamin   = models.CharField(max_length=50)
    Alamat_asal     = models.CharField(max_length=255)
    Foto_ktp        = models.ImageField(upload_to='foto_ktp')
    published       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}. {}".format(self.id, self.Nik)

class PaketKostModel(models.Model):
    Nik             = models.CharField(max_length=50)
    Paket           = models.CharField(max_length=50)
    
    def __str__(self):
        return "{}. {}".format(self.id, self.Nik)

class KritikSaranModel(models.Model):
    Nik             = models.CharField(max_length=50)
    Kritik          = models.CharField(max_length=250)
    Saran           = models.CharField(max_length=250)

    def __str__(self) :
        return "{}. {}".format(self.id, self.Nik)