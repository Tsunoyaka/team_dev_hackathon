from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import AlbumViewSet, MusAlbumViewSet, AddAlbumViewSet


router = DefaultRouter()
router.register('albums', AlbumViewSet, 'alb')
router.register('mus-albums', MusAlbumViewSet, 'malb')
router.register('add-albums', AddAlbumViewSet, 'add-alb')

urlpatterns = [

]


urlpatterns += router.urls

