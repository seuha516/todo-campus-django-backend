import random
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Create your views here.
def makeRandomString():
    keyword=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    result=''
    for i in range (36):
        result+=keyword[random.randrange(0, 36)]
    return str(datetime.datetime.now()).replace(" ","").replace(".","").replace(":","") + '_' + result

@csrf_exempt
def post(request):
    if request.method == 'POST':
        try:
            key = makeRandomString()+'.'+str(request.FILES['image'].content_type[6:])
            FileSystemStorage().save(key, request.FILES['image'])
            return JsonResponse({"id": key }, status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
