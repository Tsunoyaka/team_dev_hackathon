from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ChangePasswordView, 
    DeleteAccountView, 
    UserRegistrationView, 
    AccountActivationView, 
    RestorePasswordView, 
    SetRestoredPasswordView, 
    ListUsersView, 
    UserView, 
    ArtistActivationView, 
    ArtistRegistrationView
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('register/artist/', ArtistRegistrationView.as_view(), name='artist_register'),
    path('activate/artist/<str:activation_code>/', ArtistActivationView.as_view(), name='activate_artist'),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('activate/<str:activation_code>/', AccountActivationView.as_view(), name='activation'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('restore-password/',  RestorePasswordView.as_view(), name='restored_password'),
    path('set-restored-password/', SetRestoredPasswordView.as_view(), name='set_restored_password'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('user/<str:pk>/', UserView.as_view()),
    path('users/', ListUsersView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
