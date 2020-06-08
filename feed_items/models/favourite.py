from django.db import models
from django.conf import settings


class Favourite(models.Model):
    feed_item = models.OneToOneField(
        'feed_items.FeedItem',
        on_delete=models.CASCADE,
        related_name='favourite'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favourite_articles'
    )
