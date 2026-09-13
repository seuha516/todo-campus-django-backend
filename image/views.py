import random
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from TodoCampus_BackEnd.authentication import require_jwt

# Create your views here.
def makeRandomString():
    keyword=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    result=''
    for i in range (36):
        result+=keyword[random.randrange(0, 36)]
    return str(datetime.datetime.now()).replace(" ","").replace(".","").replace(":","") + '_' + result

@csrf_exempt
@require_jwt
def post(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            allowed_types = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif', 'image/webp': 'webp'}
            if image.content_type not in allowed_types or image.size > 5 * 1024 * 1024:
                return JsonResponse({"message": "지원하지 않는 이미지입니다."}, status=400)
            key = makeRandomString()+'.'+allowed_types[image.content_type]
            FileSystemStorage().save(key, image)
            return JsonResponse({"id": key }, status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
