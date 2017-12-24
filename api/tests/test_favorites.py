import json
import pytest
from django.urls import reverse

from funkwhale_api.music.models import Track, Artist
from funkwhale_api.favorites.models import TrackFavorite



def test_user_can_add_favorite(factories):
    track = factories['music.Track']()
    user = factories['users.User']()
    f = TrackFavorite.add(track, user)

    assert f.track == track
    assert f.user == user


def test_user_can_get_his_favorites(factories, logged_in_client, client):
    favorite = factories['favorites.TrackFavorite'](user=logged_in_client.user)
    url = reverse('api:v1:favorites:tracks-list')
    response = logged_in_client.get(url)

    expected = [
        {
            'track': favorite.track.pk,
            'id': favorite.id,
            'creation_date': favorite.creation_date.isoformat().replace('+00:00', 'Z'),
        }
    ]
    parsed_json = json.loads(response.content.decode('utf-8'))

    assert expected == parsed_json['results']


def test_user_can_add_favorite_via_api(factories, logged_in_client, client):
    track = factories['music.Track']()
    url = reverse('api:v1:favorites:tracks-list')
    response = logged_in_client.post(url, {'track': track.pk})

    favorite = TrackFavorite.objects.latest('id')
    expected = {
        'track': track.pk,
        'id': favorite.id,
        'creation_date': favorite.creation_date.isoformat().replace('+00:00', 'Z'),
    }
    parsed_json = json.loads(response.content.decode('utf-8'))

    assert expected == parsed_json
    assert favorite.track == track
    assert favorite.user == logged_in_client.user


def test_user_can_remove_favorite_via_api(logged_in_client, factories, client):
    favorite = factories['favorites.TrackFavorite'](user=logged_in_client.user)
    url = reverse('api:v1:favorites:tracks-detail', kwargs={'pk': favorite.pk})
    response = client.delete(url, {'track': favorite.track.pk})
    assert response.status_code == 204
    assert TrackFavorite.objects.count() == 0

def test_user_can_remove_favorite_via_api_using_track_id(factories, logged_in_client):
    favorite = factories['favorites.TrackFavorite'](user=logged_in_client.user)

    url = reverse('api:v1:favorites:tracks-remove')
    response = logged_in_client.delete(
        url, json.dumps({'track': favorite.track.pk}),
        content_type='application/json'
    )

    assert response.status_code == 204
    assert TrackFavorite.objects.count() == 0


@pytest.mark.parametrize('url,method', [
    ('api:v1:favorites:tracks-list', 'get'),
])
def test_url_require_auth(url, method, db, settings, client):
    settings.API_AUTHENTICATION_REQUIRED = True
    url = reverse(url)
    response = getattr(client, method)(url)
    assert response.status_code == 401


def test_can_filter_tracks_by_favorites(factories, logged_in_client):
    favorite = factories['favorites.TrackFavorite'](user=logged_in_client.user)

    url = reverse('api:v1:tracks-list')
    response = logged_in_client.get(url, data={'favorites': True})

    parsed_json = json.loads(response.content.decode('utf-8'))
    assert parsed_json['count'] == 1
    assert parsed_json['results'][0]['id'] == favorite.track.id