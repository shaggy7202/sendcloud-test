import json

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from feedparser import parse


class Feed(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    fetcher = models.OneToOneField(
        PeriodicTask, on_delete=models.SET_NULL, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feeds'
    )

    class Meta:
        unique_together = ('created_by', 'url')
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('feeds:detail', kwargs={'pk': self.pk})

    def setup_fetcher(self):
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES
        )
        self.fetcher = PeriodicTask.objects.create(
            interval=schedule,
            name=f'Fetching feed items for Feed with pk {self.pk}',
            task='feeds.tasks.update_feed.task_update_feed',
            kwargs=json.dumps({'feed_pk': self.pk})
        )
        self.save()

    def disable_fetcher(self):
        self.fetcher.enabled = False
        self.fetcher.save()

    def enable_fetcher(self):
        self.fetcher.enabled = True
        self.fetcher.save()

    def fetch_items(self):
        result = parse(self.url)
        return result['entries']


@receiver(models.signals.pre_delete, sender=Feed)
def delete_fetcher(sender, instance, **kwargs):
    if instance.fetcher:
        instance.fetcher.delete()
