import json

from django.test import RequestFactory
from django.urls import reverse

from funkwhale_api.users.models import User


def test_can_create_user_via_api(settings, client, db):
    url = reverse('rest_register')
    data = {
        'username': 'test1',
        'email': 'test1@test.com',
        'password1': 'testtest',
        'password2': 'testtest',
    }
    settings.REGISTRATION_MODE = "public"
    response = client.post(url, data)
    assert response.status_code == 201

    u = User.objects.get(email='test1@test.com')
    assert u.username == 'test1'


def test_can_disable_registration_view(settings, client, db):
    url = reverse('rest_register')
    data = {
        'username': 'test1',
        'email': 'test1@test.com',
        'password1': 'testtest',
        'password2': 'testtest',
    }
    settings.REGISTRATION_MODE = "disabled"
    response = client.post(url, data)
    assert response.status_code == 403


def test_can_fetch_data_from_api(client, factories):
    url = reverse('api:v1:users:users-me')
    response = client.get(url)
    # login required
    assert response.status_code == 401

    user = factories['users.User'](
        is_staff=True,
        perms=[
            'music.add_importbatch',
            'dynamic_preferences.change_globalpreferencemodel',
        ]
    )
    assert user.has_perm('music.add_importbatch')
    client.login(username=user.username, password='test')
    response = client.get(url)
    assert response.status_code == 200

    payload = json.loads(response.content.decode('utf-8'))

    assert payload['username'] == user.username
    assert payload['is_staff'] == user.is_staff
    assert payload['is_superuser'] == user.is_superuser
    assert payload['email'] == user.email
    assert payload['name'] == user.name
    assert payload['permissions']['import.launch']['status']
    assert payload['permissions']['settings.change']['status']