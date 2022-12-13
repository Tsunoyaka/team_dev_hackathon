from rest_framework.viewsets import ModelViewSet

from .serializers import MusAlbumSerializer, AlbumSerializer
from .models import Album, MusAlbum

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class MusAlbumVIewSet(ModelViewSet):
    queryset = MusAlbum.objects.all()
    serializer_class = MusAlbumSerializer