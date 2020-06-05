from django.db import models


class FeedItemComment(models.Model):
    feed_item = models.ForeignKey(
        'feed_items.FeedItem',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()

    def __str__(self):
        return f'Comment {self.pk} for "{self.feed_item.title}" article'
