from django.db import models

from user.models import User
from blog.models import Blog


class Subscribe(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    blog = models.ForeignKey(Blog, models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'subscribe'
