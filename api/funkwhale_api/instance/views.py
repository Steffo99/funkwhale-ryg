from rest_framework import views
from rest_framework.response import Response

from dynamic_preferences.api import serializers
from dynamic_preferences.registries import global_preferences_registry

from funkwhale_api.common import preferences

from . import nodeinfo
from . import stats


NODEINFO_2_CONTENT_TYPE = (
    'application/json; profile=http://nodeinfo.diaspora.software/ns/schema/2.0#; charset=utf-8'  # noqa
)


class InstanceSettings(views.APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        manager = global_preferences_registry.manager()
        manager.all()
        all_preferences = manager.model.objects.all().order_by(
            'section', 'name'
        )
        api_preferences = [
            p
            for p in all_preferences
            if getattr(p.preference, 'show_in_api', False)
        ]
        data = serializers.GlobalPreferenceSerializer(
            api_preferences, many=True).data
        return Response(data, status=200)


class NodeInfo(views.APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        if not preferences.get('instance__nodeinfo_enabled'):
            return Response(status=404)
        data = nodeinfo.get()
        return Response(
            data, status=200, content_type=NODEINFO_2_CONTENT_TYPE)
