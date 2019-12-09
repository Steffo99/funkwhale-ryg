import pytest
from django.core.paginator import Paginator
from django.urls import reverse

from funkwhale_api.federation import actors, serializers, webfinger


def test_authenticate_skips_anonymous_fetch_when_allow_list_enabled(
    preferences, api_client
):
    preferences["moderation__allow_list_enabled"] = True
    actor = actors.get_service_actor()
    url = reverse(
        "federation:actors-detail",
        kwargs={"preferred_username": actor.preferred_username},
    )
    response = api_client.get(url)

    assert response.status_code == 403


def test_wellknown_webfinger_validates_resource(db, api_client, settings, mocker):
    clean = mocker.spy(webfinger, "clean_resource")
    url = reverse("federation:well-known-webfinger")
    response = api_client.get(url, data={"resource": "something"})

    clean.assert_called_once_with("something")
    assert url == "/.well-known/webfinger"
    assert response.status_code == 400
    assert response.data["errors"]["resource"] == ("Missing webfinger resource type")


def test_wellknown_nodeinfo(db, preferences, api_client, settings):
    expected = {
        "links": [
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": "{}{}".format(
                    settings.FUNKWHALE_URL, reverse("api:v1:instance:nodeinfo-2.0")
                ),
            }
        ]
    }
    url = reverse("federation:well-known-nodeinfo")
    response = api_client.get(url, HTTP_ACCEPT="application/jrd+json")
    assert response.status_code == 200
    assert response["Content-Type"] == "application/jrd+json"
    assert response.data == expected


def test_wellknown_nodeinfo_disabled(db, preferences, api_client):
    preferences["instance__nodeinfo_enabled"] = False
    url = reverse("federation:well-known-nodeinfo")
    response = api_client.get(url)
    assert response.status_code == 404


def test_local_actor_detail(factories, api_client):
    user = factories["users.User"](with_actor=True)
    url = reverse(
        "federation:actors-detail",
        kwargs={"preferred_username": user.actor.preferred_username},
    )
    serializer = serializers.ActorSerializer(user.actor)
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == serializer.data


def test_service_actor_detail(factories, api_client):
    actor = actors.get_service_actor()
    url = reverse(
        "federation:actors-detail",
        kwargs={"preferred_username": actor.preferred_username},
    )
    serializer = serializers.ActorSerializer(actor)
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == serializer.data


def test_local_actor_inbox_post_requires_auth(factories, api_client):
    user = factories["users.User"](with_actor=True)
    url = reverse(
        "federation:actors-inbox",
        kwargs={"preferred_username": user.actor.preferred_username},
    )
    response = api_client.post(url, {"hello": "world"})

    assert response.status_code == 403


def test_local_actor_inbox_post(factories, api_client, mocker, authenticated_actor):
    patched_receive = mocker.patch("funkwhale_api.federation.activity.receive")
    user = factories["users.User"](with_actor=True)
    url = reverse(
        "federation:actors-inbox",
        kwargs={"preferred_username": user.actor.preferred_username},
    )
    response = api_client.post(url, {"hello": "world"}, format="json")

    assert response.status_code == 200
    patched_receive.assert_called_once_with(
        activity={"hello": "world"},
        on_behalf_of=authenticated_actor,
        inbox_actor=user.actor,
    )


def test_local_actor_inbox_post_receive(
    factories, api_client, mocker, authenticated_actor
):
    payload = {
        "to": [
            "https://test.server/federation/music/libraries/956af6c9-1eb9-4117-8d17-b15e7b34afeb/followers"
        ],
        "type": "Create",
        "actor": authenticated_actor.fid,
        "object": {
            "id": "https://test.server/federation/music/uploads/fe564a47-b1d4-4596-bf96-008ccf407672",
            "type": "Audio",
        },
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
            {},
        ],
    }
    user = factories["users.User"](with_actor=True)
    url = reverse(
        "federation:actors-inbox",
        kwargs={"preferred_username": user.actor.preferred_username},
    )
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 200


def test_shared_inbox_post(factories, api_client, mocker, authenticated_actor):
    patched_receive = mocker.patch("funkwhale_api.federation.activity.receive")
    url = reverse("federation:shared-inbox")
    response = api_client.post(url, {"hello": "world"}, format="json")

    assert response.status_code == 200
    patched_receive.assert_called_once_with(
        activity={"hello": "world"}, on_behalf_of=authenticated_actor
    )


def test_wellknown_webfinger_local(factories, api_client, settings, mocker):
    user = factories["users.User"](with_actor=True)
    url = reverse("federation:well-known-webfinger")
    response = api_client.get(
        url,
        data={"resource": "acct:{}".format(user.actor.webfinger_subject)},
        HTTP_ACCEPT="application/jrd+json",
    )
    serializer = serializers.ActorWebfingerSerializer(user.actor)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/jrd+json"
    assert response.data == serializer.data


@pytest.mark.parametrize("privacy_level", ["me", "instance", "everyone"])
def test_music_library_retrieve(factories, api_client, privacy_level):
    library = factories["music.Library"](privacy_level=privacy_level)
    expected = serializers.LibrarySerializer(library).data

    url = reverse("federation:music:libraries-detail", kwargs={"uuid": library.uuid})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == expected


def test_music_library_retrieve_page_public(factories, api_client):
    library = factories["music.Library"](privacy_level="everyone")
    upload = factories["music.Upload"](library=library, import_status="finished")
    id = library.get_federation_id()
    expected = serializers.CollectionPageSerializer(
        {
            "id": id,
            "item_serializer": serializers.UploadSerializer,
            "actor": library.actor,
            "page": Paginator([upload], 1).page(1),
            "name": library.name,
            "summary": library.description,
        }
    ).data

    url = reverse("federation:music:libraries-detail", kwargs={"uuid": library.uuid})
    response = api_client.get(url, {"page": 1})

    assert response.status_code == 200
    assert response.data == expected


def test_channel_outbox_retrieve(factories, api_client):
    channel = factories["audio.Channel"](actor__local=True)
    expected = serializers.ChannelOutboxSerializer(channel).data

    url = reverse(
        "federation:actors-outbox",
        kwargs={"preferred_username": channel.actor.preferred_username},
    )
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == expected


def test_channel_outbox_retrieve_page(factories, api_client):
    channel = factories["audio.Channel"](actor__local=True)
    upload = factories["music.Upload"](library=channel.library, playable=True)
    url = reverse(
        "federation:actors-outbox",
        kwargs={"preferred_username": channel.actor.preferred_username},
    )

    expected = serializers.CollectionPageSerializer(
        {
            "id": channel.actor.outbox_url,
            "item_serializer": serializers.ChannelCreateUploadSerializer,
            "actor": channel.actor,
            "page": Paginator([upload], 1).page(1),
        }
    ).data

    response = api_client.get(url, {"page": 1})

    assert response.status_code == 200
    assert response.data == expected


def test_channel_upload_retrieve(factories, api_client):
    channel = factories["audio.Channel"](local=True)
    upload = factories["music.Upload"](library=channel.library, playable=True)
    url = reverse("federation:music:uploads-detail", kwargs={"uuid": upload.uuid},)

    expected = serializers.ChannelUploadSerializer(upload).data

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.parametrize("privacy_level", ["me", "instance"])
def test_music_library_retrieve_page_private(factories, api_client, privacy_level):
    library = factories["music.Library"](privacy_level=privacy_level)
    url = reverse("federation:music:libraries-detail", kwargs={"uuid": library.uuid})
    response = api_client.get(url, {"page": 1})

    assert response.status_code == 403


@pytest.mark.parametrize("approved,expected", [(True, 200), (False, 403)])
def test_music_library_retrieve_page_follow(
    factories, api_client, authenticated_actor, approved, expected
):
    library = factories["music.Library"](privacy_level="me")
    factories["federation.LibraryFollow"](
        actor=authenticated_actor, target=library, approved=approved
    )
    url = reverse("federation:music:libraries-detail", kwargs={"uuid": library.uuid})
    response = api_client.get(url, {"page": 1})

    assert response.status_code == expected


@pytest.mark.parametrize(
    "factory, serializer_class, namespace",
    [
        ("music.Artist", serializers.ArtistSerializer, "artists"),
        ("music.Album", serializers.AlbumSerializer, "albums"),
        ("music.Track", serializers.TrackSerializer, "tracks"),
    ],
)
def test_music_local_entity_detail(
    factories, api_client, factory, serializer_class, namespace, settings
):
    obj = factories[factory](fid="http://{}/1".format(settings.FEDERATION_HOSTNAME))
    url = reverse(
        "federation:music:{}-detail".format(namespace), kwargs={"uuid": obj.uuid}
    )
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == serializer_class(obj).data


@pytest.mark.parametrize(
    "factory, namespace",
    [("music.Artist", "artists"), ("music.Album", "albums"), ("music.Track", "tracks")],
)
def test_music_non_local_entity_detail(
    factories, api_client, factory, namespace, settings
):
    obj = factories[factory](fid="http://wrong-domain/1")
    url = reverse(
        "federation:music:{}-detail".format(namespace), kwargs={"uuid": obj.uuid}
    )
    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.parametrize(
    "privacy_level, expected", [("me", 404), ("instance", 404), ("everyone", 200)]
)
def test_music_upload_detail(factories, api_client, privacy_level, expected):
    upload = factories["music.Upload"](
        library__privacy_level=privacy_level,
        library__actor__local=True,
        import_status="finished",
    )
    url = reverse("federation:music:uploads-detail", kwargs={"uuid": upload.uuid})
    response = api_client.get(url)

    assert response.status_code == expected
    if expected == 200:
        assert response.data == serializers.UploadSerializer(upload).data


@pytest.mark.parametrize("privacy_level", ["me", "instance"])
def test_music_upload_detail_private_approved_follow(
    factories, api_client, authenticated_actor, privacy_level
):
    upload = factories["music.Upload"](
        library__privacy_level=privacy_level,
        library__actor__local=True,
        import_status="finished",
    )
    factories["federation.LibraryFollow"](
        actor=authenticated_actor, target=upload.library, approved=True
    )
    url = reverse("federation:music:uploads-detail", kwargs={"uuid": upload.uuid})
    response = api_client.get(url)

    assert response.status_code == 200
