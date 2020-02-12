import json
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from user.models import User, LoginProvider
from user.JWTauth import make_token
import user.validation as valid


class BaseRegister(View):
    # 질문4: 중복 체크 할 때 저장하기 전에 미리 체크 한 후에 한다 아니면 저장할때 발생하는 오류로 체크한다.
    # 질문5: 가입 할때 username이나 nickname의 중복 체크를 따로 요청하는지?
    def is_valid(self, data):
        valid.nickname_check(data["nickname"])
        valid.email_check(data["email"])

        return data

    def user_register(self, user_data):
        return User.objects.create(**user_data)


class SelfRegister(BaseRegister):
    def post(self, request):
        json_data = json.loads(request.body)
        user_data = json_data["user"]

        # validate check
        try:
            valid_user_data = self.is_valid(user_data)
        except Exception as e:
            print(e)
            error = {
                "error": "self-register",
                "msg": str(e)
            }
            return JsonResponse(error, status=400)
        else:
            # USER 저장
            # password 암호화???
            valid_user_data["password"] = make_password(valid_user_data["password"])
            self.user_register(valid_user_data)

            return JsonResponse(user_data, status=201)

    def is_valid(self, data):
        # username && password valid 체크
        valid.username_check(data.get("username"))
        valid.password_check(data.get("password"))

        return super().is_valid(data)


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
    # 질문3: OAuth로 로그인하면 무슨 데이터가 오나???
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
