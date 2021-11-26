from django.shortcuts import render
from django.db import connection

#Kamar  No 1
def iotRelayRequestView(request):
    context = {}
    cursor = connection.cursor()
    kamar1 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=1')
    if kamar1 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 2
def iotRelayRequest2View(request):
    context = {}
    cursor = connection.cursor()
    kamar2 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=2')
    if kamar2 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 3
def iotRelayRequest3View(request):
    context = {}
    cursor = connection.cursor()
    kamar3 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=3')
    if kamar3 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 4
def iotRelayRequest4View(request):
    context = {}
    cursor = connection.cursor()
    kamar4 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=4')
    if kamar4 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]

    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 5
def iotRelayRequest5View(request):
    context = {}
    cursor = connection.cursor()
    kamar5 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=5')
    if kamar5 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 6
def iotRelayRequest6View(request):
    context = {}
    cursor = connection.cursor()
    kamar6 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=6')
    if kamar6 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 7
def iotRelayRequest7View(request):
    context = {}
    cursor = connection.cursor()
    kamar7 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=7')
    if kamar7 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 8
def iotRelayRequest8View(request):
    context = {}
    cursor = connection.cursor()
    kamar8 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=8')
    if kamar8 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 9
def iotRelayRequest9View(request):
    context = {}
    cursor = connection.cursor()
    kamar9 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=9')
    if kamar9 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)

#Kamar No 10
def iotRelayRequest10View(request):
    context = {}
    cursor = connection.cursor()
    kamar10 = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=10')
    if kamar10 == 0:
        listrik = 1
    else:
        listrik = cursor.fetchone()[0]
    context['listrik'] = listrik
    return render(request, 'api/bacaRelay.html', context)