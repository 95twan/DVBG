import json
from django.views.generic import View
from django.http import JsonResponse

from feed.models import Feed


class FeedView(View):
    def serialize_data(self):
        values = Feed.objects.values(
            'article_type',
            'author_id',
            'user_id',
            'post_id',
            'post_thumbnail_url',
            'post_published_at'
        )

        serialized_data = list(values)

        return serialized_data

    def get(self, request):
        return JsonResponse(self.serialize_data(), safe=False)

    def post(self, request):
        json_data = json.loads(request.body)

        Feed.objects.create(**json_data)

        return JsonResponse(json_data, status=201)


class FeedDetailView(View):
    def serialize_data(self, user_id):
        values = Feed.objects.filter(user_id=user_id).values(
            'article_type',
            'author_id',
            'user_id',
            'post_id',
            'post_thumbnail_url',
            'post_published_at'
        )

        serialized_data = list(values)

        return serialized_data

    def get(self, request, user_id):
        return JsonResponse(self.serialize_data(user_id=user_id), safe=False)





