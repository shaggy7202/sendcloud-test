import pytest

from django.shortcuts import reverse
from pytest_django.asserts import assertQuerysetEqual, assertRedirects


@pytest.mark.django_db
def test_favourites_list(authenticated_client, favourite):

    url = reverse('feed_items:favourites_list')
    response = authenticated_client.get(url)
    assertQuerysetEqual(
        response.context_data['object_list'], [repr(favourite)]
    )


@pytest.mark.django_db
def test_favourites_list_by_another_user(client, second_user, favourite):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feed_items:favourites_list')
    response = client.get(url)
    assert response.context_data['object_list'].count() == 0


@pytest.mark.django_db
def test_favourites_list_login_required(client, favourite):
    url = reverse('feed_items:favourites_list')
    response = client.get(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
