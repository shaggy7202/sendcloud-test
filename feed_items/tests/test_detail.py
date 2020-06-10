import pytest

from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects, assertContains

from feed_items.models import FeedItem


@pytest.mark.django_db
def test_detail_feed_item(authenticated_client, feed_item):
    url = reverse('feed_items:detail', kwargs={'pk': feed_item.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assertContains(response, feed_item.title)
    updated_feed_item = FeedItem.objects.get(pk=feed_item.pk)
    assert updated_feed_item.viewed


@pytest.mark.django_db
def test_detail_feed_by_another_user(client, second_user, feed_item):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feed_items:detail', kwargs={'pk': feed_item.pk})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_detail_feed_login_required(client, feed_item):
    url = reverse('feed_items:detail', kwargs={'pk': feed_item.pk})
    response = client.get(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
