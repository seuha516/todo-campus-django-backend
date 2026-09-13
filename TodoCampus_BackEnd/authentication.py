import os
from functools import wraps

import jwt
from django.http import JsonResponse


def require_jwt(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        header = request.headers.get('Authorization', '')
        if not header.startswith('Bearer '):
            return JsonResponse({'message': '인증이 필요합니다.'}, status=401)
        try:
            payload = jwt.decode(header[7:], os.environ.get('JWT_SECRET'), os.environ.get('ALGORITHM'))
            request.auth_username = payload['username']
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError, KeyError):
            return JsonResponse({'message': '유효하지 않은 토큰입니다.'}, status=401)
        return view(request, *args, **kwargs)
    return wrapped
