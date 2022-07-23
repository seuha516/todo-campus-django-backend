import re
from datetime import timedelta
from datetime import datetime
from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Calendar

# Create your views here.
def daysOfYear(year):
    if year%400==0:
        return 366;
    elif year%100==0:
        return 365;
    elif year%4==0:
        return 366;
    else:
        return 365;
def daysOfMonth(year, month):
    if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
        return 31;
    elif month==4 or month==6 or month==9 or month==11:
        return 30;
    elif month==2:
        return daysOfYear(year)-337;
def dateToNumber(year, month, day):
    result=0
    for i in range(1, year):
        result+=daysOfYear(i)
    for i in range(1, month):
        result+=daysOfMonth(year, i)
    return result+day
def getSt(year, month):
    st=dateToNumber(year,month,1)
    mid=(42-daysOfMonth(year,month))/2
    if abs(mid-(st%7)) < abs(mid-(st%7)-7):
        st-=(st%7)
    else:
        st-=(st%7)+7
    return st

@csrf_exempt
def getList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            cursor = connection.cursor()
            strSQL = "SELECT * FROM calendar WHERE username = \"" + data['username'] + "\";"
            cursor.execute(strSQL)
            resultSQL = cursor.fetchall()
            connection.close()

            st=getSt(data['year'],data['month'])
            end=getSt(data['year'],data['month'])+41
            result = [];
            for i in range(42):
                result.append([])

            for i in resultSQL:
                j = {
                    'num': i[0],
                    'username': i[1],
                    'name': i[2],
                    'color': i[3],
                    'content': i[4],
                    'location': i[5],
                    'start': i[6],
                    'end': i[7],
                }
                jst=dateToNumber(j['start'].year,j['start'].month,j['start'].day)
                jend=dateToNumber(j['end'].year, j['end'].month, j['end'].day)
                if jst <= st <= jend:
                    for k in range (st, min(end,jend)+1):
                        result[k-st].append(j)
                elif st <= jst <= end:
                    for k in range (jst, min(end,jend)+1):
                        result[k-st].append(j)

            return JsonResponse({"result":result},status=200)
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
            if data['start']>data['end']:
                return JsonResponse({"message": "시작 시간이 종료 시간보다 늦습니다."}, status=401)

            Calendar(
                username=data['username'],
                name=data['name'],
                color=data['color'],
                content=data['content'],
                location=data['location'],
                start=datetime.strptime(data['start'],"%Y-%m-%dT%H:%M:%S.%fZ")+timedelta(hours=9),
                end=datetime.strptime(data['end'],"%Y-%m-%dT%H:%M:%S.%fZ")+timedelta(hours=9),
            ).save()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if data['name'] == '':
                return JsonResponse({"message": "이름을 반드시 입력해야 합니다."}, status=401)
            colorRegex = re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
            if not colorRegex.search(data['color']):
                return JsonResponse({"message": "색상이 올바르지 않습니다."}, status=401)
            if data['start']>data['end']:
                return JsonResponse({"message": "시작 시간이 종료 시간보다 늦습니다."}, status=401)

            if not (Calendar.objects.filter(num=data['num'])).exists() :
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            Calendar.objects.filter(num=data['num']).update(
                username=data['username'],
                name=data['name'],
                color=data['color'],
                content=data['content'],
                location=data['location'],
                start=datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9),
                end=datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9),
            )
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Calendar.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            target = Calendar.objects.get(num=data['num'])
            target.delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
