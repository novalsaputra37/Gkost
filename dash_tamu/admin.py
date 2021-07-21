from django.contrib import admin
from .models import RegisterTamuModel,PaketKostModel,KritikSaranModel

class RegisterTamuAdmin(admin.ModelAdmin):
    readonly_fields=[
        'published',
        'updated'
    ]
    
# Register your models here.
admin.site.register(RegisterTamuModel, RegisterTamuAdmin)
admin.site.register(PaketKostModel)
admin.site.register(KritikSaranModel)