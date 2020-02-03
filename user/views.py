import json
from django.views.generic import View
from user.models import User, LoginProvider
from django.http import JsonResponse


class BaseRegister(View):
    def check_nickname(self, nickname):
        pass

    def check_email(self, email):
        pass

    def is_valid(self, data):
        self.check_nickname(data["nickname"])
        self.check_email(data["email"])

        return data

    def user_register(self, user_data):
        return User.objects.create(**user_data)


class SelfRegister(BaseRegister):
    def post(self, request):
        json_data = json.loads(request.body)
        user_data = json_data["user"]

        # validate check
        valid_user_data = self.is_valid(user_data)

        # USER 저장
        self.user_register(valid_user_data)

        # 일단 아무거나 반환
        return JsonResponse(user_data, status=201)

    def is_valid(self, data):
        # username && password null 체크
        # username 중복 체크
        # password 암호화???
        return super().is_valid(data)


class OAuthRegister(BaseRegister):
    def post(self, request):
        json_data = json.loads(request.body)
        user_data = json_data["user"]
        provider = json_data["provider"]

        # validate check
        valid_user_data = self.is_valid(user_data)

        # USER 저장
        user = self.user_register(valid_user_data)

        provider["user_id"] = user.id

        # LOGIN_PROVIDER 저장
        LoginProvider.objects.create(**provider)

        return JsonResponse(json_data, status=201)
