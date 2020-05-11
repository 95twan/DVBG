import json
from django.views.generic import View
from django.http import JsonResponse

from blog.models import Post, Board, Comment, Blog
from blog.tasks import add_new_post_feed_task, removed_post_delete_feed_task

from user.jwt_auth import login_required


class BlogDetail(View):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        blog_json = blog.json_serializer()
        return JsonResponse(blog_json)


class BoardList(View):
    def get(self, request):
        boards = Board.objects.all()
        boards_json_list = [board.json_serializer() for board in boards]
        return JsonResponse(boards_json_list, safe=False)

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

        for data in serialized_data:
            data["images"] = json.loads(data["images"])

        return serialized_data

    def get(self, request):
        return JsonResponse(self.serialize_data(), safe=False)

    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        board_id = json_data['board_id']
        board = Board.objects.get(pk=board_id)

        images_str_data = json.dumps(json_data.get('images'))
        if images_str_data == "null":
            images_str_data = "[]"

        post = Post.objects.create(
            board=board,
            title=json_data['title'],
            content=json_data['content'],
            images=images_str_data,
            tag=json_data['tag'],
            author_id=json_data['author_id'],
            is_hidden=json_data['is_hidden']
        )

        task_data = {
            "author_id": post.author_id,
            "post_id": post.id,
            "post_published_at": post.published_at
        }

        add_new_post_feed_task.apply_async(kwargs=task_data)

        return JsonResponse(json_data, status=201)


class PostDetail(View):
    def serialize_data(self, pk):
        post = Post.objects.filter(id=pk).values()[0]

        post["images"] = json.loads(post["images"])

        return post

    def get(self, request, pk):
        return JsonResponse(self.serialize_data(pk=pk))

    @login_required
    def put(self, request, pk):
        json_data = json.loads(request.body)

        board_id = json_data['board_id']
        board = Board.objects.get(pk=board_id)

        images_str_data = json.dumps(json_data.get('images'))
        if images_str_data == 'null':
            images_str_data = '[]'

        post = Post.objects.filter(id=pk)
        post.update(
            board=board,
            title=json_data['title'],
            content=json_data['content'],
            images=images_str_data,
            tag=json_data['tag'],
            author_id=json_data['author_id'],
            is_hidden=json_data['is_hidden']
        )

        # add_new_post_feed_task.apply_async()

        return JsonResponse(json_data)

    @login_required
    def delete(self, request, pk):
        post = Post.objects.filter(id=pk)
        post.delete()

        removed_post_delete_feed_task.apply_async((pk, ))

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
