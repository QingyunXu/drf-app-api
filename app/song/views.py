from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import PlayList, Singer, Song
from core.permissions import IsAdminOrReadOnly
from song.serializers.playlistSerializers import PlaylistSerializer,\
    PlaylistDetailsSerializer, WritePlaylistSerializer
from song.serializers.singerSerializers import SingerSerializer
from song.serializers.songSerializers import SongSerializer, \
    SongDetailsSerializer


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = SingerSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    def _params_to_ints(self, qs):
        """convert a list of string ids to int"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """retrieve songs by singer"""
        singers = self.request.query_params.get('singers')
        queryset = self.queryset
        if singers:
            singer_ids = self._params_to_ints(singers)
            queryset = queryset.filter(singers__id__in=singer_ids)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SongDetailsSerializer
        return SongSerializer


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PlayList.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlaylistDetailsSerializer
        elif self.action == 'create':
            return WritePlaylistSerializer
        return PlaylistSerializer
