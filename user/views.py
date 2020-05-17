import json
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from user.models import User, LoginProvider
from user.jwt_auth import make_token
import user.validation as valid


class BaseRegister(View):
    def is_valid(self, data):
        valid.nickname_check(data["nickname"])
        valid.email_check(data["email"])

        return data

    def user_register(self, user_data):
        return User.objects.create(**user_data)


class SelfRegister(BaseRegister):
    def post(self, request):
        json_data = json.loads(request.body)

        try:
            user = User.create_user(json_data)
            user.save()
        except Exception as e:
            print(e)
            error = {
                "error": "self-register",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)

        return JsonResponse(json_data["user"], status=201)


class OAuthRegister(BaseRegister):
    def post(self, request):
        json_data = json.loads(request.body)

        try:
            user_data, provider = self.is_valid(json_data)
        except Exception as e:
            print(e)
            error = {
                "error": "oauth-register",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)

        if user_data:
            user = self.user_register(user_data)
            provider["user_id"] = user.id

        LoginProvider.objects.create(**provider)

        return JsonResponse(json_data, status=201)

    def is_valid(self, data):
        user = valid.is_empty(data.get("user"), "user data set is empty")
        print(user)
        if user:
            super().is_valid(data["user"])

        provider = valid.is_empty(data.get("provider"), "provider data set is empty")

        valid.is_empty(provider.get("provider"), "provider is empty")
        valid.is_empty(provider.get("access_token"), "access_token is empty")
        valid.is_empty(provider.get("refresh_token"), "refresh_token is empty")

        return user, provider


class BaseLogin(View):
    # guest login은 여기서 담당
    def response(self, user_id):
        # token 발급
        token = make_token(user_id)
        # 질문 2: token에 어떤 정보를 담아야 하나??
        # header에 set_cookie
        res_data = {
            "success": "Login"
        }
        res = JsonResponse(res_data, status=200)
        res.set_cookie('authorization', token)
        return res


class SelfLogin(BaseLogin):
    def post(self, request):
        json_data = json.loads(request.body)

        try:
            valid_data = self.is_valid(json_data)
        except Exception as e:
            print(e)
            error = {
                "error": "self-login",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)

        try:
            user_id = self.login(valid_data)
        except Exception as e:
            print(e)
            error = {
                "error": "self-login",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)
        else:
            return self.response(user_id)

    def is_valid(self, data):
        valid.is_empty(data.get("username"), "username is empty")
        valid.is_empty(data.get("password"), "password is empty")
        return data

    def login(self, data):
        username = data["username"]
        password = data["password"]

        # username이 db에 존재하는지
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception('id or password is not valid')

        # password 비교
        if not check_password(password, user.password):
            raise Exception('id or password is not valid')

        return user.id


class OAuthLogin(BaseLogin):
    # OAuth로 로그인하면 무슨 데이터가 오나???
    def post(self, request):
        json_data = json.loads(request.body)

        try:
            valid_data = self.is_valid(json_data)
        except Exception as e:
            print(e)
            error = {
                "error": "oauth-login",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)

        try:
            self.login(valid_data)
        except Exception as e:
            print(e)
            error = {
                "error": "oauth-login",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)
        else:
            return self.response()

    def is_valid(self, data):
        # access_token이 유효한지
        valid.access_token_check(data.get("access_token"))

        # 유효하지 않다면 access_token 재발급
        self.token_reissue()

        return data

    def token_reissue(self, refresh_token):
        pass

    def login(self, data):
        return True
