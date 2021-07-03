from rest_framework import serializers

from fairplay_server.ksm.models import KeyRequestBody, KeyResponseBody


class KeyRequestBodySerializer(serializers.Serializer):
    spc = serializers.CharField()
    key_ref = serializers.UUIDField()

    def update(self, instance, validated_data):
        instance.spc = validated_data.get("spc", instance.spc)
        return instance

    def create(self, validated_data):
        return KeyRequestBody(**validated_data)


class KeyResponseBodySerializer(serializers.Serializer):
    ckc = serializers.CharField()

    def update(self, instance, validated_data):
        instance.ckc = validated_data.get("ckc", instance.ckc)
        return instance

    def create(self, validated_data):
        return KeyResponseBody(**validated_data)
