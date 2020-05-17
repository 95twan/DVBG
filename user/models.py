from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=45, unique=True)
    email = models.EmailField(max_length=45)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    @classmethod
    def create_user(cls, data):
        assert data.get("user")
        user_data = data["user"]
        assert user_data.get("username")
        assert user_data.get("password")
        assert user_data.get("nickname")
        assert user_data.get("email")

        validate_email(user_data["email"])

        return cls(
            username=user_data["username"],
            password=user_data["password"],
            nickname=user_data["nickname"],
            email=user_data["email"]
        )

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


class LoginProvider(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    provider = models.CharField(max_length=45)
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=128)

    class Meta:
        db_table = 'login_provider'
