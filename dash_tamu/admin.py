from django.contrib import admin
from .models import ProfilTamuModel,PaketKostModel,KritikSaranModel

class ProfilTamuAdmin(admin.ModelAdmin):
    readonly_fields=[
        'published',
        'updated'
    ]
    
# Register your models here.
admin.site.register(ProfilTamuModel, ProfilTamuAdmin)
admin.site.register(PaketKostModel)
admin.site.register(KritikSaranModel)