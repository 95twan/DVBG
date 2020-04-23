from django.db import models
from user.models import User


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'blog'


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blog, models.CASCADE)
    name = models.CharField(max_length=45)
    is_hidden = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'board'


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=45)
    content = models.TextField()
    tag = models.CharField(max_length=45, blank=True, null=True)
    author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    is_hidden = models.BooleanField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, models.CASCADE)
    user = models.ForeignKey(User, models.DO_NOTHING)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=45)
    is_private = models.BooleanField()
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
