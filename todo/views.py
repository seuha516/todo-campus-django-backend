from datetime import timedelta
from datetime import datetime
from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Todo

# Create your views here.
@csrf_exempt
def getList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            cursor = connection.cursor()
            if data['category'] == 'all0000000000':
                strSQL = "SELECT * FROM todo WHERE username=\"%s\" ORDER BY noted DESC, due ASC" % data['username']
            elif data['category'] == 'noted0000000000':
                strSQL = "SELECT * FROM todo WHERE username=\"%s\" AND (noted = 1 OR noted = -1) ORDER BY due ASC" % data['username']
            elif data['category'] == 'done0000000000':
                strSQL = "SELECT * FROM todo WHERE username=\"%s\" AND (due < NOW() OR noted < 0) ORDER BY noted DESC, due ASC" % data['username']
            else:
                strSQL = "SELECT * FROM todo WHERE username=\"%s\" AND category=\"%s\" ORDER BY noted DESC, due ASC" % (data['username'], data['category'])

            listSQL="SELECT DISTINCT category FROM todo WHERE username=\"%s\"" % data['username']
            cursor.execute(listSQL)
            sqlData = cursor.fetchall()
            categoryList = []
            isNone=False
            for i in sqlData:
                if i[0]=='':
                    isNone=True
                else:
                    categoryList.append(i[0])
            if isNone:
                categoryList.insert(0,'')

            cursor.execute(strSQL)
            sqlData = cursor.fetchall()
            connection.close()
            result = []
            for i in sqlData:
                j = {
                    'num': i[0],
                    'username': i[1],
                    'title': i[2],
                    'category': i[3],
                    'noted': i[4],
                    'due': i[5],
                }
                result.append(j)

            return JsonResponse({"result": result, "categoryList":categoryList}, status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def write(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try: 
            if data['title']== '':
                return JsonResponse({"message": "제목을 반드시 입력해야 합니다."}, status=401)
            if datetime.strptime(data['due'], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9) < datetime.now():
                return JsonResponse({"message": "기한을 과거로 설정할 수 없습니다."}, status=401)
            Todo(
                username=data['username'],
                title=data['title'],
                category=data['category'],
                noted=0,
                due=datetime.strptime(data['due'], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9),
            ).save()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Todo.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            Todo.objects.filter(num=data['num']).update(
                noted=data['noted'],
            )
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Todo.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "데이터를 찾을 수 없습니다."}, status=401)
            target = Todo.objects.get(num=data['num'])
            target.delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

