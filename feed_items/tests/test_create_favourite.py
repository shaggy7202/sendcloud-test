import pytest
from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects

from feed_items.models import Favourite


@pytest.mark.django_db
def test_create_favourite(authenticated_client, feed_item):
    url = reverse('feed_items:favourites_create')
    data = {'feed_item': feed_item.pk}
    authenticated_client.post(url, data)
    assert Favourite.objects.filter(feed_item=feed_item).exists()


@pytest.mark.django_db
def test_create_comment_another_user(client, feed_item, second_user):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feed_items:favourites_create')
    data = {'feed_item': feed_item.pk}
    response = client.post(url, data)
    assert response.status_code == 404
    assert not Favourite.objects.filter(feed_item=feed_item).exists()


@pytest.mark.django_db
def test_create_comment_login_required(client, feed_item):
    url = reverse('feed_items:favourites_create')
    data = {'feed_item': feed_item.pk}
    response = client.post(url, data=data)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
