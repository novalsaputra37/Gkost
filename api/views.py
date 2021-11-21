from django.shortcuts import render
from django.db import connection

#Kamar  No 1
def iotRelayRequestView(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=1')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 2
def iotRelayRequest2View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=2')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 3
def iotRelayRequest3View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=3')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 4
def iotRelayRequest4View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=4')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]

    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 5
def iotRelayRequest5View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=5')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 6
def iotRelayRequest6View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=6')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 7
def iotRelayRequest7View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=7')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 8
def iotRelayRequest8View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=8')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 9
def iotRelayRequest9View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=9')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 10
def iotRelayRequest10View(request):
    context = {}
    cursor = connection.cursor()
    a = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=10')
    if a == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)