from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .serializers import PlaylistSerializer, MusPlaylistSerializer, PlaylistDetailSerializer
from .permissions import IsOwner
from .models import Playlist, MusPlaylist

from apps.album.models import AddAlbum
from apps.album.serializers import AddAlbumSerializer

class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
 
    def get_serializer_class(self):
        if self.action == 'list':
            return PlaylistSerializer
        elif self.action == 'retrieve':
            return PlaylistDetailSerializer
        return super().get_serializer_class() 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'my_playlist' and self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    @action(methods=["GET"], detail=False, url_path='my-playlist')
    def my_playlist(self, request):
        add_album = AddAlbum.objects.filter(user=request.user)
        add_serializers = AddAlbumSerializer(add_album, many=True).data
        playlist = Playlist.objects.filter(user=request.user)
        add_playlist = PlaylistSerializer(playlist, many=True).data
        list_= []
        for image in add_serializers:
            image['image'] = f"/media/{image['image']}"
            list_.append(image)
        if add_playlist or list_:
            return Response(data=[add_playlist, list_], status=status.HTTP_200_OK)
        return Response('У вас нет плейлиста', status=status.HTTP_204_NO_CONTENT)


class MusPlaylistViewSet(ModelViewSet):
    queryset = MusPlaylist.objects.all()
    serializer_class = MusPlaylistSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
