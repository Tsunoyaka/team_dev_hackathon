from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import PlaylistViewSet, MusPlaylistViewSet


router = DefaultRouter()
router.register('crud-playlist', PlaylistViewSet, 'playlist')
router.register('mus-playlist', MusPlaylistViewSet, 'add-playlist')


urlpatterns = [

]


urlpatterns += router.urls

