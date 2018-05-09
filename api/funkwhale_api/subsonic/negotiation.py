from rest_framework import exceptions
from rest_framework import negotiation

from . import renderers


MAPPING = {
    'json': (renderers.SubsonicJSONRenderer(), 'application/json'),
    'xml': (renderers.SubsonicXMLRenderer(), 'text/xml'),
}


class SubsonicContentNegociation(negotiation.DefaultContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix=None):
        path = request.path
        data = request.GET or request.POST
        requested_format = data.get('f', 'xml')
        try:
            return MAPPING[requested_format]
        except KeyError:
            raise exceptions.NotAcceptable(available_renderers=renderers)
