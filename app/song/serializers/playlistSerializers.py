from rest_framework import serializers

from core.models import PlayList


class PlayListSerializer(serializers.ModelSerializer):
    """Serializer for playlist obj"""
    class Meta:
        model = PlayList
        fields = ('id', 'name')
        read_only_fields = ('id',)
