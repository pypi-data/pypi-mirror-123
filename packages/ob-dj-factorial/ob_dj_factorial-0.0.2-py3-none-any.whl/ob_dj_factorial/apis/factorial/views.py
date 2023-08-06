import logging

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class CallBackView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    allowed_methods = [
        "POST",
    ]

    def post(self, request) -> Response:

        # TODO: Hash verification not working :/
        # if not signature == hs_signature:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        # TODO: Replace with Celery Task to asyncly process the payload
        # for event in request.data:
        #     handler = HubSpotCallbackProcessor(payload=event)
        #     handler.process()
        return Response(status=status.HTTP_200_OK)
