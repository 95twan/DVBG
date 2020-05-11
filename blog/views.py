import json
from django.views.generic import View
from django.http import JsonResponse

from blog.models import Post, Board, Comment, Blog
from blog.tasks import add_new_post_feed_task, removed_post_delete_feed_task

from user.jwt_auth import login_required


class BlogDetail(View):
    def get(self, request, pk):
        try:
            blog = Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            error_data = {
                "status": 404,
                "err_msg": "해당하는 아이디의 블로그가 없습니다."
            }
            return JsonResponse(error_data, status=404)

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

        Board.objects.create(**json_data)

        return JsonResponse(json_data, status=201)


class BoardDetail(View):
    def get(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
        except Board.DoesNotExist:
            error_data = {
                "status": 404,
                "err_msg": "해당하는 아이디의 보드가 없습니다."
            }
            return JsonResponse(error_data, status=404)

        board_json = board.json_serializer()
        return JsonResponse(board_json)

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
    def get(self, request):
        posts = Post.objects.all()
        post_json_list = [post.json_serializer() for post in posts]
        return JsonResponse(post_json_list, safe=False)

    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        images_str_data = json.dumps(json_data.get('images'))
        if images_str_data == "null":
            images_str_data = "[]"

        json_data['images'] = images_str_data

        post = Post.objects.create(**json_data)

        task_data = {
            "author_id": post.author_id,
            "post_id": post.id,
            "post_published_at": post.published_at
        }

        add_new_post_feed_task.apply_async(kwargs=task_data)

        return JsonResponse(json_data, status=201)


class PostDetail(View):
    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            error_data = {
                "status": 404,
                "err_msg": "해당하는 아이디의 포스트가 없습니다."
            }
            return JsonResponse(error_data, status=404)

        post_json = post.json_serializer()

        return JsonResponse(post_json)

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
    def get(self, request):
        comments = Comment.objects.all()
        comment_json_list = [comment.json_serializer() for comment in comments]
        return JsonResponse(comment_json_list, safe=False)

    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        Comment.objects.create(**json_data)

        return JsonResponse(json_data, status=201)


class CommentDetail(View):
    def get(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            error_data = {
                "status": 404,
                "err_msg": "해당하는 아이디의 코멘트가 없습니다."
            }
            return JsonResponse(error_data, status=404)

        comment_json = comment.json_serializer()

        return JsonResponse(comment_json)

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
    def get(self, request, user_id):
        blogs = Blog.objects.filter(user_id=user_id)
        blog_json_list = [blog.json_serializer() for blog in blogs]
        return JsonResponse(blog_json_list, safe=False)
