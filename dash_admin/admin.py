from django.contrib import admin
from .models import KamarKostModel,PemasukanKostModel,PengeluaranKostModel

# Register your models here.
admin.site.register(KamarKostModel)
admin.site.register(PemasukanKostModel)
admin.site.register(PengeluaranKostModel)