from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from feedparser import parse

from feeds.models import Feed


@shared_task(bind=True, max_retries=5, soft_time_limit=10)
def task_fetch_items_for_feed(self, feed_pk):
    feed = Feed.objects.get(pk=feed_pk)

    try:
        result = parse(feed.url)
    except SoftTimeLimitExceeded:
        items = []
    else:
        items = result['entries']

    if items:
        return feed.items.save_items(feed, items)

    if self.request.retries >= self.max_retries:
        # Disable periodic task
        feed.fetcher.enabled = False
        feed.fetcher.save()
        return
    raise self.retry(countdown=30)
