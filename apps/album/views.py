from rest_framework.viewsets import ModelViewSet

from .serializers import MusAlbumSerializer, AlbumSerializer, AlbumDetailSerializer, AddAlbumSerializer
from .models import Album, MusAlbum, AddAlbum
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumSerializer
        elif self.action == 'retrieve':
            return AlbumDetailSerializer
        return super().get_serializer_class() 

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         self.permission_classes = [AllowAny]
    #     if self.action == 'my_albums' and self.request.method == 'GET':
    #         self.permission_classes = [IsAdminUser]
    #     # if self.action in ['create', 'comment', 'set_rating', 'like']:
    #     #     self.permission_classes = [IsAuthenticated]
    #     # if self.action in ['destroy', 'update', 'partial_update']:
    #     #     self.permission_classes = [IsOwner]
    #     return super().get_permissions()

    @action(methods=["GET"], detail=False, url_path='my-albums')
    def my_albums(self, request):
        album = Album.objects.filter(user=request.user)
        add_album = AddAlbum.objects.filter(user=request.user)
        add_serializers = AddAlbumSerializer(add_album, many=True).data
        serializers = AlbumSerializer(album, many=True).data
        if serializers:
            return Response(data=[serializers, add_serializers])
        return Response('У вас нет альбомов')




class MusAlbumVIewSet(ModelViewSet):
    queryset = AddAlbum.objects.all()
    serializer_class = AddAlbumSerializer