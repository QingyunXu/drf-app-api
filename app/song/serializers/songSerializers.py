from rest_framework import serializers

from core.models import Singer, PlayList, Song


class SongSerializer(serializers.ModelSerializer):
    playlists = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=PlayList.objects.all()
    )
    singers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Singer.objects.all()
    )

    class Meta:
        model = Song
        fields = ('id', 'title', 'length', 'release', 'singers', 'playlists')
        read_only_fields = ('id',)
        write_only_fields = ('playlists',)
