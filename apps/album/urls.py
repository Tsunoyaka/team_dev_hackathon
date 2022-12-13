from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import AlbumViewSet, MusAlbumVIewSet


router = DefaultRouter()
router.register('albums', AlbumViewSet, 'alb')
router.register('musalbums', MusAlbumVIewSet, 'malb')

urlpatterns = [

]


urlpatterns += router.urls

