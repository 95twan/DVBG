from __future__ import absolute_import, unicode_literals
from celery import shared_task

from blog.models import Post
from subscribe.models import Subscribe
from feed.models import Feed


@shared_task
def add_new_post_feed_task(author_id, post_id, post_published_at):

    # post_id로 블로그 찾고 해당 블로그를 구독 하는 유저 찾기
    value = Post.objects.filter(pk=post_id).select_related('board').values('board__blog_id')[0]

    subscribers = Subscribe.objects.filter(blog_id=value["board__blog_id"])

    for subscriber in subscribers:
        feed_data = {
            "article_type": "ARTICLE_POST",
            "user_id": subscriber.user.id,
            "author_id": author_id,
            "post_id": post_id,
            "post_thumbnail_url": "http://~",
            "post_published_at": post_published_at
        }
        # ㅂㅓㄹ크 크리레이트
        Feed.objects.create(**feed_data)

    return "Success"


@shared_task
def removed_post_delete_feed_task(post_id):

    Feed.objects.filter(post_id=post_id).delete()

    return "Success"
