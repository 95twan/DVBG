import json

from django.db import models
from user.models import User


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'blog'

    def json_serializer(self):
        # allow Null인거는 체크햐야 함
        return {
            "id": self.id,
            "user_id": self.user.id,
            "name": self.name
        }


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blog, models.CASCADE)
    name = models.CharField(max_length=45)
    is_hidden = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'board'

    def json_serializer(self):
        # allow Null인거는 체크햐야 함
        return {
            "id": self.id,
            "blog_id": self.blog.id,
            "name": self.name,
            "is_hidden": self.is_hidden,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at
        }


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=45)
    content = models.TextField()
    images = models.TextField()
    tag = models.CharField(max_length=45, blank=True, null=True)
    author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    is_hidden = models.BooleanField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post'

    def json_serializer(self):

        image_data = json.loads(self.images)

        # allow Null인거는 체크햐야 함
        return {
            "id": self.id,
            "board_id": self.board.id,
            "title": self.title,
            "content": self.content,
            "images": image_data,
            "tag": self.tag,
            "author_id": self.author.id,
            "is_hidden": self.is_hidden,
            "published_at": self.published_at
        }


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

    def json_serializer(self):

        # allow Null인거는 체크햐야 함
        return {
            "id": self.id,
            "post_id": self.post.id,
            "user_id": self.user.id,
            "reply_id": self.reply.id,
            "content": self.content,
            "is_private": self.is_private,
            "registered_at": self.registered_at
        }
