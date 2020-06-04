from django.db import models
from django.conf import settings


class FeedItem(models.Model):
    feed = models.ForeignKey(
        'feeds.Feed', on_delete=models.CASCADE, related_name='items'
    )
    guid = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    description = models.TextField()
    publication_date = models.DateTimeField()
    link = models.URLField()
    favourite = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='favourite'
    )

    def __str__(self):
        return self.title
