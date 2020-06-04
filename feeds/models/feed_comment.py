from django.db import models
from django.conf import settings


class FeedComment(models.Model):
    feed_item = models.ForeignKey(
        'feeds.FeedItem', on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Comment {self.pk} for "{self.feed_item.title}" article'
