from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializers import (
    UserSerializer,
    ForAdminSerializer,
    ForUserSerializer,
    TokenSerializer
)
from .models import User


class APISignUp(APIView):
    """Регистрация пользователя и отправка сообщения."""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
            )
        except IntegrityError:
            return Response(
                'Данный пользователь уже зарегестрирован',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APICode(APIView):
    """Запрос отправленного ранее кода."""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            email = serializer.data['email']
            user = get_object_or_404(User, username=username, email=email)
            self.create_confirmation_code_and_send_email(user)
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIToken(APIView):
    """Выдача токена."""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        if default_token_generator.check_token(
            user, serializer.data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation code': 'Некорректный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class APIUser(APIView):
    """Изменение своих данных."""
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = ForUserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = ForUserSerializer(
            user, data=request.data, partial=True, many=False
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetForAdmin(ModelViewSet):
    """Работа с пользователями для администратора."""
    queryset = User.objects.all()
    serializer_class = ForAdminSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'
