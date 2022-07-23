from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Memo

# Create your views here.
@csrf_exempt
def getList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            cursor = connection.cursor()
            strSQL = "SELECT * FROM memo WHERE username = \"" + data['username'] + "\" ORDER BY num DESC"
            cursor.execute(strSQL)
            sqlData = cursor.fetchall()
            connection.close()

            result=[]
            for i in sqlData:
                j = {
                    'num': i[0],
                    'username': i[1],
                    'body': i[2],
                }
                result.append(j)

            return JsonResponse({"result":result}, status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def write(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            Memo(
                username=data['username'],
                body=data['body'],
            ).save()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Memo.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            Memo.objects.filter(num=data['num']).update(
                body=data['body'],
            )
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Memo.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            target = Memo.objects.get(num=data['num'])
            target.delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

