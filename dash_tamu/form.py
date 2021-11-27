from django import forms
from .models import (
                    ProfilTamuModel,
                    PaketKostModel,
                    KritikSaranModel
                    )

class ProfilTamuForm(forms.ModelForm):
    class Meta :
        model = ProfilTamuModel
        fields = [
            'Nik',
            'Nama_lengkap',
            'No_tlp',
            'Email',
            'Tempat_lahir',
            'Tanggal_lahir',
            'Agama',
            'Pekerjaan',
            'Jenis_kelamin',
            'Alamat_asal',
            'Foto_ktp',
        ]

        widgets = {
            'Nik' : forms.TextInput(
                attrs ={
                    'class' : 'form-control',
                    'placeholder' : 'Masukan NIK KTP',
                    
                }
            ),

            'Nama_lengkap': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Masukan Nama Lengkap',
                    }
				),
            
            'No_tlp': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Masukan no Telpon',
                    }
				),
            
            'Email': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Masukan Email',
                    }
				),

            'Tempat_lahir': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Masukan Tempat Lahir',
                    }
				),

            'Tanggal_lahir': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'type'  : 'date',
                    }
				),

            'Agama': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Agama',
                    
                    }
				),
            
            'Pekerjaan': forms.TextInput(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Pekerjaan',
                    
                    }
				),

            'Jenis_kelamin': forms.RadioSelect(
                choices = {('pria','pria'),('wanita','wanita'),},
				),

            'Alamat_asal': forms.Textarea(
				attrs = {
					'class':'form-control',
                    'placeholder' : 'Alamat Asal',}
				),
        }
    
    PILIHAN = (
			('nilai 1','Pilihan 1'),
			('nilai 2','Pilihan 2'),
			('nilai 3','Pilihan 3'),
		)

class PaketKostForm(forms.ModelForm):
    class Meta :
        model = PaketKostModel
        fields = [
            'Nik',
            'Paket'
        ]

        PILIHAN = (
			('1','Paket 1'),
			('2','Paket 2'),
			('3','Paket 3'),
		)

        widgets = {
            'Nik' : forms.TextInput(
                attrs ={
                    'class' : 'form-control',
                }
            ),

            'Paket': forms.Select(
                choices= PILIHAN,
				attrs = {
					'class':'form-control',
                    }
				),
        }

class KritikSaranForm(forms.ModelForm):
    class Meta :
        model = KritikSaranModel
        fields = [
            'Nik',
            'Kritik',
            'Saran'
        ]