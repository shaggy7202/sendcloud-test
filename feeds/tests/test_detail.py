import pytest

from django.shortcuts import reverse
from pytest_django.asserts import assertRedirects, assertContains


@pytest.mark.django_db
def test_detail_feed(authenticated_client, feed):
    url = reverse('feeds:detail', kwargs={'pk': feed.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assertContains(response, feed.name)


@pytest.mark.django_db
def test_detail_feed_by_another_user(client, second_user, feed):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feeds:detail', kwargs={'pk': feed.pk})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_detail_feed_login_required(client, feed):
    url = reverse('feeds:detail', kwargs={'pk': feed.pk})
    response = client.get(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
