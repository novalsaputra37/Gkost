# Generated by Django 3.2.5 on 2021-07-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_tamu', '0002_paketkostmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='KritikSaranModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nik', models.CharField(max_length=50)),
                ('Kritik', models.CharField(max_length=250)),
                ('Saran', models.CharField(max_length=250)),
            ],
        ),
    ]
