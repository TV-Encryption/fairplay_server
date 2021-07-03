import base64
from logging import getLogger
from typing import Tuple
from uuid import UUID

import requests
from django.conf import settings
from FairplayKSM import generate_ckc
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import FAIRPLAY_ASK, FAIRPLAY_PRIVATE_KEY
from fairplay_server.ksm.api.serializers import (
    KeyRequestBodySerializer,
    KeyResponseBodySerializer,
)
from fairplay_server.ksm.models import KeyResponseBody


class ContentKey(APIView):
    logger = getLogger(__name__)

    @classmethod
    def post(cls, request, format=None):

        request_serializer = KeyRequestBodySerializer(data=request.data)

        request_serializer.is_valid(raise_exception=True)

        request_body = request_serializer.save()
        spc = base64.b64decode(request_body.spc)
        key_ref = base64.b64encode(request_body.key_ref.bytes)

        ckc = generate_ckc(
            key_ref=key_ref,
            spc=spc,
            key_fetch_callback=cls.get_key,
            p_key_pem=FAIRPLAY_PRIVATE_KEY,
            ask=FAIRPLAY_ASK,
        )

        response_body = KeyResponseBody(ckc=base64.b64encode(ckc).decode("ascii"))

        response_serializer = KeyResponseBodySerializer(response_body)
        return Response(response_serializer.data)

    @classmethod
    def get_key(cls, asset_id: bytes) -> Tuple[bytes, bytes]:

        key_ref = UUID(bytes=base64.b64decode(asset_id))

        token = settings.KEYSERVER_TOKEN
        header = {"Authorization": "Token " + token}
        url = settings.KEYSERVER_BASE_URL + "/" + str(key_ref)
        try:
            respond = requests.get(url, headers=header)
        except Exception as e:
            cls.logger.exception("Failed fetching key.")
            raise e
        if respond.status_code == 200:
            json = respond.json()
            iv = bytes.fromhex(json["init_vector"])
            key = bytes.fromhex(json["key"])
            return iv, key
        raise RuntimeError(f"HTTP status Code: {respond.status_code}")


content_key_view = ContentKey.as_view()
