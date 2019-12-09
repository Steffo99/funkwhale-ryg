import pytest

from funkwhale_api.federation import api_serializers
from funkwhale_api.federation import serializers


def test_library_serializer(factories, to_api_date):
    library = factories["music.Library"](uploads_count=5678)
    expected = {
        "fid": library.fid,
        "uuid": str(library.uuid),
        "actor": serializers.APIActorSerializer(library.actor).data,
        "name": library.name,
        "description": library.description,
        "creation_date": to_api_date(library.creation_date),
        "uploads_count": library.uploads_count,
        "privacy_level": library.privacy_level,
        "follow": None,
        "latest_scan": None,
    }

    serializer = api_serializers.LibrarySerializer(library)

    assert serializer.data == expected


def test_library_serializer_latest_scan(factories):
    library = factories["music.Library"](uploads_count=5678)
    scan = factories["music.LibraryScan"](library=library)
    setattr(library, "latest_scans", [scan])
    expected = api_serializers.LibraryScanSerializer(scan).data
    serializer = api_serializers.LibrarySerializer(library)

    assert serializer.data["latest_scan"] == expected


def test_library_serializer_with_follow(factories, to_api_date):
    library = factories["music.Library"](uploads_count=5678)
    follow = factories["federation.LibraryFollow"](target=library)

    setattr(library, "_follows", [follow])
    expected = {
        "fid": library.fid,
        "uuid": str(library.uuid),
        "actor": serializers.APIActorSerializer(library.actor).data,
        "name": library.name,
        "description": library.description,
        "creation_date": to_api_date(library.creation_date),
        "uploads_count": library.uploads_count,
        "privacy_level": library.privacy_level,
        "follow": api_serializers.NestedLibraryFollowSerializer(follow).data,
        "latest_scan": None,
    }

    serializer = api_serializers.LibrarySerializer(library)

    assert serializer.data == expected


def test_library_follow_serializer_validates_existing_follow(factories):
    follow = factories["federation.LibraryFollow"]()
    serializer = api_serializers.LibraryFollowSerializer(
        data={"target": follow.target.uuid}, context={"actor": follow.actor}
    )

    assert serializer.is_valid() is False
    assert "target" in serializer.errors


def test_library_follow_serializer_do_not_allow_own_library(factories):
    actor = factories["federation.Actor"]()
    library = factories["music.Library"](actor=actor)
    serializer = api_serializers.LibraryFollowSerializer(context={"actor": actor})

    with pytest.raises(
        api_serializers.serializers.ValidationError, match=r".*own library.*"
    ):
        serializer.validate_target(library)


def test_manage_upload_action_read(factories):
    ii = factories["federation.InboxItem"]()
    s = api_serializers.InboxItemActionSerializer(queryset=None)

    s.handle_read(ii.__class__.objects.all())

    assert ii.__class__.objects.filter(is_read=False).count() == 0


@pytest.mark.parametrize(
    "factory_name, factory_kwargs, expected",
    [
        (
            "federation.Actor",
            {"preferred_username": "hello", "domain__name": "world"},
            {"full_username": "hello@world"},
        ),
        (
            "music.Library",
            {"name": "hello", "uuid": "ad1ee1f7-589c-4abe-b303-e4fe7a889260"},
            {"uuid": "ad1ee1f7-589c-4abe-b303-e4fe7a889260", "name": "hello"},
        ),
        (
            "federation.LibraryFollow",
            {"approved": False, "uuid": "ad1ee1f7-589c-4abe-b303-e4fe7a889260"},
            {"uuid": "ad1ee1f7-589c-4abe-b303-e4fe7a889260", "approved": False},
        ),
    ],
)
def test_serialize_generic_relation(factory_name, factory_kwargs, expected, factories):
    obj = factories[factory_name](**factory_kwargs)
    expected["type"] = factory_name
    assert api_serializers.serialize_generic_relation({}, obj) == expected
