from django.db import connection
import json
from django.http import HttpResponse

def my_view(request):
    x = 1
    while (x <= 10):
        cursor = connection.cursor()
        kamar = cursor.execute('SELECT CASE WHEN datediff(Waktu_out, current_date()) >= 0 THEN 0 ELSE 1 END as listrik  FROM dash_admin_kamarkostmodel WHERE No_kamar=%s', [x])
        if kamar == 0:
            lampu = 1
        else:
            lampu = cursor.fetchone()[0]
        
        print(lampu)

        if x == 1:
            kamar1 = lampu
        elif x == 2:
            kamar2 = lampu
        elif x == 3:
            kamar3 = lampu
        elif x == 4:
            kamar4 = lampu
        elif x == 5:
            kamar5 = lampu
        elif x == 6:
            kamar6 = lampu
        elif x == 7:
            kamar7 = lampu
        elif x == 8:
            kamar8 = lampu
        elif x == 9:
            kamar9 = lampu
        elif x == 10:
            kamar10 = lampu
        x = x + 1

    data = {
        'kamar1' : kamar1,
        'kamar2' : kamar2,
        'kamar3' : kamar3,
        'kamar4' : kamar4,
        'kamar5' : kamar5,
        'kamar6' : kamar6,
        'kamar7' : kamar7,
        'kamar8' : kamar8,
        'kamar9' : kamar9,
        'kamar10' : kamar10,
    }

    listrik = {
        'listrik' : data,
    }
    dump = json.dumps(listrik)

    return HttpResponse(dump, content_type='application/json')