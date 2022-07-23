import json
import bcrypt
import jwt
import os
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Account

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if data['username']=='':
                return JsonResponse({"message": "사용할 ID를 입력해 주세요."}, status=401)
            if data['password']=='':
                return JsonResponse({"message": "사용할 비밀번호를 입력해 주세요."}, status=401)
            if data['email']=='':
                return JsonResponse({"message": "사용할 이메일을 입력해 주세요."}, status=401)
            if data['nickname']=='':
                return JsonResponse({"message": "사용할 닉네임을 입력해 주세요."}, status=401)
            if (Account.objects.filter(username=data['username'])).exists():
                return JsonResponse({"message": "이미 있는 ID입니다."}, status=409)
            if (Account.objects.filter(nickname=data['nickname'])).exists():
                return JsonResponse({"message": "이미 있는 닉네임입니다."}, status=409)

            hashedPassword=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            Account(
                username=data['username'],
                hashedPassword=hashedPassword,
                email=data['email'],
                nickname=data['nickname'],
                setting=None,
                notice=None,
            ).save()

            token=jwt.encode({'username':data['username']}, os.environ.get("JWT_SECRET"), os.environ.get("ALGORITHM")).decode('utf-8')
            response=JsonResponse({"username":data['username'], "email":data['email'], "nickname":data['nickname'],
                                   "setting":None, "notice":None, "token": token}, status=200);
            return response

        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Account.objects.filter(username=data['username'])).exists() :
                return JsonResponse({"message": "존재하지 않는 ID입니다."}, status=401)
            user = Account.objects.get(username=data['username'])

            if 'token' in data:
                token=data['token']
                try:
                    decodedToken = jwt.decode(token, os.environ.get("JWT_SECRET"), os.environ.get("ALGORITHM"))
                    if decodedToken['username']==data['username']:
                        token = jwt.encode({'username': data['username']}, os.environ.get("JWT_SECRET"),
                                           os.environ.get("ALGORITHM")).decode('utf-8')
                        response = JsonResponse(
                            {"username": user.username, "email": user.email, "nickname": user.nickname,
                             "setting": user.setting, "notice": user.notice, "token": token}, status=200);
                        return response
                    else:
                         return JsonResponse({"message": "토큰이 잘못되었습니다. (다른 이용자의 토큰)"}, status=401)
                except json.decoder.JSONDecodeError:
                    return JsonResponse({"message": "토큰이 잘못되었습니다."}, status=401)
                except UnicodeError:
                    return JsonResponse({"message": "토큰이 잘못되었습니다."}, status=401)
                except jwt.exceptions.DecodeError:
                    return JsonResponse({"message": "토큰이 잘못되었습니다."}, status=401)

            if data['username'] == "":
                return JsonResponse({"message": "ID를 입력하세요."}, status=401)
            if data['password'] == "":
                return JsonResponse({"message": "비밀번호를 입력하세요."}, status=401)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.hashedPassword.encode('utf-8')):
                token = jwt.encode({'username': data['username']}, os.environ.get("JWT_SECRET"), os.environ.get("ALGORITHM")).decode('utf-8')
                response = JsonResponse({"username":user.username, "email":user.email, "nickname":user.nickname,
                                         "setting":user.setting, "notice":user.notice, "token":token}, status=200);
                return response
            else:
                return JsonResponse({"message": "비밀번호가 틀렸습니다."}, status=401)

        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
