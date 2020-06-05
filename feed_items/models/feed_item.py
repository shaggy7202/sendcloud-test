from django.db import models
from dateutil import parser


class FeedItemManager(models.Manager):
    def save_items(self, feed, items):
        saved_items = set(
            self.filter(feed=feed).values_list('guid', flat=True)
        )
        result_items = []
        for item in items:
            if item.id in saved_items:
                # Item already saved
                continue
            result_items.append(self.model(
                title=item.title,
                link=item.link,
                guid=item.id,
                publication_date=parser.parse(item.published),
                description=item.summary,
                feed=feed
            ))
        if result_items:
            # Save all items by one query
            self.bulk_create(result_items)


class FeedItem(models.Model):
    feed = models.ForeignKey(
        'feeds.Feed', on_delete=models.CASCADE, related_name='items'
    )
    guid = models.CharField(max_length=255)
    title = models.TextField()
    description = models.TextField()
    publication_date = models.DateTimeField()
    link = models.URLField()
    viewed = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)

    objects = FeedItemManager()

    class Meta:
        unique_together = ('feed', 'guid')
        ordering = ['-publication_date']

    def __str__(self):
        return self.title
