from django.core.validators import validate_email

from user.models import User


def is_empty(data, msg="data is empty"):
    if not data:
        raise Exception(msg)

    return data


def username_check(username):
    is_empty(username, "username is empty")
    if User.objects.filter(username=username).exists():
        raise Exception("Duplicate username")


def password_check(password):
    is_empty(password, "password is empty")


def nickname_check(nickname):
    is_empty(nickname, "nickname is empty")
    if User.objects.filter(nickname=nickname).exists():
        raise Exception("Duplicate nickname")


def email_check(email):
    is_empty(email, "nickname is empty")
    validate_email(email)


def access_token_check(token):
    is_empty(token, "token is empty")

