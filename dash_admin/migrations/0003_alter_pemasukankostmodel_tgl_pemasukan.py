# Generated by Django 3.2.5 on 2021-08-02 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dash_admin', '0002_auto_20210722_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pemasukankostmodel',
            name='Tgl_pemasukan',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
