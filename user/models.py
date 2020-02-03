from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    nickname = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user'


class LoginProvider(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    provider = models.CharField(max_length=45)
    access_token = models.CharField(max_length=128)
    refresh_token = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'login_provider'
