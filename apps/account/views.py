from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import (
    UserRegistrationSerializer, 
    PasswordChangeSerializer,
    RestorePasswordSerializer,
    SetRestoredPasswordSerializer,
    UsersSerializer,
    ArtistRegistrationSerializer,
    UpdateAccountSerializer
    )


User = get_user_model()




class UserView(APIView):
    def get(self, request, email):
            try:
                user = User.objects.get(email=email)
            except:
                return Response('Пользователя под таким первичным ключём не существует.',
                status=status.HTTP_404_NOT_FOUND)
            serializer = UsersSerializer(instance=user)
            # # usernames = [user.username for user in User.objects.all()]
            return Response(serializer.data, status=status.HTTP_200_OK)

class ListUsersView(APIView):
    def get(self, request):
        usernames = User.objects.all()
        list_ = []
        for user in usernames:
           B = {
            'user': user.username,
            'email': user.email,
            'image': f'http://127.0.0.1:8000/{user.image}'
           }
           list_.append(B)
        return Response(list_)
        


class UserRegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Спасибо за регистрацию! Ссылка для активации учетной записи отправлена Вам на почту.',
                status=status.HTTP_201_CREATED
            )

class ArtistRegistrationView(APIView):
    @swagger_auto_schema(request_body=ArtistRegistrationSerializer)
    def post(self, request: Request):
        serializer = ArtistRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Спасибо за регистрацию! Ссылка для активации учетной записи отправлена Вам на почту.',
                status=status.HTTP_201_CREATED
            )


class AccountActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Страница не найдена...', 
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Учетная запись активирована! Теперь Вы можете войти на сайт и пройти логин.', 
            status=status.HTTP_200_OK
            )

class ArtistActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Страница не найдена...', 
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.is_artist = True
        user.activation_code = ''
        user.save()
        return Response(
            'Учетная запись активирована! Теперь Вы исполнитель!', 
            status=status.HTTP_200_OK
            )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PasswordChangeSerializer)
    def post(self, request: Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно изменен.',
                status=status.HTTP_200_OK
            )


class RestorePasswordView(APIView):

    @swagger_auto_schema(request_body=RestorePasswordSerializer)
    def post(self, request: Request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Код для восстановления пароля был отправлен Вам на почту.',
                status=status.HTTP_200_OK
            )


class SetRestoredPasswordView(APIView):
    @swagger_auto_schema(request_body=SetRestoredPasswordSerializer)
    def post(self, request: Request):
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно восстановлен.',
                status=status.HTTP_200_OK
            )

class UpdateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, email):
        try:
            obj = User.objects.get(email=email)
        except:
            return Response('Пользователь с таким первичным ключем отсутствует.',
            status=status.HTTP_404_NOT_FOUND
            )
        serializer = UpdateAccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.update(obj, serializer.validated_data)
            answer = {"status": "UPDATE" }
            answer.update(serializer.data, status=status.HTTP_200_OK)
            return Response(answer)



class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    
    def delete(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'Учетная запись удалена.',
            status=status.HTTP_204_NO_CONTENT
        )

