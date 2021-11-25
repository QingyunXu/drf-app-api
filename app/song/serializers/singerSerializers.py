from rest_framework import serializers

from core.models import Singer


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = ('id', 'name', 'image')
        read_only_fields = ('id',)
