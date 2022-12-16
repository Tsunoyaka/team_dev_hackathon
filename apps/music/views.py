from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters import rest_framework as rest_filter
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from .permissions import IsOwner
from .serializers import MusicCreateSerializer, MusicSerializer, GenreSerializer, LikeMusicSerializer, LikeSerializer
from .models import Music, Genre, LikeMusic

from django.contrib.auth import get_user_model

User = get_user_model()

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
        if self.action == 'my_like' and self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'like' and self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner, IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        music = self.get_object()
        serializer = LikeMusicSerializer(data=request.data, context={
            'request': request,
            'music': music,
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            elif request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked!')

    @action(methods=["GET"], detail=False, url_path='my-like')
    def my_like(self, request):
        add_album = LikeMusic.objects.filter(user=request.user)
        add_serializers = LikeSerializer(add_album, many=True).data
        list_ = []
        for i in add_serializers:
            i['image'] = f"/media/{i['image']}"
            i['music'] = f"/media/{i['music']}"
            list_.append(i)
        return Response(data=list_)
    
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
