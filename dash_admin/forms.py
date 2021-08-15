from decimal import Clamped
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
                    'id' : 'state',
                    'class' : 'form-control w-100',
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
                    'id' : 'birthday',
                    'class' : 'form-control',
                    'type'  : 'text',
                    'data-datepicker' : "",
                    'placeholder' : 'dd/mm/yyyy'
                }
            ),
            'Waktu_out' : forms.DateInput(
                attrs ={
                    'id' : 'birthday',
                    'class' : 'form-control',
                    'type'  : 'text',
                    'data-datepicker' : "",
                    'placeholder' : 'dd/mm/yyyy'
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
                    'id' : 'birthday',
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

class PengeluaranKostForm(forms.ModelForm):
    class Meta :
        model = PengeluaranKostModel
        fields = [
            'Pengeluaran',
            'Tgl_pengeluaran',
            'jmlh_pengeluaran'
        ]

        widgets = {
            'Pengeluaran' : forms.TextInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan Pengeluaran',
                    
                }
            ),
            'Tgl_pengeluaran' : forms.DateInput(
                attrs ={
                    'class' : 'form-control',
                    'type'  : 'date',
                }
            ),
            'jmlh_pengeluaran' : forms.NumberInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan jmlh_pengeluaran',
                }
            ),
        }