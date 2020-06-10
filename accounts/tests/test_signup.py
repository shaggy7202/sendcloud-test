import pytest

from django.shortcuts import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_signup(client):
    url = reverse('accounts:signup')
    data = {
        'username': 'test',
        'password1': 'secretMegaPass123',
        'password2': 'secretMegaPass123'
    }
    UserModel = get_user_model()
    client.post(url, data=data)
    assert UserModel.objects.filter(username=data['username']).exists()


@pytest.mark.django_db
def test_signup_passwords_not_match(client):
    url = reverse('accounts:signup')
    data = {
        'username': 'test',
        'password1': 'secretMegaPass123',
        'password2': 'secretMegaPass1234'
    }
    UserModel = get_user_model()

    response = client.post(url, data=data)
    assert 'password_mismatch' in response.context_data['form'].error_messages

    # Make sure no user created
    assert not UserModel.objects.filter(username=data['username']).exists()
