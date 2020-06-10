import pytest

from django.shortcuts import reverse
from pytest_django.asserts import assertQuerysetEqual, assertRedirects


@pytest.mark.django_db
def test_feed_list(authenticated_client, feed):

    url = reverse('feeds:list')
    response = authenticated_client.get(url)
    assertQuerysetEqual(response.context_data['object_list'], [repr(feed)])


@pytest.mark.django_db
def test_feed_list_by_another_user(client, second_user, feed):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feeds:list')
    response = client.get(url)
    assert response.context_data['object_list'].count() == 0


@pytest.mark.django_db
def test_feed_list_login_required(client, feed):
    url = reverse('feeds:list')
    response = client.get(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
