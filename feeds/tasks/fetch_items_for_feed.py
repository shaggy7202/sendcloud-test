from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded, MaxRetriesExceededError

from django.core.cache import cache

from feeds.models import Feed

# Retry task in 30 seconds
COUNTDOWN = 30


@shared_task(bind=True, max_retries=3, soft_time_limit=5)
def task_fetch_items_for_feed(self, feed_pk):
    """
    Task for fetching feed items. We need to be sure that only one instance
    of this task is running so we are implementing locking here.
    """
    lock_id = f'lock-for-feed-{feed_pk}'

    # cache.add return False if value already in the cache
    acquire_lock = cache.add(lock_id, "true", 5)  # Cache for 5 sec

    if acquire_lock:
        feed = Feed.objects.get(pk=feed_pk)
        try:
            fetch_items(feed=feed, task=self)
        except SoftTimeLimitExceeded:
            if self.request.retries < self.max_retries:
                raise self.retry(countdown=COUNTDOWN)
        except MaxRetriesExceededError:
            feed.fetcher.enabled = False
            feed.fetcher.save()
        finally:
            cache.delete(lock_id)


def fetch_items(feed, task):
    if items := feed.fetch_items():
        return feed.items.save_items(feed, items)
    raise task.retry(countdown=COUNTDOWN)

