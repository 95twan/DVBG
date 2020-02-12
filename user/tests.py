import json
from django.test import TestCase


class SelfRegisterLoginTest(TestCase):

    def test_self_register(self):
        res_code = self.register()

        self.assertEqual(res_code, 201)

    def test_self_login(self):
        self.register()

        user = {
            "username": "user5",
            "password": "password",
        }

        res = self.client.post("/api/user/selflogin/", json.dumps(user), content_type="application/json")

        self.assertEqual(res.status_code, 200)

    def register(self):
        user = {
            "user": {
                "username": "user5",
                "password": "password",
                "nickname": "nick5",
                "email": "test@gmail.com"
            }
        }
        res = self.client.post("/api/user/selfregister/", json.dumps(user), content_type="application/json")

        return res.status_code



