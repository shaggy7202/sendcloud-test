import httpretty
import pytest

from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects

from feeds.models import Feed


@pytest.mark.django_db
@httpretty.activate
def test_create_feed(authenticated_client, rss_feed_xml):
    httpretty.register_uri(
        httpretty.GET, 'http://dummysite.com',
        body=rss_feed_xml,
    )
    url = reverse('feeds:create')
    data = {
        'name': 'Feed name',
        'url': 'http://dummysite.com'
    }
    authenticated_client.post(url, data=data)

    created_feed = Feed.objects.get(name=data['name'])
    assert created_feed.url == data['url']

    # Check fetcher enabled and created
    assert created_feed.fetcher.enabled

    # check feed items created
    assert created_feed.items.count() == 2


@pytest.mark.django_db
def test_create_feed_same_url(authenticated_client, feed):
    url = reverse('feeds:create')
    data = {
        'name': 'Feed',
        'url': feed.url
    }
    response = authenticated_client.post(url, data=data)

    # Check we still have 1 feed for this url
    assert Feed.objects.filter(url=feed.url).count() == 1

    form_errors = response.context_data['form'].errors
    assert form_errors['url'][0] == 'You already have feed for this url'


@pytest.mark.django_db
@httpretty.activate
def test_create_feed_invalid_url(authenticated_client):
    # Returned result isn't valid XML, so form should be invalid
    httpretty.register_uri(
        httpretty.GET, 'http://dummysite.com',
        body='{"results": "some results here"}',
    )
    url = reverse('feeds:create')
    data = {
        'name': 'Feed name',
        'url': 'http://dummysite.com'
    }
    response = authenticated_client.post(url, data=data)
    form_errors = response.context_data['form'].errors
    assert form_errors['url'][0] == 'Unable to process given RSS feed url'


@pytest.mark.django_db
def test_create_feed_login_required(client):
    url = reverse('feeds:create')
    data = {
        'name': 'Feed name',
        'url': 'http://dummysite.com'
    }
    response = client.post(url, data=data)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
