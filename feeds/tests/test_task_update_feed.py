import pytest
import httpretty
from unittest.mock import patch
from django.core.cache import cache
from django.utils import timezone
from celery.exceptions import Retry

from feeds.tasks import task_update_feed
from feeds.models import Feed


@httpretty.activate
@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
def test_task(
    patched_add, patched_delete, feed, rss_feed_xml
):
    httpretty.register_uri(
        httpretty.GET, feed.url,
        body=rss_feed_xml,
    )
    task_update_feed(feed.pk)
    # Check feed items created from fixture
    assert feed.items.count() == 2
    patched_add.assert_called_once()
    patched_delete.assert_called_once()


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
@patch("celery.app.task.Task.request")
def test_task_disabled_after_max_retries(
    patched_task_request, patched_delete, patched_add, feed
):
    # Enable fetcher before test
    feed.fetcher.enabled = True
    feed.fetcher.save()
    patched_task_request.retries = 3

    task_update_feed(feed.pk)
    updated_feed = Feed.objects.get(pk=feed.pk)
    assert updated_feed.fetcher.enabled is False
    patched_add.assert_called_once()
    patched_delete.assert_called_once()


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=False)
@patch('feeds.tasks.update_feed.fetch_items')
def test_task_locked(patched_fetch_items, patched_add, feed):
    task_update_feed(feed.pk)
    patched_fetch_items.assert_not_called()


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
def test_task_disabled_user_inactive_week(
    patched_delete, patched_add, feed, user
):
    # Enable fetcher before test
    feed.fetcher.enabled = True
    feed.fetcher.save()

    week_ago = timezone.now() - timezone.timedelta(days=7)
    user.last_login = week_ago
    user.save()
    task_update_feed(feed.pk)
    updated_feed = Feed.objects.get(pk=feed.pk)
    assert updated_feed.fetcher.enabled is False

    patched_add.assert_called_once()
    patched_delete.assert_called_once()


@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
@patch('feeds.models.feed.Feed.fetch_items', return_value=[])
def test_task_retried(patched_add, patched_delete, patched_fetch, feed):
    with pytest.raises(Retry):
        task_update_feed(feed.pk)
    patched_add.assert_called_once()
    patched_delete.assert_called_once()
    patched_fetch.assrt_called_once()
