from django import forms
from .models import KamarKostModel,PemasukanKostModel,PengeluaranKostModel

class KamarKostForm(forms.ModelForm):
    
    class Meta :
        model = KamarKostModel
        fields = [
            'Nik',
            'No_kamar',
            'Waktu_in',
            'Waktu_out'
        ]

        widgets = {
            'Nik' : forms.NumberInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan NIK KTP',
                }
            ),
            'No_kamar' : forms.NumberInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan No_kamar',
                    
                }
            ),
            'Waktu_in' : forms.DateInput(
                attrs ={
                    'class' : 'form-control',
                    'type'  : 'date'
                }
            ),
            'Waktu_out' : forms.DateInput(
                attrs ={
                    'class' : 'form-control',
                    'type'  : 'date'
                }
            ),
        }
    
class PemasukanKostForm(forms.ModelForm):
    class Meta :
        model = PemasukanKostModel
        fields = [
            'Nik',
            'Tgl_pemasukan',
            'Jmlh_pemasukan',
            'Keterangan'
        ]

        widgets = {
            'Nik' : forms.TextInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan NIK KTP',
                    
                }
            ),
            'Tgl_pemasukan' : forms.DateInput(
                attrs ={
                    'class' : 'form-control',
                    'type'  : 'date',
                    
                }
            ),
            'Jmlh_pemasukan' : forms.NumberInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan Jmlh_pemasukan',
                }
            ),
            'Keterangan' : forms.TextInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Keterangan',
                }
            ),
        }