import pytest

from django.shortcuts import reverse
from feed_items.models import Comment
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_delete_comment(authenticated_client, comment):
    url = reverse('feed_items:delete_comment', kwargs={'pk': comment.pk})
    authenticated_client.post(url)
    assert not Comment.objects.filter(pk=comment.pk).exists()


@pytest.mark.django_db
def test_delete_comment_by_another_user(client, second_user, comment):
    client.login(username=second_user.username, password='someUserPass12')
    url = reverse('feed_items:delete_comment', kwargs={'pk': comment.pk})
    response = client.post(url)
    assert response.status_code == 404
    assert Comment.objects.filter(pk=comment.pk).exists()


@pytest.mark.django_db
def test_delete_comment_login_required(client, comment):
    url = reverse('feed_items:delete_comment', kwargs={'pk': comment.pk})
    response = client.post(url)
    expected_redirect_url = f'{reverse("accounts:login")}?next={url}'
    assertRedirects(response, expected_redirect_url)
