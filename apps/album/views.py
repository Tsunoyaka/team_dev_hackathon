from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .serializers import (
    MusAlbumSerializer, 
    AlbumSerializer, 
    AlbumDetailSerializer, 
    AddAlbumSerializer
    )
from .models import Album, MusAlbum, AddAlbum
from .permissions import IsOwner
from rest_framework import filters, status



class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['album','user__username']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumSerializer
        elif self.action == 'retrieve':
            return AlbumDetailSerializer
        return super().get_serializer_class() 

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class AddAlbumViewSet(ModelViewSet):
    queryset = AddAlbum.objects.all()
    serializer_class = AddAlbumSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class MusAlbumViewSet(ModelViewSet):
    queryset = MusAlbum.objects.all()
    serializer_class = MusAlbumSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsOwner]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
