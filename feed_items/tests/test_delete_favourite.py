import pytest

from django.shortcuts import reverse
from feed_items.models import Favourite
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_delete_favourite(authenticated_client, favourite):
    url = reverse('feed_items:favourites_delete', kwargs={'pk': favourite.pk})
    authenticated_client.post(url)
    assert not Favourite.objects.filter(pk=favourite.pk).exists()


@pytest.mark.django_db
def test_delete_favourite_by_another_user(client, second_user, favourite):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feed_items:favourites_delete', kwargs={'pk': favourite.pk})
    response = client.post(url)
    assert response.status_code == 404
    assert Favourite.objects.filter(pk=favourite.pk).exists()


@pytest.mark.django_db
def test_delete_favourite_login_required(client, favourite):
    url = reverse('feed_items:favourites_delete', kwargs={'pk': favourite.pk})
    response = client.get(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
