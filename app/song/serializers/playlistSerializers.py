from song.serializers.songSerializers import SongSerializer
from rest_framework import serializers

from core.models import PlayList, Song


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer for playlist obj"""
    songs = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Song.objects.all
    )

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'songs')
        read_only_fields = ('id',)


class WritePlaylistSerializer(serializers.ModelSerializer):
    """Serializer for write playlist obj"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'songs', 'user')
        read_only_fields = ('id',)


class PlaylistDetailsSerializer(serializers.ModelSerializer):
    """Serializer for display playlist obj"""
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'songs')
        read_only_fields = fields
