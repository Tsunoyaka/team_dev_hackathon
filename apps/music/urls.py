from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import MusicViewSet, GenreViewSet


router = DefaultRouter()
router.register('note', MusicViewSet, 'music')
router.register('genre', GenreViewSet, 'genre')

urlpatterns = [

]


urlpatterns += router.urls

