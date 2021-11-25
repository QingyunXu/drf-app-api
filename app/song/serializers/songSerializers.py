from song.serializers.singerSerializers import SingerSerializer
from rest_framework import serializers

from core.models import Singer, Song


class SongSerializer(serializers.ModelSerializer):
    singers = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Singer.objects.all()
    )

    class Meta:
        model = Song
        fields = ('id', 'title', 'length', 'release', 'singers')
        read_only_fields = ('id',)


class SongDetailsSerializer(serializers.ModelSerializer):
    singers = SingerSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ('id', 'title', 'length', 'release', 'singers',)
        read_only_fields = fields
