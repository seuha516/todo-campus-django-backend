import datetime
import random
import json
from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Post

# Create your views here.
def makeRandomString():
    keyword=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
    result=''
    for i in range (36):
        result+=keyword[random.randrange(0, 36)]
    return str(datetime.datetime.now()).replace(" ","").replace(".","").replace(":","") + '_' + result
pageVolume=5

@csrf_exempt
def getList(request):
    if request.method == 'GET':
        try:
            page=1
            tag=''
            if 'page' in request.GET:
                page=int(request.GET['page'])
            if 'tag' in request.GET:
                tag=request.GET['tag']
            if page < 1:
                return JsonResponse({"message": "페이지가 잘못되었습니다."}, status=500)

            cursor = connection.cursor()
            if tag=='':
                strSQL="SELECT `num`, `nickname`, `title`, `body`, `publishedDate`, `comment`, `like` FROM post ORDER BY publishedDate DESC LIMIT %d, %d" % ((page-1)*pageVolume, pageVolume)
            else:
                strSQL = "SELECT `num`, `nickname`, `title`, `body`, `publishedDate`, `comment`, `like` FROM post WHERE %s MEMBER OF( tag ) ORDER BY publishedDate DESC LIMIT %d, %d" % ('\"%s\"' % tag, (page - 1) * pageVolume, pageVolume)
            cursor.execute(strSQL)
            sqlData = cursor.fetchall()
            connection.close()

            result=[]
            for i in sqlData:
                j = {
                    'num': i[0],
                    'nickname': i[1],
                    'title': i[2],
                    'body': i[3],
                    'publishedDate': i[4],
                    'comment': json.loads(i[5]),
                    'like': json.loads(i[6]),
                }
                result.append(j)

            return JsonResponse({"result":result}, status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def read(request,num):
    if request.method == 'GET':
        try:
            if not (Post.objects.filter(num=num)).exists() :
                return JsonResponse({"message": "글을 찾을 수 없습니다."}, status=401)
            target=Post.objects.get(num=num)
            return JsonResponse({'num':target.num,'username':target.username,'nickname':target.nickname,
                                 'title':target.title,'body':target.body,'image':target.image,
                                 'publishedDate':target.publishedDate,'lastModifiedDate':target.lastModifiedDate,
                                 'tag':target.tag,'comment':target.comment,'like':target.like}, status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def write(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if data['title']== '':
                return JsonResponse({"message": "제목을 입력해야 합니다."}, status=401)
            if data['body']== '':
                return JsonResponse({"message": "내용을 입력해야 합니다."}, status=401)
            now=datetime.datetime.now()
            Post(
                username=data['username'],
                nickname=data['nickname'],
                title=data['title'],
                body=data['body'],
                image=data['image'],
                tag=data['tag'],
                comment=[],
                like=[],
                publishedDate=now,
                lastModifiedDate=now,
            ).save()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if data['title'] == '':
                return JsonResponse({"message": "제목을 입력해야 합니다."}, status=401)
            if data['body'] == '':
                return JsonResponse({"message": "내용을 입력해야 합니다."}, status=401)
            if not (Post.objects.filter(num=data['num'])).exists() :
                return JsonResponse({"message": "글을 찾을 수 없습니다."}, status=401)

            Post.objects.filter(num=data['num']).update(
                nickname=data['nickname'],
                title=data['title'],
                body=data['body'],
                image=data['image'],
                tag=data['tag'],
                lastModifiedDate=datetime.datetime.now(),
            )
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Post.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "글을 찾을 수 없습니다."}, status=401)
            target = Post.objects.get(num=data['num'])
            target.delete()
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)

@csrf_exempt
def addComment(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            if not (Post.objects.filter(num=data['num'])).exists():
                return JsonResponse({"message": "게시글을 찾을 수 없습니다."}, status=401)
            post = Post.objects.get(num=data['num'])
            comment = post.comment
            like = post.like
            key = makeRandomString()

            if data['type']=='addComment':
                if data['comment'] == '':
                    return JsonResponse({"message": "빈 댓글은 입력할 수 없습니다."}, status=401)
                if data['commentId'] == '':
                    newComment = {'commentId': key, 'comment': data['comment'], 'nickname': data['nickname'],
                                  'username': data['username'], 'reply': False, 'date': str(datetime.datetime.now()),
                                  'die': False}
                    comment.append(newComment)
                else:
                    newComment = {'commentId': data['commentId'][:59]+key, 'comment': data['comment'], 'nickname': data['nickname'],
                                  'username': data['username'], 'reply': True, 'date': str(datetime.datetime.now()),
                                  'die': False}
                    idx=-1
                    for i in range(len(comment)):
                        c=comment[i]
                        if c['commentId'][:59] == data['commentId'][:59]:
                            idx=i
                    if idx>=0:
                        comment.insert(idx+1, newComment)

                Post.objects.filter(num=data['num']).update(
                    comment=comment,
                )
                return HttpResponse(status=200)
            elif data['type']=='removeComment':
                for i in range(len(comment)):
                    if comment[i]['commentId'] == data['commentId']:
                        comment[i]['die']=True
                        break
                Post.objects.filter(num=data['num']).update(
                    comment=comment,
                )
                return HttpResponse(status=200)
            elif data['type']=='like':
                can=True
                for i in range(len(like)):
                    if like[i] == data['username']:
                        can=False
                        break
                if can:
                    like.append(data['username'])
                    Post.objects.filter(num=data['num']).update(
                        like=like,
                    )
                else:
                    return JsonResponse({"message": "이미 좋아요를 눌렀습니다."}, status=401)
                return HttpResponse(status=200)
            else:
                return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
        except KeyError:
            return JsonResponse({"message": "알 수 없는 오류가 발생했습니다."}, status=500)
