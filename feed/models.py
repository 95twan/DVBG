from djongo import models


class Feed(models.Model):
    _id = models.ObjectIdField()
    article_type = models.CharField(max_length=255)
    author_id = models.IntegerField()
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    post_thumbnail_url = models.CharField(max_length=128)
    post_published_at = models.DateTimeField()

    class Meta:
        app_label = 'feed'
        db_table = 'feed'
