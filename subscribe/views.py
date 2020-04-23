import json

from django.views.generic import View
from django.http.response import JsonResponse

from user.models import User
from user.jwt_auth import login_required
from blog.models import Blog
from subscribe.models import Subscribe


class SubscribeAuthor(View):
    @login_required
    def post(self, request):
        # 이미 구독 한 유저랑 나 자신은 구독 안되게 해야됨
        json_data = json.loads(request.body)

        user_id = json_data['user_id']
        author_id = json_data['author_id']

        user = User.objects.get(pk=user_id)
        blogs = Blog.objects.select_related('user').filter(user_id=author_id)

        Subscribe.objects.create(user=user, author_id=author_id)

        for blog in blogs:
            Subscribe.objects.create(user=user, blog=blog)

        return JsonResponse({"success": True})

    @login_required
    def delete(self, request):
        json_data = json.load(request.body)

        user_id = json_data['user_id']
        author_id = json_data['author_id']

        user = User.objects.get(pk=user_id)
        author = User.objects.get(pk=author_id)

        blogs = author.blog_set.all()

        for blog in blogs:
            subscribe = Subscribe.objects.filter(user=user, blog=blog)
            subscribe.delete()

        subscribe = Subscribe.objects.get(user=user, author=author)
        subscribe.delete()

        return JsonResponse({"success": True})


class SubscribeBlog(View):
    @login_required
    def post(self, request):
        json_data = json.loads(request.body)

        user_id = json_data['user_id']
        blog_id = json_data['blog_id']

        user = User.objects.get(pk=user_id)
        blog = Blog.objects.get(pk=blog_id)

        Subscribe.objects.create(user=user, blog=blog)

        return JsonResponse({"success": True})

    @login_required
    def delete(self, request):
        json_data = json.load(request.body)

        user_id = json_data['user_id']
        blog_id = json_data['blog_id']

        user = User.objects.get(pk=user_id)
        blog = Blog.objects.get(pk=blog_id)

        subscribe = Subscribe.objects.filter(user=user, blog=blog)
        subscribe.delete()

        return JsonResponse({"success": True})
