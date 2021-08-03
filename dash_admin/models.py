from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class KamarKostModel(models.Model):
    Nik              = models.CharField(max_length=50)
    No_kamar         = models.IntegerField()
    Waktu_in         = models.DateField()
    Waktu_out        = models.DateField()

    def __str__(self):
        return "{}. {}".format(self.id, self.Nik)

class PemasukanKostModel(models.Model):
    Nik              = models.CharField(max_length=50)
    Tgl_pemasukan    = models.DateField(default=datetime.datetime.now)
    Jmlh_pemasukan   = models.IntegerField()
    Keterangan       = models.CharField(max_length=50)

    def __str__(self):
        return "{}. {}".format(self.id, self.Nik)

class PengeluaranKostModel(models.Model):
    Pengeluaran       = models.CharField(max_length=50)
    Tgl_pengeluaran   = models.DateField()
    jmlh_pengeluaran  = models.IntegerField()

    def __str__(self):
        return "{}. {}".format(self.id, self.Pengeluaran)