import httpretty
import pytest
from django.core.cache import cache
from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects
from unittest.mock import patch

from feeds.models import Feed


@httpretty.activate
@pytest.mark.django_db
@patch.object(cache, 'add', return_value=True)
@patch.object(cache, 'delete', return_value=True)
def test_fetch_items(
    patched_add, patched_delete, feed, rss_feed_xml, authenticated_client
):
    url = reverse('feeds:fetch_items', kwargs={'pk': feed.pk})
    httpretty.register_uri(
        httpretty.GET, feed.url,
        body=rss_feed_xml,
    )
    authenticated_client.get(url)
    updated_feed = Feed.objects.get(pk=feed.pk)
    assert updated_feed.items.count() == 2
    assert updated_feed.fetcher.enabled

    patched_add.assert_called_once()
    patched_delete.assert_called_once()


@pytest.mark.django_db
def test_fetch_items_by_another_user(second_user, feed, client):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feeds:fetch_items', kwargs={'pk': feed.pk})
    response = client.get(url)

    assert response.status_code == 404
    feed.refresh_from_db()
    assert feed.items.count() == 0


@pytest.mark.django_db
def test_fetch_items_login_required(client, feed):
    url = reverse('feeds:fetch_items', kwargs={'pk': feed.pk})
    response = client.get(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
