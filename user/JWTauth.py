import jwt
import os
from datetime import datetime, timedelta

from django.http import JsonResponse

from user.models import User


JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_EXP_DELTA_HOURS = 1


def make_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXP_DELTA_HOURS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

    return jwt_token.decode('utf-8')


def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        jwt_token = request.COOKIES.get("authorization")

        if not jwt_token:
            return JsonResponse({"error": "login_required"}, status=401)

        try:
            data = jwt.decode(jwt_token, JWT_SECRET, JWT_ALGORITHM)
            User.objects.get(id=data['user_id'])

        except jwt.DecodeError:
            return JsonResponse({"error_code": "INVALID_TOKEN"}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error_code": "EXPIRED_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"error_code": "UNKNOWN_USER"}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper



