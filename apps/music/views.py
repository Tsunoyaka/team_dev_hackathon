from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters import rest_framework as rest_filter
from rest_framework import filters, status

from rest_framework.response import Response
from .permissions import IsOwner

from .serializers import MusicCreateSerializer, MusicSerializer, GenreSerializer
from .models import Music, Genre


class MusicViewSet(ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    filter_backends = [
        filters.SearchFilter, 
        rest_filter.DjangoFilterBackend]
    search_fields = ['title','artist__username']
    filterset_fields = ['genre']

    def get_serializer_class(self):
        if self.action == 'list':
            return MusicSerializer
        elif self.action == 'create':
            return MusicCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner, IsAdminUser]
        return super().get_permissions()


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner, IsAdminUser]
        return super().get_permissions()
