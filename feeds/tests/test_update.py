import pytest

from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects

from feeds.models import Feed


@pytest.mark.django_db
def test_update_feed(authenticated_client, feed):
    url = reverse('feeds:update', args=(feed.pk,))
    data = {'name': 'Updated name'}
    authenticated_client.post(url, data=data)

    updated_feed = Feed.objects.get(pk=feed.pk)
    assert updated_feed.name == data['name']


@pytest.mark.django_db
def test_update_feed_url_not_updated(authenticated_client, feed):
    url = reverse('feeds:update', args=(feed.pk,))
    data = {'name': 'Updated name', 'url': 'http://dummy-url.com'}
    authenticated_client.post(url, data=data)

    # Check url not changed
    updated_feed = Feed.objects.get(pk=feed.pk)

    assert updated_feed.name == data['name']
    assert updated_feed.url != data['url']


@pytest.mark.django_db
def test_update_feed_another_user(client, feed, second_user):
    feed_name = feed.name
    url = reverse('feeds:update', args=(feed.pk,))
    client.login(username=second_user.username, password='someUserPass12')
    data = {'name': 'Updated name'}
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 404
    possibly_updated_feed = Feed.objects.get(pk=feed.pk)
    assert possibly_updated_feed.name != feed_name


@pytest.mark.django_db
def test_create_feed_login_required(client, feed):
    url = reverse('feeds:update', args=(feed.pk,))
    data = {
        'name': 'Feed name',
    }
    response = client.post(url, data=data)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
