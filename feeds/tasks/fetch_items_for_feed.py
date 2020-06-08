from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from django.core.cache import cache

from feeds.models import Feed


@shared_task(bind=True, max_retries=3, soft_time_limit=5)
def task_fetch_items_for_feed(self, feed_pk):
    """
    Task for fetching feed items. We need to be sure that only one instance
    of this task is running so we are implementing locking here.
    """
    lock_id = f'lock-for-feed-{feed_pk}'

    # cache.add return False if value already in the cache
    acquire_lock = cache.add(lock_id, "true", 10)  # Cache for 10 sec

    if acquire_lock:
        try:
            fetch_items(feed_pk=feed_pk, task=self)
        except SoftTimeLimitExceeded:
            if self.request.retries < self.max_retries:
                raise self.retry(countdown=30)
        finally:
            cache.delete(lock_id)


def fetch_items(feed_pk, task):
    feed = Feed.objects.get(pk=feed_pk)

    # Disable periodic task after maximum amount of retries is reached
    if task.request.retries >= task.max_retries:
        feed.fetcher.enabled = False
        return feed.fetcher.save()

    if items := feed.fetch_items():
        feed.items.save_items(feed, items)
    else:
        raise task.retry(countdown=30)  # Retry task in 30 seconds
