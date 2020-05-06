import json
from django.views.generic import View
from django.http import JsonResponse

from blog.models import Post, Board, Comment, Blog
from blog.tasks import feed_task

from user.jwt_auth import login_required


class BlogDetail(View):
    def serialize_data(self, pk):
        board = Blog.objects.filter(id=pk).values()[0]
        return board

    def get(self, request, pk):
        return JsonResponse(self.serialize_data(pk=pk))


class BoardList(View):
    def serialize_data(self):
        values = Board.objects.values()

        serialized_data = list(values)

        return serialized_data

    def get(self, request):
        return JsonResponse(self.serialize_data(), safe=False)

    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        Board.objects.create(name=json_data['name'], is_hidden=json_data['is_hidden'])

        return JsonResponse(json_data, status=201)


class BoardDetail(View):
    def serialize_data(self, pk):
        board = Board.objects.filter(id=pk).values()[0]
        return board

    def get(self, request, pk):
        return JsonResponse(self.serialize_data(pk=pk))

    @login_required
    def put(self, request, pk):
        json_data = json.loads(request.body)

        board = Board.objects.filter(id=pk)
        board.update(name=json_data['name'])

        return JsonResponse(json_data)

    @login_required
    def delete(self, request, pk):
        board = Board.objects.get(id=pk)
        board.post_set.update(is_hidden="True")
        board.delete()

        response_data = {
            "success": True
        }

        return JsonResponse(response_data)


class PostList(View):
    def serialize_data(self):
        values = Post.objects.values()

        serialized_data = list(values)

        return serialized_data

    def get(self, request):
        return JsonResponse(self.serialize_data(), safe=False)

    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        board_id = json_data['board_id']
        board = Board.objects.get(pk=board_id)

        post = Post.objects.create(
            board=board,
            title=json_data['title'],
            content=json_data['content'],
            tag=json_data['tag'],
            author_id=json_data['author_id'],
            is_hidden=json_data['is_hidden']
        )

        task_data = {
            "author_id": post.author_id,
            "post_id": post.id,
            "post_published_at": post.published_at
        }

        feed_task.apply_async(kwargs=task_data)

        return JsonResponse(json_data, status=201)


class PostDetail(View):
    def serialize_data(self, pk):
        post = Post.objects.filter(id=pk).values()[0]
        return post

    def get(self, request, pk):
        return JsonResponse(self.serialize_data(pk=pk))

    @login_required
    def put(self, request, pk):
        json_data = json.loads(request.body)

        board_id = json_data['board_id']
        board = Board.objects.get(pk=board_id)

        post = Post.objects.filter(id=pk)
        post.update(
            board=board,
            title=json_data['title'],
            content=json_data['content'],
            tag=json_data['tag'],
            author_id=json_data['author_id'],
            is_hidden=json_data['is_hidden']
        )

        # feed_task.apply_async()

        return JsonResponse(json_data)

    @login_required
    def delete(self, request, pk):
        post = Post.objects.filter(id=pk)
        post.delete()

        response_data = {
            "success": True
        }

        return JsonResponse(response_data)


class CommentList(View):
    def serialize_data(self):
        comments = Comment.objects.values()

        serialized_data = list(comments)

        return serialized_data

    def get(self, request):
        return JsonResponse(self.serialize_data(), status=200, safe=False)

    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        Comment.objects.create(**json_data)

        return JsonResponse(json_data, status=201)


class CommentDetail(View):
    def serialize_data(self, pk):
        comment = Comment.objects.filter(id=pk).values()[0]
        return comment

    def get(self, request, pk):
        return JsonResponse(self.serialize_data(pk=pk))

    @login_required
    def put(self, request, pk):
        json_data = json.loads(request.body)

        comment = Comment.objects.filter(id=pk)
        comment.update(**json_data)

        return JsonResponse(json_data)

    @login_required
    def delete(self, request, pk):
        comment = Comment.objects.filter(id=pk)
        comment.delete()

        response_data = {
            "delete": "Success"
        }

        return JsonResponse(response_data)


class UserBlog(View):
    def serialize_data(self, user_id):
        blogs = Blog.objects.filter(user_id=user_id).values()

        serialized_data = list(blogs)

        return serialized_data

    def get(self, request, user_id):
        return JsonResponse(self.serialize_data(user_id=user_id), safe=False)
