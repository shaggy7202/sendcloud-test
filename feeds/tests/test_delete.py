import pytest

from django.shortcuts import reverse
from feeds.models import Feed
from django_celery_beat.models import PeriodicTask
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_delete_feed(authenticated_client, feed):
    fetcher = feed.fetcher
    url = reverse('feeds:delete', kwargs={'pk': feed.pk})
    authenticated_client.post(url)

    # Make sure task also deleted
    assert not PeriodicTask.objects.filter(pk=fetcher.pk).exists()
    assert not Feed.objects.filter(pk=feed.pk).exists()


@pytest.mark.django_db
def test_delete_feed_by_another_user(client, second_user, feed):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feeds:delete', kwargs={'pk': feed.pk})
    response = client.post(url)
    assert response.status_code == 404
    assert Feed.objects.filter(pk=feed.pk).exists()


def test_delete_feed_login_required(client, feed):
    url = reverse('feeds:delete', kwargs={'pk': feed.pk})
    response = client.post(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
