from __future__ import absolute_import, unicode_literals
from celery import shared_task

from blog.models import Post
from feed.models import Feed


@shared_task
def subscribe_author_add_feed_task(user_id, author_id):

    posts = Post.objects.filter(board__blog__user_id=author_id).order_by('-published_at')[:10]

    for post in posts:
        feed_data = {
            "article_type": "ARTICLE_POST",
            "user_id": user_id,
            "author_id": author_id,
            "post_id": post.id,
            "post_thumbnail_url": "http://~",
            "post_published_at": post.published_at
        }
        # 벌크 크리레이트
        Feed.objects.create(**feed_data)

    return "Success"
