import math
import json
import re
from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import WeekTable

# Create your views here.
@csrf_exempt
def getList(request):
    if request.method == 'POST':
        key = JSONParser().parse(request)['username']
        try:
            cursor = connection.cursor()
            strSQL = "SELECT * FROM weektable WHERE username = \"" + key + "\";"
            cursor.execute(strSQL)
            data = cursor.fetchall()
            connection.close()

            daysInWeek = 5
            minTime = 480
            maxTime = 1140
            courseCount = 0
            totalCredit = 0
            result = [];
            for i in data:
                j = {
                    'num': i[0],
                    'name': i[2],
                    'color': i[3],
                    'etc': i[4],
                    'credit': i[5],
                    'professor': i[6],
                    'time': json.loads(i[7])
                }
                result.append(j);

                courseCount += 1
                totalCredit = totalCredit + i[5]
                for j in json.loads(i[7]):
                    minTime = min(minTime, j['start'])
                    maxTime = max(maxTime, j['start'] + j['time'])
                    if j['whatDay'] == 'Sat':
                        daysInWeek = max(daysInWeek, 6)
                    elif j['whatDay'] == 'Sun':
                        daysInWeek = 7

            minTime = max(0, math.floor(minTime / 60) - 1)
            maxTime = min(24, math.ceil(maxTime / 60) + 1)
            return JsonResponse({'list': result, 'daysInWeek': daysInWeek, 'minTime': minTime, 'maxTime': maxTime,
                                 'courseCount': courseCount, 'totalCredit': totalCredit}, status=200)

        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def insert(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if data['name']== '':
                return JsonResponse({"message": "이름을 반드시 입력해야 합니다."}, status=401)
            colorRegex=re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
            if not colorRegex.search(data['color']):
                return JsonResponse({"message": "색상이 올바르지 않습니다."}, status=401)
            if data['credit']=='':
                data['credit']=0
            elif int(data['credit']) < 0:
                return JsonResponse({"message": "학점이 올바르지 않습니다."}, status=401)
            else:
                data['credit']=int(data['credit'])

            cursor = connection.cursor()
            strSQL = "SELECT * FROM weektable WHERE username = \"" + data['username'] + "\";"
            cursor.execute(strSQL)
            sqlData = cursor.fetchall()
            connection.close()

            for i in sqlData:
                time=json.loads(i[7])
                for j in time:
                    for k in data['time']:
                        if k['time']==0:
                            return JsonResponse({"message": "0분짜리 일정을 넣을 수 없습니다."}, status=401)
                        if j['whatDay'] != k['whatDay']:
                            break;
                        if j['start'] <= k['start'] < j['start'] + j['time'] or k['start'] <= j['start'] < k[
                            'start'] + k['time']:
                            return JsonResponse({"message": "이미 있는 일정과 겹칩니다."},status=412)

            WeekTable(
                username=data['username'],
                name=data['name'],
                color=data['color'],
                etc=data['etc'],
                credit=data['credit'],
                professor=data['professor'],
                time=data['time'],
            ).save()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if data['name']== '':
                return JsonResponse({"message": "이름을 반드시 입력해야 합니다."}, status=401)
            colorRegex=re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
            if not colorRegex.search(data['color']):
                return JsonResponse({"message": "색상이 올바르지 않습니다."}, status=401)
            if data['credit']=='':
                data['credit']=0
            elif int(data['credit']) < 0:
                return JsonResponse({"message": "학점이 올바르지 않습니다."}, status=401)
            else:
                data['credit']=int(data['credit'])

            cursor = connection.cursor()
            strSQL = "SELECT * FROM weektable WHERE username = \"" + data['username'] + "\";"
            cursor.execute(strSQL)
            sqlData = cursor.fetchall()
            connection.close()

            for i in sqlData:
                if i[0]==data['num']:
                    continue;
                time=json.loads(i[7])
                for j in time:
                    for k in data['time']:
                        if k['time']==0:
                            return JsonResponse({"message": "0분짜리 일정을 넣을 수 없습니다."}, status=401)
                        if j['whatDay'] != k['whatDay']:
                            break;
                        if j['start'] <= k['start'] < j['start'] + j['time'] or k['start'] <= j['start'] < k[
                            'start'] + k['time']:
                            return JsonResponse({"message": "이미 있는 일정과 겹칩니다."},status=412)

            if not (WeekTable.objects.filter(num=data['num'])).exists() :
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            WeekTable.objects.filter(num=data['num']).update(
                username=data['username'],
                name=data['name'],
                color=data['color'],
                etc=data['etc'],
                credit=data['credit'],
                professor=data['professor'],
                time=data['time'],
            )
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (WeekTable.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            target = WeekTable.objects.get(num=data['num'])
            target.delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
