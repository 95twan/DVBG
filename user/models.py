from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    nickname = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user'
