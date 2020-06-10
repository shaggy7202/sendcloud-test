import pytest
from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects

from feed_items.models import Comment


@pytest.mark.django_db
def test_create_comment(authenticated_client, feed_item):
    url = reverse('feed_items:create_comment')
    data = {
        'feed_item': feed_item.pk,
        'text': 'Comment text'
    }
    authenticated_client.post(url, data)
    created_comment = Comment.objects.get(feed_item=feed_item)
    assert created_comment.text == data['text']


@pytest.mark.django_db
def test_create_comment_another_user(client, feed_item, second_user):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feed_items:create_comment')
    data = {
        'feed_item': feed_item.pk,
        'text': 'Comment text'
    }
    response = client.post(url, data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_comment_login_required(client, feed_item):
    url = reverse('feed_items:create_comment')
    data = {
        'feed_item': feed_item.pk,
        'text': 'Comment text'
    }
    response = client.post(url, data=data)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
