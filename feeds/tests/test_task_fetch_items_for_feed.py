import pytest
import httpretty
from unittest.mock import patch
from django.core.cache import cache
from celery.exceptions import (MaxRetriesExceededError, Retry)

from feeds.tasks import task_fetch_items_for_feed
from feeds.models import Feed


@httpretty.activate
@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
def test_task(patched_add, patched_delete, feed, rss_feed_xml):
    httpretty.register_uri(
        httpretty.GET, feed.url,
        body=rss_feed_xml,
    )
    task_fetch_items_for_feed(feed.pk)
    assert feed.items.count() == 2


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
@patch(
    'feeds.tasks.fetch_items_for_feed.fetch_items',
    side_effect=MaxRetriesExceededError()
)
def test_task_disabled_after_max_retries(
    patched_add, patched_delete, patched_fetch, feed
):
    # Enable fetcher before test
    feed.fetcher.enabled = True
    feed.fetcher.save()
    task_fetch_items_for_feed(feed.pk)
    updated_feed = Feed.objects.get(pk=feed.pk)
    patched_fetch.assert_called_once()
    patched_delete.assert_called_once()
    assert updated_feed.fetcher.enabled is False


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=False)
@patch('feeds.tasks.fetch_items_for_feed.fetch_items')
def test_task_locked(patched_fetch_items, patched_add, feed):
    task_fetch_items_for_feed(feed.pk)
    patched_fetch_items.assert_not_called()


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
@patch('feeds.models.feed.Feed.fetch_items', return_value=[])
def test_task_retried(patched_add, patched_delete, patched_fetch, feed):
    with pytest.raises(Retry):
        task_fetch_items_for_feed(feed.pk)
